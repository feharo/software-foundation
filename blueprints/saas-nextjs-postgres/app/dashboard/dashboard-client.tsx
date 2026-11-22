"use client";

import { useRouter } from "next/navigation";
import { type FormEvent, useEffect, useState } from "react";
import Link from "next/link";
import { authClient } from "../../lib/auth-client";

type Workspace = { id: string; name: string };
type Task = { id: string; title: string; done: boolean; created_at: string };
type WorkspacesResponse = { items: Workspace[] };
type TasksResponse = { items: Task[]; total: number };
const PAGE_SIZE = 8;

async function api<T>(url: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(url, {
    ...options,
    cache: "no-store",
    headers: { "Content-Type": "application/json", ...options.headers },
  });
  const json: unknown = await response.json().catch(() => null);
  if (!response.ok) {
    const error = json && typeof json === "object" && "error" in json
      ? String(json.error) : "Não conseguimos concluir sua solicitação.";
    throw new Error(error);
  }
  return json as T;
}

export default function DashboardClient({ userEmail }: { userEmail: string }) {
  const router = useRouter();
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [loadingWorkspaces, setLoadingWorkspaces] = useState(true);
  const [workspaceId, setWorkspaceId] = useState("");
  const [newWorkspace, setNewWorkspace] = useState("");
  const [creatingWorkspace, setCreatingWorkspace] = useState(false);
  const [taskTitle, setTaskTitle] = useState("");
  const [taskBusy, setTaskBusy] = useState(false);
  const [taskPendingId, setTaskPendingId] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [total, setTotal] = useState(0);
  const [loadingTasks, setLoadingTasks] = useState(false);
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [page, setPage] = useState(1);
  const [revision, setRevision] = useState(0);
  const [error, setError] = useState("");
  const [workspaceError, setWorkspaceError] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    api<WorkspacesResponse>("/api/workspaces", { signal: controller.signal })
      .then((data) => {
        setWorkspaces(data.items);
        setWorkspaceId(data.items[0]?.id ?? "");
      })
      .catch((cause) => {
        if (!controller.signal.aborted) setWorkspaceError(cause instanceof Error ? cause.message : "Falha ao carregar.");
      })
      .finally(() => { if (!controller.signal.aborted) setLoadingWorkspaces(false); });
    return () => controller.abort();
  }, []);

  useEffect(() => {
    const id = setTimeout(() => setDebouncedSearch(search.trim()), 350);
    return () => clearTimeout(id);
  }, [search]);

  useEffect(() => {
    if (!workspaceId) {
      setTasks([]);
      setTotal(0);
      return;
    }
    const controller = new AbortController();
    setLoadingTasks(true);
    setError("");
    const query = new URLSearchParams({
      workspaceId, page: String(page), search: debouncedSearch,
    });
    api<TasksResponse>("/api/tasks?" + query.toString(), { signal: controller.signal })
      .then((data) => {
        if (!controller.signal.aborted) {
          setTasks(data.items);
          setTotal(data.total);
        }
      })
      .catch((cause) => {
        if (!controller.signal.aborted) setError(cause instanceof Error ? cause.message : "Falha ao carregar tarefas.");
      })
      .finally(() => { if (!controller.signal.aborted) setLoadingTasks(false); });
    return () => controller.abort();
  }, [workspaceId, page, debouncedSearch, revision]);

  async function createWorkspace(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (creatingWorkspace || newWorkspace.trim().length < 3) return;
    setCreatingWorkspace(true);
    setWorkspaceError("");
    try {
      const { item } = await api<{ item: Workspace }>("/api/workspaces", {
        method: "POST",
        body: JSON.stringify({ name: newWorkspace.trim() }),
      });
      setWorkspaces((current) => [...current, item]);
      setNewWorkspace("");
      setWorkspaceId(item.id);
      setTasks([]);
      setPage(1);
      setSearch("");
      setDebouncedSearch("");
    } catch (cause) {
      setWorkspaceError(cause instanceof Error ? cause.message : "Não foi possível criar o espaço.");
    } finally {
      setCreatingWorkspace(false);
    }
  }

  async function addTask(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!workspaceId || !taskTitle.trim() || taskBusy) return;
    setTaskBusy(true);
    setError("");
    try {
      await api("/api/tasks", {
        method: "POST", body: JSON.stringify({ workspaceId, title: taskTitle.trim() }),
      });
      setTaskTitle("");
      setSearch("");
      setDebouncedSearch("");
      setPage(1);
      setRevision((n) => n + 1);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Não foi possível salvar.");
    } finally {
      setTaskBusy(false);
    }
  }

  async function toggle(task: Task) {
    if (taskPendingId) return;
    setTaskPendingId(task.id);
    setError("");
    const updated = !task.done;
    setTasks((rows) => rows.map((row) => row.id === task.id ? { ...row, done: updated } : row));
    try {
      await api("/api/tasks", { method: "PATCH", body: JSON.stringify({ id: task.id, done: updated }) });
    } catch (cause) {
      setTasks((rows) => rows.map((row) => row.id === task.id ? { ...row, done: task.done } : row));
      setError(cause instanceof Error ? cause.message : "Não foi possível atualizar.");
    } finally {
      setTaskPendingId("");
    }
  }

  async function remove(task: Task) {
    if (taskPendingId || !window.confirm("Excluir esta atividade? Não será possível desfazer.")) return;
    setTaskPendingId(task.id);
    setError("");
    try {
      await api("/api/tasks", { method: "DELETE", body: JSON.stringify({ id: task.id }) });
      if (page > 1 && tasks.length === 1) setPage((n) => Math.max(1, n - 1));
      else setRevision((n) => n + 1);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Não foi possível excluir.");
    } finally {
      setTaskPendingId("");
    }
  }

  async function logout() {
    const result = await authClient.signOut();
    if (result.error) {
      setError(result.error.message || "Não foi possível sair.");
      return;
    }
    router.replace("/login");
    router.refresh();
  }

  const active = workspaces.find((workspace) => workspace.id === workspaceId);
  const pages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <div className="dashboard-shell">
      <a className="skip-link" href="#main">Pular para o conteúdo</a>
      <header className="dashboard-header">
        <Link href="/" className="brand">
          <span className="brand-mark" aria-hidden="true">S</span>
          <span>__APP_NAME__</span>
        </Link>
        <button type="button" className="text-button" onClick={() => void logout()}>Sair</button>
      </header>
      <div className="dashboard-layout">
        <aside className="dashboard-sidebar">
          <div className="sidebar-section">
            <span className="sidebar-badge">Minha conta</span>
            <p style={{ overflowWrap: "anywhere", marginTop: 12 }}>{userEmail}</p>
            <h2>{active?.name || "Meu primeiro espaço"}</h2>
            <p>Suas atividades são acessíveis somente pela conta proprietária.</p>
          </div>
        </aside>
        <main className="dashboard-main" id="main">
          <div className="dashboard-intro">
            <div>
              <p className="eyebrow">Visão geral</p>
              <h1>Seu espaço de trabalho.</h1>
              <p>Organize as prioridades sem perder o contexto.</p>
            </div>
          </div>
          <section className="dashboard-card" aria-labelledby="workspaces-heading">
            <div className="section-header"><h2 id="workspaces-heading">Espaços</h2></div>
            {workspaceError && <p className="feedback feedback-error" role="alert">{workspaceError}</p>}
            <form className="inline-form" onSubmit={createWorkspace}>
              <label className="sr-only" htmlFor="workspace-name">Nome do espaço</label>
              <input id="workspace-name" minLength={3} maxLength={80} required
                placeholder="Ex.: Minha empresa" value={newWorkspace}
                onChange={(event) => setNewWorkspace(event.target.value)} />
              <button type="submit" className="button button-primary" disabled={creatingWorkspace || newWorkspace.trim().length < 3}>
                {creatingWorkspace ? "Criando…" : "Criar espaço"}
              </button>
            </form>
            {loadingWorkspaces ? <p role="status">Carregando espaços…</p> :
              workspaces.length > 0 ?
              <div className="workspace-row">
                <label htmlFor="current-workspace" className="form-label">Espaço atual</label>
                <select id="current-workspace" value={workspaceId} onChange={(event) => {
                  setWorkspaceId(event.target.value);
                  setTasks([]);
                  setPage(1);
                }}>
                  {workspaces.map((item) => <option value={item.id} key={item.id}>{item.name}</option>)}
                </select>
              </div> :
              <div className="empty-state"><strong>Crie seu primeiro espaço</strong><p>Depois adicione atividades para começar.</p></div>
            }
          </section>
          <section className="dashboard-card" aria-labelledby="tasks-heading">
            <div className="section-header">
              <h2 id="tasks-heading">Atividades</h2>
              {workspaceId && <span className="sidebar-badge">{total} atividades</span>}
            </div>
            {error && <p role="alert" className="feedback feedback-error">{error}</p>}
            {workspaceId ? <>
              <form className="inline-form" onSubmit={addTask}>
                <label className="sr-only" htmlFor="task-title">Título da atividade</label>
                <input id="task-title" maxLength={160} required
                  placeholder="Qual sua próxima atividade?" value={taskTitle}
                  onChange={(event) => setTaskTitle(event.target.value)} />
                <button className="button button-primary" type="submit" disabled={taskBusy || !taskTitle.trim()}>
                  {taskBusy ? "Salvando…" : "Adicionar"}
                </button>
              </form>
              <div style={{ marginTop: 20 }}>
                <label htmlFor="task-search" className="form-label">Buscar atividades</label>
                <input id="task-search" type="search" maxLength={80} placeholder="Pesquisar pelo nome"
                  value={search} onChange={(event) => { setSearch(event.target.value); setPage(1); }} />
              </div>
              {loadingTasks ?
                <div aria-busy="true" aria-label="Carregando atividades" className="dashboard-skeleton" style={{ width: "100%", margin: "20px 0" }}>
                  <div className="skeleton skeleton-line" /><div className="skeleton skeleton-line" /><div className="skeleton skeleton-line" />
                </div> :
                tasks.length === 0 ?
                <div className="empty-state"><strong>{debouncedSearch ? "Nenhum resultado" : "Nenhuma atividade"}</strong><p>{debouncedSearch ? "Tente outro termo." : "Cadastre sua primeira atividade."}</p></div> :
                <ul className="task-list">
                  {tasks.map((task) => <li key={task.id} className="task-item">
                    <input className="task-toggle" type="checkbox" checked={task.done}
                      disabled={Boolean(taskPendingId)} onChange={() => void toggle(task)}
                      aria-label={(task.done ? "Desmarcar: " : "Concluir: ") + task.title} />
                    <span className={"task-item-title" + (task.done ? " done" : "")}>{task.title}</span>
                    <button type="button" className="text-button danger" disabled={Boolean(taskPendingId)}
                      onClick={() => void remove(task)} aria-label={"Excluir: " + task.title}>Excluir</button>
                  </li>)}
                </ul>
              }
              {total > PAGE_SIZE &&
                <nav className="pagination" aria-label="Paginação das atividades">
                  <button type="button" className="button button-outline" disabled={page <= 1 || loadingTasks}
                    onClick={() => setPage((n) => Math.max(1, n - 1))}>Anterior</button>
                  <span>Página {page} de {pages}</span>
                  <button type="button" className="button button-outline" disabled={page >= pages || loadingTasks}
                    onClick={() => setPage((n) => n + 1)}>Próxima</button>
                </nav>
              }
            </> :
              <div className="empty-state"><strong>Selecione um espaço</strong><p>Para começar, crie seu primeiro workspace acima.</p></div>
            }
          </section>
        </main>
      </div>
    </div>
  );
}
