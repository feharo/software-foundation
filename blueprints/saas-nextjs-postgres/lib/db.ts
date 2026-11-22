import { Pool } from "pg";

// One pool per Node.js server process. Never imported into Client Components.
const url = process.env.DATABASE_URL;
if (!url) throw new Error("DATABASE_URL não configurada. Veja .env.example.");

const globalPool = globalThis as typeof globalThis & { __foundationPgPool?: Pool };
export const pool = globalPool.__foundationPgPool ?? new Pool({
  connectionString: url,
  max: 10,
  connectionTimeoutMillis: 5000,
  idleTimeoutMillis: 30000,
});
if (process.env.NODE_ENV !== "production") globalPool.__foundationPgPool = pool;
