
"""
เกม Pacman ควบคุมด้วย Joystick ผ่าน MCP3208 (Raspberry Pi)
-----------------------------------------------------------
การต่อวงจร (ตามการทดลองที่ 4):
  - GND  -> Ground ของ Raspberry Pi
  - +5   -> 3.3V ของ Raspberry Pi
  - VRx  -> CH0 ของ MCP3208
  - VRy  -> CH1 ของ MCP3208
  - SW   -> ขา GPIO ของ Raspberry Pi (ตั้งเป็น pull-up, กดแล้วเป็น LOW)

ต้องติดตั้งไลบรารีก่อนใช้งานบน Raspberry Pi:
  pip3 install pygame spidev RPi.GPIO

หมายเหตุ: ถ้ารันบนเครื่องที่ไม่มี Joystick ต่อจริง (เช่น ทดสอบบนคอมพิวเตอร์)
ให้ตั้งค่า USE_JOYSTICK = False ด้านล่าง เพื่อเล่นด้วยปุ่มลูกศรบนคีย์บอร์ดแทน
"""

import time
import random
import sys

import pygame

# ---------- ตั้งค่าว่าจะใช้ Joystick จริง (Raspberry Pi) หรือคีย์บอร์ด (ทดสอบบนคอม) ----------
USE_JOYSTICK = True   # ถ้ารันบน Raspberry Pi ที่ต่อวงจรจริง ให้เป็น True

if USE_JOYSTICK:
    import spidev
    import RPi.GPIO as GPIO

    # ---------- ตั้งค่า SPI สำหรับ MCP3208 ----------
    spi = spidev.SpiDev()
    spi.open(0, 0)
    spi.max_speed_hz = 500000

    # ---------- ตั้งค่า GPIO สำหรับขา SW (ปุ่มกด) ----------
    SW_PIN = 17  # แก้เลขนี้ให้ตรงกับขา GPIO ที่ต่อจริง
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SW_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def read_channel(channel):
        adc = spi.xfer2([6 | (channel & 4) >> 2, (channel & 3) << 6, 0])
        data = ((adc[1] & 15) << 8) + adc[2]
        return data

    def read_joystick():
        """คืนค่า (dx, dy, button_pressed) จาก joystick จริง"""
        vrx = read_channel(0)
        vry = read_channel(1)
        sw_state = GPIO.input(SW_PIN)  # 0 = กดปุ่ม

        # ค่ากลางของ ADC 12-bit อยู่ที่ประมาณ 2048 (0-4095)
        center = 2048
        deadzone = 400  # ช่วงตรงกลางที่ถือว่ายังไม่โยก

        dx = dy = 0
        if vrx - center > deadzone:
            dx = 1
        elif center - vrx > deadzone:
            dx = -1

        if vry - center > deadzone:
            dy = 1
        elif center - vry > deadzone:
            dy = -1

        return dx, dy, (sw_state == 0)

else:
    def read_joystick():
        """โหมดทดสอบ: อ่านค่าจากปุ่มลูกศรบนคีย์บอร์ดแทน joystick"""
        keys = pygame.key.get_pressed()
        dx = dy = 0
        if keys[pygame.K_LEFT]:
            dx = -1
        elif keys[pygame.K_RIGHT]:
            dx = 1
        if keys[pygame.K_UP]:
            dy = -1
        elif keys[pygame.K_DOWN]:
            dy = 1
        pressed = keys[pygame.K_SPACE]
        return dx, dy, pressed


# =====================================================================
#                           ตัวเกม Pacman
# =====================================================================

TILE = 24          # ขนาดของแต่ละช่องตาราง (พิกเซล)
FPS = 60
MOVE_INTERVAL = 0.14   # วินาทีต่อการขยับ 1 ช่อง (ยิ่งน้อยยิ่งเร็ว)

# แผนที่เขาวงกต: # = กำแพง, . = จุดคะแนน, ' ' = ทางเดินว่าง, P = จุดเริ่ม Pacman, G = จุดเริ่มผี
MAZE = [
    "############################",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.#..#.#...#.##.#...#.#..#.#",
    "#.####.#####.##.#####.####.#",
    "#..........................#",
    "#.####.##.########.##.####.#",
    "#.####.##.########.##.####.#",
    "#......##....##....##......#",
    "######.##### ## #####.######",
    "     #.##    G     ##.#     ",
    "######.## ######## ##.######",
    "      .   #G G  G#   .      ",
    "######.## ######## ##.######",
    "     #.##          ##.#     ",
    "######.## ######## ##.######",
    "#............##............#",
    "#.####.#####.##.#####.####.#",
    "#.####.#####.##.#####.####.#",
    "#...##...P............##...#",
    "###.##.##.########.##.##.###",
    "#......##....##....##......#",
    "#.##########.##.##########.#",
    "#...........##.............#",
    "############################",
]

ROWS = len(MAZE)
COLS = len(MAZE[0])
WIDTH = COLS * TILE
HEIGHT = ROWS * TILE + 60  # เผื่อพื้นที่แสดงคะแนนด้านบน

WALL_COLOR = (33, 33, 222)
BG_COLOR = (0, 0, 0)
DOT_COLOR = (255, 184, 174)
PACMAN_COLOR = (255, 255, 0)
GHOST_COLORS = [(255, 0, 0), (255, 184, 255), (0, 255, 255), (255, 184, 82)]
TEXT_COLOR = (255, 255, 255)


