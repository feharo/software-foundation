/**
 * Supabase integration smoke using real Auth + PostgREST + RLS.
 * Invoke ONLY against a local Supabase project. No hosted or production credentials.
 */
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createClient } from "@supabase/supabase-js";

function localSettings() {
  const result = execFileSync("supabase", ["status", "-o", "env"], { encoding: "utf8", timeout: 12000 });
  const lines = result.split(/\r?\n/);
  const values = {};
  for (const line of lines) {
    const match = line.match(/^([A-Z][A-Z0-9_]*)=(.*)$/);
    if (match) values[match[1]] = match[2].replace(/^["']|["']$/g, "");
  }
  // Prevent accidentally running against an externally supplied project.
  const url = values.API_URL;
  const anon = values.ANON_KEY || values.PUBLISHABLE_KEY;
  if (!url || !anon) throw new Error("Supabase local não iniciado (API_URL/ANON_KEY ausentes).");
  const parsed = new URL(url);
  if (!["127.0.0.1", "localhost", "::1"].includes(parsed.hostname)) {
    throw new Error("Integração bloqueada: somente o Supabase local é permitido.");
  }
  return { url, anon };
}

function requireNoError(error, label) {
  if (error) throw new Error(label + ": " + error.message);
}

const { url, anon } = localSettings();
const makeClient = () => createClient(url, anon, {
  auth: { persistSession: false, autoRefreshToken: false },
});
const a = makeClient();
const b = makeClient();
const anonymous = makeClient();
const suffix = String(Date.now());

async function register(client, label) {
  const email = "foundation-" + suffix + "-" + label + "@example.test";
  const password = "Foundation-local-only-password-123!";
  const signup = await client.auth.signUp({ email, password });
  requireNoError(signup.error, "signup " + label);
  assert.ok(signup.data.user, "signup must create an authenticated user");
  if (!signup.data.session) {
    const login = await client.auth.signInWithPassword({ email, password });
    requireNoError(login.error, "login " + label);
    assert.ok(login.data.session, "local auto-confirm configuration must provide a session");
  }
  const user = await client.auth.getUser();
  requireNoError(user.error, "session " + label);
  assert.ok(user.data.user?.id, "authenticated user ID missing");
  return user.data.user.id;
}

const userA = await register(a, "a");
const userB = await register(b, "b");
assert.notEqual(userA, userB);

const workspaceA = await a.from("workspaces")
  .insert({ name: "A - local only", owner_id: userA }).select("id").single();
requireNoError(workspaceA.error, "owner create workspace");
const workspaceId = workspaceA.data?.id;
assert.ok(workspaceId);

const ownWorkspace = await a.from("workspaces").select("id").eq("id", workspaceId);
requireNoError(ownWorkspace.error, "owner workspace SELECT");
assert.equal(ownWorkspace.data.length, 1);

const otherWorkspace = await b.from("workspaces").select("id").eq("id", workspaceId);
requireNoError(otherWorkspace.error, "cross-tenant workspace SELECT");
assert.equal(otherWorkspace.data.length, 0, "user B must never read A's workspace");

const memberB = await b.from("workspace_memberships").select("workspace_id").eq("workspace_id", workspaceId);
requireNoError(memberB.error, "cross-tenant membership SELECT");
assert.equal(memberB.data.length, 0);

const forgedWorkspace = await b.from("workspaces")
  .insert({ name: "Forged owner", owner_id: userA });
assert.ok(forgedWorkspace.error, "user B must not create a workspace owned by user A");

const created = await a.from("tasks").insert({
  workspace_id: workspaceId, created_by: userA, title: "A private task",
}).select("id").single();
requireNoError(created.error, "owner create task");
const taskId = created.data?.id;
assert.ok(taskId);

const ownTasks = await a.from("tasks").select("id,done").eq("workspace_id", workspaceId);
requireNoError(ownTasks.error, "owner SELECT tasks");
assert.equal(ownTasks.data.length, 1);

const bTasks = await b.from("tasks").select("id").eq("workspace_id", workspaceId);
requireNoError(bTasks.error, "cross-tenant SELECT tasks");
assert.equal(bTasks.data.length, 0, "user B must not see A's task");

const forgedTask = await b.from("tasks").insert({
  workspace_id: workspaceId, created_by: userB, title: "Forged task",
});
assert.ok(forgedTask.error, "user B must not insert task into A's workspace");

const unauthenticated = await anonymous.from("tasks").select("id").eq("workspace_id", workspaceId);
assert.ok(unauthenticated.error || unauthenticated.data?.length === 0,
  "anonymous client must not access private tasks");

const patchedB = await b.from("tasks").update({ done: true }).eq("id", taskId).select("id");
assert.ok(patchedB.error || patchedB.data?.length === 0, "user B must not update A's task");

const deletedB = await b.from("tasks").delete().eq("id", taskId).select("id");
assert.ok(deletedB.error || deletedB.data?.length === 0, "user B must not delete A's task");

const stillOwn = await a.from("tasks").select("id,done").eq("id", taskId).single();
requireNoError(stillOwn.error, "owner task still exists");
assert.equal(stillOwn.data.done, false, "denied mutations cannot change A's task");

const changedA = await a.from("tasks").update({ done: true }).eq("id", taskId).select("id,done").single();
requireNoError(changedA.error, "owner task update");
assert.equal(changedA.data.done, true);

const removedA = await a.from("tasks").delete().eq("id", taskId).select("id");
requireNoError(removedA.error, "owner task delete");
assert.equal(removedA.data.length, 1);

console.log("OK: Supabase local Auth, workspaces, RLS tenant isolation and task mutations verified.");
