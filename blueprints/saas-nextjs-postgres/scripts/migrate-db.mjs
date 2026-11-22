// Idempotent baseline bootstrap. For subsequent schema changes use versioned migrations.
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { dirname, resolve } from "node:path";
import pg from "pg";

const url = process.env.DATABASE_URL;
if (!url) {
  console.error("DATABASE_URL ausente. Configure .env.local antes de migrar.");
  process.exit(1);
}
const currentDir = dirname(fileURLToPath(import.meta.url));
const file = resolve(currentDir, "../db/schema.sql");
const pool = new pg.Pool({ connectionString: url, max: 1, connectionTimeoutMillis: 5000 });
try {
  const sql = await readFile(file, "utf8");
  await pool.query(sql);
  console.log("Migração do domínio aplicada com sucesso.");
} catch (error) {
  console.error("Falha ao migrar domínio:", error instanceof Error ? error.message : "erro desconhecido");
  process.exitCode = 1;
} finally {
  await pool.end();
}
