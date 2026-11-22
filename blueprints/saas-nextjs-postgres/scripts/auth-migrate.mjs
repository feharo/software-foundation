// Node 22+ loads .env.local before launching the Better Auth CLI.
import { spawnSync } from "node:child_process";

if (!process.env.DATABASE_URL || !process.env.BETTER_AUTH_SECRET || process.env.BETTER_AUTH_SECRET.length < 32) {
  console.error("Configure DATABASE_URL e BETTER_AUTH_SECRET (mínimo de 32 caracteres) em .env.local.");
  process.exit(1);
}
const command = process.platform === "win32" ? "npx.cmd" : "npx";
const result = spawnSync(command, ["--yes", "auth@1.7.27", "migrate", "--yes"], {
  stdio: "inherit",
  env: process.env,
  shell: process.platform === "win32",
});
if (result.error) {
  console.error("Falha ao iniciar a CLI do Better Auth:", result.error.message);
}
process.exit(result.status ?? 1);
