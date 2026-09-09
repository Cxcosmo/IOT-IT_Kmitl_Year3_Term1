import { eq } from "drizzle-orm";
import db from "../db/index.js";
import { authors, type Author, type NewAuthor } from "../db/schema.js";

export async function getAuthors(): Promise<Author[]> {
  return db.select().from(authors);
}

export async function getAuthorById(id: number): Promise<Author | undefined> {
  const [author] = await db.select().from(authors).where(eq(authors.id, id)).limit(1);
  return author;
}

export async function authorExists(id: number): Promise<boolean> {
  return (await getAuthorById(id)) !== undefined;
}

export async function createAuthor(data: NewAuthor): Promise<Author> {
  const [author] = await db.insert(authors).values(data).returning();
  if (!author) {
    throw new Error("Created author was not returned");
  }
  return author;
}

export async function updateAuthor(
  id: number,
  data: Partial<NewAuthor>,
): Promise<Author | undefined> {
  const [author] = await db.update(authors).set(data).where(eq(authors.id, id)).returning();
  return author;
}

export async function deleteAuthor(id: number): Promise<boolean> {
  const [deleted] = await db.delete(authors).where(eq(authors.id, id)).returning({ id: authors.id });
  return !!deleted;
}
