-- Application tables. Apply only AFTER Better Auth creates its own "user" table.
-- Only the Next.js server connects to this database; clients never receive DATABASE_URL.
-- All mutations and queries in routes must enforce the authenticated owner.

BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS workspaces (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name varchar(80) NOT NULL CHECK (length(trim(name)) BETWEEN 3 AND 80),
  owner_id text NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS workspaces_owner_idx ON workspaces (owner_id, created_at);

CREATE TABLE IF NOT EXISTS tasks (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  workspace_id uuid NOT NULL REFERENCES workspaces(id) ON DELETE CASCADE,
  created_by text NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
  title varchar(160) NOT NULL CHECK (length(trim(title)) BETWEEN 1 AND 160),
  done boolean NOT NULL DEFAULT false,
  created_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS tasks_workspace_created_idx ON tasks (workspace_id, created_at DESC, id DESC);

COMMIT;
