import { NextResponse } from "next/server";
import { pool } from "../../../lib/db";
import { currentUserId } from "../../../lib/identity";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

export async function GET() {
  try {
    const userId = await currentUserId();
    if (!userId) return NextResponse.json({ error: "Entre para continuar." }, { status: 401 });
    const result = await pool.query<{ id: string; name: string }>(
      "SELECT id, name FROM workspaces WHERE owner_id = $1 ORDER BY created_at ASC, id ASC",
      [userId],
    );
    return NextResponse.json({ items: result.rows }, { headers: { "Cache-Control": "no-store" } });
  } catch {
    return NextResponse.json({ error: "Não conseguimos listar seus espaços." }, { status: 500 });
  }
}

export async function POST(request: Request) {
  try {
    const userId = await currentUserId();
    if (!userId) return NextResponse.json({ error: "Entre para continuar." }, { status: 401 });
    const body: unknown = await request.json().catch(() => null);
    if (!body || typeof body !== "object" || !("name" in body) ||
        typeof body.name !== "string" || body.name.trim().length < 3 || body.name.trim().length > 80) {
      return NextResponse.json({ error: "Nome deve ter de 3 a 80 caracteres." }, { status: 400 });
    }
    const result = await pool.query<{ id: string; name: string }>(
      "INSERT INTO workspaces (owner_id, name) VALUES ($1, $2) RETURNING id, name",
      [userId, body.name.trim()],
    );
    return NextResponse.json({ item: result.rows[0] }, { status: 201 });
  } catch {
    return NextResponse.json({ error: "Não conseguimos criar o espaço." }, { status: 500 });
  }
}