def cell(r, c):
    if 0 <= r < ROWS and 0 <= c < COLS:
        return MAZE[r][c]
    return "#"


def is_wall(r, c):
    return cell(r, c) == "#"


class Entity:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.dir = (0, 0)

    @property
    def pos(self):
        return (self.col * TILE + TILE // 2, self.row * TILE + TILE // 2 + 60)

    def try_move(self, dr, dc):
        nr, nc = self.row + dr, self.col + dc
        if not is_wall(nr, nc):
            self.row, self.col = nr, nc
            return True
        return False


def find_positions():
    dots = set()
    start = None
    ghosts = []
    for r, row in enumerate(MAZE):
        for c, ch in enumerate(row):
            if ch == ".":
                dots.add((r, c))
            elif ch == "P":
                start = (r, c)
            elif ch == "G":
                ghosts.append((r, c))
    if start is None:
        start = (ROWS // 2, COLS // 2)
    return dots, start, ghosts


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pacman - Joystick Edition")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24, bold=True)
    big_font = pygame.font.SysFont("Arial", 48, bold=True)

    dots, pac_start, ghost_starts = find_positions()
    pacman = Entity(*pac_start)
    ghosts = [Entity(r, c) for r, c in ghost_starts] or [Entity(1, 1)]

    score = 0
    lives = 3
    game_over = False
    win = False

    last_move_time = time.time()
    last_ghost_time = time.time()
    pending_dir = (0, 0)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # ---------- อ่านค่าจาก Joystick (หรือคีย์บอร์ดในโหมดทดสอบ) ----------
        dx, dy, button_pressed = read_joystick()
        if dx != 0:
            pending_dir = (0, dx)     # แกน X ควบคุมซ้าย-ขวา (คอลัมน์)
        elif dy != 0:
            pending_dir = (dy, 0)     # แกน Y ควบคุมขึ้น-ลง (แถว)

        if button_pressed and (game_over or win):
            # กดปุ่มเพื่อเริ่มเกมใหม่
            dots, pac_start, ghost_starts = find_positions()
            pacman = Entity(*pac_start)
            ghosts = [Entity(r, c) for r, c in ghost_starts] or [Entity(1, 1)]
            score = 0
            lives = 3
            game_over = False
            win = False

        now = time.time()

        if not game_over and not win:
            # ---------- ขยับ Pacman ----------
            if now - last_move_time >= MOVE_INTERVAL:
                last_move_time = now
                dr, dc = pending_dir
                if dr != 0 or dc != 0:
                    pacman.try_move(dr, dc)

                if (pacman.row, pacman.col) in dots:
                    dots.discard((pacman.row, pacman.col))
                    score += 10
                    if not dots:
                        win = True

            # ---------- ขยับผี (สุ่มทิศทางแบบง่าย) ----------
            if now - last_ghost_time >= MOVE_INTERVAL * 1.3:
                last_ghost_time = now
                for g in ghosts:
                    choices = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                    random.shuffle(choices)
                    for dr, dc in choices:
                        nr, nc = g.row + dr, g.col + dc
                        if not is_wall(nr, nc):
                            g.row, g.col = nr, nc
                            break

            # ---------- เช็คชนผี ----------
            for g in ghosts:
                if g.row == pacman.row and g.col == pacman.col:
                    lives -= 1
                    pacman.row, pacman.col = pac_start
                    if lives <= 0:
                        game_over = True
                    break

        # ---------- วาดภาพ ----------
        screen.fill(BG_COLOR)

        # แผนที่และจุดคะแนน
        for r in range(ROWS):
            for c in range(COLS):
                x, y = c * TILE, r * TILE + 60
                if is_wall(r, c):
                    pygame.draw.rect(screen, WALL_COLOR, (x, y, TILE, TILE))
                elif (r, c) in dots:
                    pygame.draw.circle(screen, DOT_COLOR, (x + TILE // 2, y + TILE // 2), 3)

        # Pacman
        pygame.draw.circle(screen, PACMAN_COLOR, pacman.pos, TILE // 2 - 2)

        # ผี
        for i, g in enumerate(ghosts):
            color = GHOST_COLORS[i % len(GHOST_COLORS)]
            gx, gy = g.pos
            pygame.draw.circle(screen, color, (gx, gy), TILE // 2 - 2)

        # แถบคะแนนด้านบน
        pygame.draw.rect(screen, (20, 20, 20), (0, 0, WIDTH, 60))
        score_text = font.render(f"Score: {score}", True, TEXT_COLOR)
        lives_text = font.render(f"Lives: {lives}", True, TEXT_COLOR)
        screen.blit(score_text, (10, 18))
        screen.blit(lives_text, (WIDTH - 130, 18))

        if game_over:
            msg = big_font.render("GAME OVER", True, (255, 60, 60))
            hint = font.render("กดปุ่ม Joystick (SW) เพื่อเริ่มใหม่", True, TEXT_COLOR)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))
        elif win:
            msg = big_font.render("YOU WIN!", True, (60, 255, 60))
            hint = font.render("กดปุ่ม Joystick (SW) เพื่อเล่นใหม่", True, TEXT_COLOR)
            screen.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2 - 40))
            screen.blit(hint, (WIDTH // 2 - hint.get_width() // 2, HEIGHT // 2 + 20))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    if USE_JOYSTICK:
        GPIO.cleanup()
        spi.close()
    sys.exit()


if __name__ == "__main__":
    main()

