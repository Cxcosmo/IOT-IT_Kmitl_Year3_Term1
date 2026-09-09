import { z } from "zod";
import { positiveIdSchema } from "./common.js";

export const authorIdParamsSchema = z.strictObject({
  authorId: positiveIdSchema,
});

export const authorBodySchema = z.strictObject({
  firstname: z.string().trim().min(1).max(100),
  surname: z.string().trim().min(1).max(100),
  userID: z.string().trim().min(1).max(100),
  birthday: z.string().regex(/^\d{4}-\d{2}-\d{2}$/, "birthday must be YYYY-MM-DD"),
  gender: z.enum(["male", "female", "other"]),
});
