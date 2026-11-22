import { NextResponse } from "next/server";
import { pool } from "../../../lib/db";
import { currentUserId } from "../../../lib/identity";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const isUuid = (value: unknown): value is string =>
  typeof value === "string" && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);

function fail(error: string, status: number) {
  return NextResponse.json({ error }, { status });
}

async function ownerCanAccess(owner: string, workspaceId: string): Promise<boolean> {
  const result = await pool.query(
    "SELECT 1 FROM workspaces WHERE id = $1 AND owner_id = $2 LIMIT 1",
    [workspaceId, owner],
  );
  return (result.rowCount ?? 0) > 0;
}

export async function GET(request: Request) {
  try {
    const owner = await currentUserId();
    if (!owner) return fail("Entre para continuar.", 401);
    const url = new URL(request.url);
    const workspaceId = url.searchParams.get("workspaceId");
    if (!isUuid(workspaceId)) return fail("Espaço inválido.", 400);
    if (!await ownerCanAccess(owner, workspaceId)) return fail("Sem acesso a este espaço.", 403);
    const rawPage = Number(url.searchParams.get("page") || "1");
    if (!Number.isInteger(rawPage) || rawPage < 1 || rawPage > 10000) return fail("Página inválida.", 400);
    const search = (url.searchParams.get("search") || "").trim();
    if (search.length > 80) return fail("Pesquisa muito longa.", 400);
    // Treat the search term as literal text, not as SQL LIKE wildcards.
    const safeWhere = "workspace_id = $1 AND ($2 = '' OR strpos(lower(title), lower($2)) > 0)";
    const [items, count] = await Promise.all([
      pool.query<{ id: string; title: string; done: boolean; created_at: string }>(
        "SELECT id, title, done, created_at FROM tasks WHERE " + safeWhere +
        " ORDER BY created_at DESC, id DESC LIMIT $3 OFFSET $4",
        [workspaceId, search, 8, (rawPage - 1) * 8],
      ),
      pool.query<{ total: string }>(
        "SELECT count(*)::text AS total FROM tasks WHERE " + safeWhere,
        [workspaceId, search],
      ),
    ]);
    return NextResponse.json({
      items: items.rows, total: Number(count.rows[0]?.total ?? 0),
    }, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return fail("Não conseguimos carregar as atividades.", 500);
  }
}

export async function POST(request: Request) {
  try {
    const owner = await currentUserId();
    if (!owner) return fail("Entre para continuar.", 401);
    const body: unknown = await request.json().catch(() => null);
    if (!body || typeof body !== "object" || !("workspaceId" in body) || !("title" in body) ||
        !isUuid(body.workspaceId) || typeof body.title !== "string" ||
        body.title.trim().length < 1 || body.title.trim().length > 160) {
      return fail("Verifique o espaço e o nome da atividade.", 400);
    }
    const result = await pool.query(
      "INSERT INTO tasks (workspace_id, created_by, title) " +
      "SELECT id, $1, $3 FROM workspaces WHERE id = $2 AND owner_id = $1 RETURNING id",
      [owner, body.workspaceId, body.title.trim()],
    );
    if (!result.rowCount) return fail("Sem acesso a este espaço.", 403);
    return NextResponse.json({ item: result.rows[0] }, { status: 201 });
  } catch {
    return fail("Não conseguimos criar a atividade.", 500);
  }
}

export async function PATCH(request: Request) {
  try {
    const owner = await currentUserId();
    if (!owner) return fail("Entre para continuar.", 401);
    const body: unknown = await request.json().catch(() => null);
    if (!body || typeof body !== "object" || !("id" in body) || !("done" in body) ||
        !isUuid(body.id) || typeof body.done !== "boolean") return fail("Atualização inválida.", 400);
    const result = await pool.query(
      "UPDATE tasks AS t SET done = $3 FROM workspaces AS w " +
      "WHERE t.workspace_id = w.id AND w.owner_id = $1 AND t.id = $2 RETURNING t.id",
      [owner, body.id, body.done],
    );
    if (!result.rowCount) return fail("Atividade não encontrada ou sem acesso.", 404);
    return NextResponse.json({ ok: true });
  } catch {
    return fail("Não conseguimos atualizar a atividade.", 500);
  }
}

export async function DELETE(request: Request) {
  try {
    const owner = await currentUserId();
    if (!owner) return fail("Entre para continuar.", 401);
    const body: unknown = await request.json().catch(() => null);
    if (!body || typeof body !== "object" || !("id" in body) || !isUuid(body.id)) {
      return fail("ID inválido.", 400);
    }
    const result = await pool.query(
      "DELETE FROM tasks AS t USING workspaces AS w " +
      "WHERE t.workspace_id = w.id AND w.owner_id = $1 AND t.id = $2 RETURNING t.id",
      [owner, body.id],
    );
    if (!result.rowCount) return fail("Atividade não encontrada ou sem acesso.", 404);
    return NextResponse.json({ ok: true });
  } catch {
    return fail("Não conseguimos excluir a atividade.", 500);
  }
}
