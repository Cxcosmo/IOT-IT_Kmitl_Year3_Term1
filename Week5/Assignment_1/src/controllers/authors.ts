import { zValidator } from "@hono/zod-validator";
import { Hono } from "hono";
import { authorBodySchema, authorIdParamsSchema } from "../schemas/authors.js";
import {
  createAuthor,
  deleteAuthor,
  getAuthorById,
  getAuthors,
  updateAuthor,
} from "../services/authors.js";

export const authorsController = new Hono();

authorsController.get("/", async (c) => c.json(await getAuthors()));

authorsController.get(
  "/:authorId",
  zValidator("param", authorIdParamsSchema),
  async (c) => {
    const { authorId } = c.req.valid("param");
    const author = await getAuthorById(authorId);

    if (!author) {
      return c.json({ error: "Author not found" }, 404);
    }

    return c.json(author);
  },
);

authorsController.post("/", zValidator("json", authorBodySchema), async (c) => {
  const body = c.req.valid("json");
  const author = await createAuthor(body);
  c.header("Location", `/api/v1/authors/${author.id}`);
  return c.json(author, 201);
});

authorsController.patch(
  "/:authorId",
  zValidator("param", authorIdParamsSchema),
  zValidator("json", authorBodySchema),
  async (c) => {
    const { authorId } = c.req.valid("param");
    const body = c.req.valid("json");
    const author = await updateAuthor(authorId, body);

    if (!author) {
      return c.json({ error: "Author not found" }, 404);
    }

    return c.json(author);
  },
);

authorsController.delete(
  "/:authorId",
  zValidator("param", authorIdParamsSchema),
  async (c) => {
    const { authorId } = c.req.valid("param");
    const deleted = await deleteAuthor(authorId);

    if (!deleted) {
      return c.json({ error: "Author not found" }, 404);
    }

    return c.body(null, 204);
  },
);
