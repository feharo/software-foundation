// Runs only in CI against a disposable local PostgreSQL service.
import assert from "node:assert/strict";

const base = "http://localhost:3000";

async function call(path, method = "GET", body = undefined, cookie = "") {
  const response = await fetch(base + path, {
    method,
    headers: {
      Origin: base,
      "Content-Type": "application/json",
      ...(cookie ? { Cookie: cookie } : {}),
    },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  let data = null;
  try { data = await response.json(); } catch { /* Handle non-JSON error */ }
  return { response, data };
}

function sessionCookie(response) {
  const setCookies = response.headers.getSetCookie();
  assert.ok(setCookies.length > 0, "Auth must return session cookies");
  return setCookies.map((entry) => entry.split(";")[0]).join("; ");
}

async function register(suffix) {
  const result = await call("/api/auth/sign-up/email", "POST", {
    name: "Tester " + suffix,
    email: "foundation-" + suffix + "@example.test",
    password: "SaaS-test-password-12345!",
  });
  assert.equal(result.response.status, 200, "Better Auth sign-up failed: " + JSON.stringify(result.data));
  const cookie = sessionCookie(result.response);
  const session = await call("/api/auth/get-session", "GET", undefined, cookie);
  assert.equal(session.response.status, 200, "Session lookup failed");
  assert.ok(session.data?.user?.id, "Session user missing");
  return cookie;
}

const id = String(Date.now());
const first = await register(id + "-a");
const second = await register(id + "-b");

const w = await call("/api/workspaces", "POST", { name: "Workspace A" }, first);
assert.equal(w.response.status, 201, JSON.stringify(w.data));
const workspaceId = w.data?.item?.id;
assert.match(workspaceId, /^[0-9a-f-]{36}$/i);

const t = await call("/api/tasks", "POST", { workspaceId, title: "Private task" }, first);
assert.equal(t.response.status, 201, JSON.stringify(t.data));
const taskId = t.data?.item?.id;

const listA = await call("/api/tasks?workspaceId=" + workspaceId, "GET", undefined, first);
assert.equal(listA.response.status, 200, JSON.stringify(listA.data));
assert.equal(listA.data?.total, 1);

const listB = await call("/api/tasks?workspaceId=" + workspaceId, "GET", undefined, second);
assert.equal(listB.response.status, 403, "Tenant B must not read tenant A tasks");
const writeB = await call("/api/tasks", "POST", { workspaceId, title: "Forged" }, second);
assert.equal(writeB.response.status, 403, "Tenant B must not write into tenant A");
const patchB = await call("/api/tasks", "PATCH", { id: taskId, done: true }, second);
assert.equal(patchB.response.status, 404, "Tenant B must not update tenant A task");
const deleteB = await call("/api/tasks", "DELETE", { id: taskId }, second);
assert.equal(deleteB.response.status, 404, "Tenant B must not delete tenant A task");

const listAgain = await call("/api/tasks?workspaceId=" + workspaceId, "GET", undefined, first);
assert.equal(listAgain.data?.total, 1, "Cross-tenant attempts must not modify data");
console.log("OK: registration, sessions, workspace, task CRUD entrypoint and cross-tenant denial.");
