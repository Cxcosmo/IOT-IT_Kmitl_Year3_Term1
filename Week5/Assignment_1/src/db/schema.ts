import { index, integer, pgTable, text } from "drizzle-orm/pg-core";

export const authors = pgTable("authors", {
  id: integer("id").primaryKey().generatedAlwaysAsIdentity(),
  firstname: text("firstname").notNull(),
  surname: text("surname").notNull(),
  userID: text("userID").notNull(),
  birthday: text("birthday").notNull(),
  gender: text("gender").notNull(),
});

export type Author = typeof authors.$inferSelect;
export type NewAuthor = typeof authors.$inferInsert;
