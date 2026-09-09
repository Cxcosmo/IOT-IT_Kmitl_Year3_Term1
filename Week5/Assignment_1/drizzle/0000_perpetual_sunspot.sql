CREATE TABLE "authors" (
	"id" integer PRIMARY KEY GENERATED ALWAYS AS IDENTITY (sequence name "authors_id_seq" INCREMENT BY 1 MINVALUE 1 MAXVALUE 2147483647 START WITH 1 CACHE 1),
	"firstname" text NOT NULL,
	"surname" text NOT NULL,
	"userID" text NOT NULL,
	"birthday" text NOT NULL,
	"gender" text NOT NULL
);
