"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { type FormEvent, useEffect, useState } from "react";
import { getSupabase } from "../../lib/supabase";

type Workspace = { id: string; name: string };
type Task = { id: string; title: string; done: boolean; created_at: string };
type Phase = "loading" | "ready" | "unconfigured" | "error";

const PAGE_SIZE = 8;

export default function DashboardPage() {
  const router = useRouter();
  const supabase = getSupabase();
  const [phase, setPhase] = useState<Phase>("loading");
  const [userId, setUserId] = useState("");
  const [workspaces, setWorkspaces] = useState<Workspace[]>([]);
  const [workspaceId, setWorkspaceId] = useState("");
  const [workspaceName, setWorkspaceName] = useState("");
  const [creatingWorkspace, setCreatingWorkspace] = useState(false);
  const [taskTitle, setTaskTitle] = useState("");
  const [taskBusy, setTaskBusy] = useState(false);
  const [pendingTaskId, setPendingTaskId] = useState("");
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loadingTasks, setLoadingTasks] = useState(false);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState("");
  const [debouncedSearch, setDebouncedSearch] = useState("");
  const [reloadVersion, setReloadVersion] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!supabase) {
      setPhase("unconfigured");
      return;
    }
    const client = supabase;
    let alive = true;

    async function initialize() {
      try {
        const { data, error: authError } = await client.auth.getUser();
        if (authError || !data.user) {
          if (alive) router.replace("/login");
          return;
        }
        const { data: results, error: dbError } = await client
          .from("workspaces")
          .select("id,name")
          .order("created_at", { ascending: true });

        if (!alive) return;
        if (dbError) throw dbError;
        setUserId(data.user.id);
        const rows = (results || []) as Workspace[];
        setWorkspaces(rows);
        setWorkspaceId(rows[0]?.id ?? "");
        setPhase("ready");
      } catch (cause) {
        if (!alive) return;
        setError(cause instanceof Error ? cause.message : "Não foi possível carregar seus espaços.");
        setPhase("error");
      }
    }

    void initialize();
    const { data } = client.auth.onAuthStateChange((event) => {
      if (event === "SIGNED_OUT") router.replace("/login");
    });
    return () => { alive = false; data.subscription.unsubscribe(); };
  }, [router, supabase]);

  useEffect(() => {
    const timeout = setTimeout(() => setDebouncedSearch(search.trim()), 350);
    return () => clearTimeout(timeout);
  }, [search]);

  useEffect(() => {
    if (!supabase || !workspaceId || phase !== "ready") {
      setTasks([]);
      setTotal(0);
      return;
    }
    const client = supabase;
    let alive = true;

    async function loadTasks() {
      setLoadingTasks(true);
      setError("");
      let query = client
        .from("tasks")
        .select("id,title,done,created_at", { count: "exact" })
        .eq("workspace_id", workspaceId)
        .order("created_at", { ascending: false })
        .range((page - 1) * PAGE_SIZE, page * PAGE_SIZE - 1);

      if (debouncedSearch) {
        query = query.ilike("title", "%" + debouncedSearch.replace(/[%_]/g, "") + "%");
      }
      const { data, count, error: listError } = await query;
      if (!alive) return;
      if (listError) {
        setError(listError.message);
      } else {
        setTasks((data || []) as Task[]);
        setTotal(count ?? 0);
      }
      setLoadingTasks(false);
    }
    void loadTasks();
    return () => { alive = false; };
  }, [supabase, workspaceId, page, debouncedSearch, reloadVersion, phase]);

  async function createWorkspace(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!supabase || !userId || creatingWorkspace || workspaceName.trim().length < 3) return;
    setCreatingWorkspace(true);
    setError("");
    try {
      const { data, error: createError } = await supabase.from("workspaces")
        .insert({ name: workspaceName.trim(), owner_id: userId })
        .select("id,name")
        .single();
      if (createError) throw createError;
      const row = data as Workspace;
      setWorkspaces((current) => [...current, row]);
      setWorkspaceId(row.id);
      setWorkspaceName("");
      setSearch("");
      setDebouncedSearch("");
      setPage(1);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Não conseguimos criar seu espaço.");
    } finally {
      setCreatingWorkspace(false);
    }
  }

  async function addTask(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!supabase || !workspaceId || !userId || taskBusy || !taskTitle.trim()) return;
    setTaskBusy(true);
    setError("");
    try {
      const { error: createError } = await supabase.from("tasks").insert({
        workspace_id: workspaceId,
        created_by: userId,
        title: taskTitle.trim(),
      });
      if (createError) throw createError;
      setTaskTitle("");
      setPage(1);
      setSearch("");
      setDebouncedSearch("");
      setReloadVersion((n) => n + 1);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Não conseguimos criar a atividade.");
    } finally {
      setTaskBusy(false);
    }
  }

  async function toggleTask(task: Task) {
    if (!supabase || !workspaceId || pendingTaskId) return;
    const next = !task.done;
    setPendingTaskId(task.id);
    setError("");
    setTasks((current) => current.map((item) => item.id === task.id ? { ...item, done: next } : item));
    try {
      const { error: updateError } = await supabase.from("tasks").update({ done: next })
        .eq("workspace_id", workspaceId).eq("id", task.id).select("id").single();
      if (updateError) throw updateError;
    } catch (cause) {
      setTasks((current) => current.map((item) => item.id === task.id ? { ...item, done: task.done } : item));
      setError(cause instanceof Error ? cause.message : "Não conseguimos atualizar a atividade.");
    } finally {
      setPendingTaskId("");
    }
  }

  async function removeTask(task: Task) {
    if (!supabase || !workspaceId || pendingTaskId) return;
    if (!window.confirm("Excluir esta atividade? Esta ação não poderá ser desfeita.")) return;
    setPendingTaskId(task.id);
    setError("");
    try {
      const { error: deleteError } = await supabase.from("tasks").delete()
        .eq("workspace_id", workspaceId).eq("id", task.id).select("id").single();
      if (deleteError) throw deleteError;
      if (tasks.length === 1 && page > 1) setPage((n) => n - 1);
      else setReloadVersion((n) => n + 1);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Não conseguimos excluir a atividade.");
    } finally {
      setPendingTaskId("");
    }
  }

  async function logout() {
    if (!supabase) return;
    const { error: logoutError } = await supabase.auth.signOut();
    if (logoutError) setError(logoutError.message);
    else router.replace("/login");
  }

  if (phase === "unconfigured") {
    return (
      <main className="center-page">
        <div className="center-card">
          <p className="eyebrow">Configuração inicial</p>
          <h1>Vamos conectar seu SaaS.</h1>
          <p>Para acessar seu painel, crie um projeto Supabase, execute o arquivo
            <code> supabase/schema.sql </code> e preencha o <code>.env.local</code> seguindo o README.</p>
          <Link className="button button-outline" href="/">Voltar ao início</Link>
        </div>
      </main>
    );
  }

  if (phase === "loading") {
    return (
      <main className="dashboard-shell" aria-label="Carregando painel">
        <div className="dashboard-skeleton"><div className="skeleton skeleton-title" /><div className="skeleton skeleton-line" /><div className="skeleton skeleton-panel" /></div>
      </main>
    );
  }

  if (phase === "error") {
    return (
      <main className="center-page">
        <div className="center-card">
          <h1>Não foi possível abrir seu painel.</h1>
          <p className="feedback feedback-error" role="alert">{error}</p>
          <p>Confirme a migração SQL e as configurações do Supabase.</p>
          <button className="button button-primary" onClick={() => window.location.reload()}>Tentar novamente</button>
        </div>
      </main>
    );
  }

  const activeWorkspace = workspaces.find((item) => item.id === workspaceId);
  const pageCount = Math.max(1, Math.ceil(total / PAGE_SIZE));

  return (
    <div className="dashboard-shell">
      <a className="skip-link" href="#dashboard-content">Pular para o conteúdo</a>
      <header className="dashboard-header">
        <Link className="brand" href="/" aria-label="__APP_NAME__ - início">
          <span className="brand-mark" aria-hidden="true">S</span>
          <span>__APP_NAME__</span>
        </Link>
        <button className="text-button" type="button" onClick={() => void logout()}>Sair</button>
      </header>
      <div className="dashboard-layout">
        <aside className="dashboard-sidebar" aria-label="Sobre seu espaço">
          <section className="sidebar-section">
            <span className="sidebar-badge">Seu espaço</span>
            <h2 style={{ marginTop: 15 }}>{activeWorkspace?.name ?? "Primeiro acesso"}</h2>
            <p>Suas atividades ficam organizadas neste workspace. Somente quem tem permissão acessa os dados.</p>
          </section>
        </aside>
        <main className="dashboard-main" id="dashboard-content">
          <div className="dashboard-intro">
            <div><p className="eyebrow">Painel de trabalho</p><h1>Bem-vindo ao seu painel.</h1><p>Um lugar simples para acompanhar o que importa.</p></div>
          </div>

          {error && <p className="feedback feedback-error" role="alert">{error}</p>}

          <section className="dashboard-card" aria-labelledby="workspace-heading">
            <div className="section-header"><h2 id="workspace-heading">Espaços de trabalho</h2></div>
            <form className="inline-form" onSubmit={createWorkspace}>
              <label className="sr-only" htmlFor="workspace-name">Nome do novo espaço</label>
              <input id="workspace-name" value={workspaceName} onChange={(event) => setWorkspaceName(event.target.value)}
                minLength={3} maxLength={80} placeholder="Ex.: Minha empresa" required />
              <button className="button button-primary" type="submit" disabled={creatingWorkspace || workspaceName.trim().length < 3}>
                {creatingWorkspace ? "Criando…" : "Criar espaço"}
              </button>
            </form>
            {workspaces.length > 0 && (
              <div className="workspace-row">
                <label className="form-label" htmlFor="active-workspace">Espaço atual</label>
                <select id="active-workspace" value={workspaceId} onChange={(event) => {
                  setWorkspaceId(event.target.value);
                  setPage(1);
                }}>
                  {workspaces.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}
                </select>
              </div>
            )}
          </section>

          <section className="dashboard-card" aria-labelledby="tasks-heading">
            <div className="section-header">
              <h2 id="tasks-heading">Atividades</h2>
              {workspaceId && <span className="sidebar-badge">{total} {total === 1 ? "atividade" : "atividades"}</span>}
            </div>
            {!workspaceId ? (
              <div className="empty-state"><strong>Crie seu primeiro espaço</strong><p>Depois você poderá adicionar atividades para acompanhar sua operação.</p></div>
            ) : (
              <>
                <form className="inline-form" onSubmit={addTask}>
                  <label className="sr-only" htmlFor="task-name">Nome da atividade</label>
                  <input id="task-name" value={taskTitle} onChange={(event) => setTaskTitle(event.target.value)}
                    maxLength={160} required placeholder="Qual será a próxima atividade?" />
                  <button className="button button-primary" type="submit" disabled={taskBusy || !taskTitle.trim()}>
                    {taskBusy ? "Adicionando…" : "Adicionar"}
                  </button>
                </form>
                <div style={{ marginTop: 20 }}>
                  <label className="form-label" htmlFor="task-search">Buscar atividades</label>
                  <input id="task-search" type="search" value={search} onChange={(event) => { setSearch(event.target.value); setPage(1); }}
                    placeholder="Pesquisar pelo nome" maxLength={80} />
                </div>
                {loadingTasks ? (
                  <div aria-label="Carregando atividades" aria-busy="true" className="dashboard-skeleton" style={{ width: "100%", margin: "20px 0" }}>
                    <div className="skeleton skeleton-line"/><div className="skeleton skeleton-line"/><div className="skeleton skeleton-line"/>
                  </div>
                ) : tasks.length === 0 ? (
                  <div className="empty-state"><strong>{debouncedSearch ? "Nenhuma atividade encontrada" : "Nenhuma atividade ainda"}</strong><p>{debouncedSearch ? "Tente outra busca." : "Adicione a primeira atividade para começar."}</p></div>
                ) : (
                  <ul className="task-list">
                    {tasks.map((task) => (
                      <li className="task-item" key={task.id}>
                        <input className="task-toggle" type="checkbox" checked={task.done} disabled={Boolean(pendingTaskId)}
                          aria-label={task.done ? "Marcar como pendente: " + task.title : "Concluir: " + task.title}
                          onChange={() => void toggleTask(task)} />
                        <span className={"task-item-title" + (task.done ? " done" : "")}>{task.title}</span>
                        <button className="text-button danger" type="button" disabled={Boolean(pendingTaskId)}
                          aria-label={"Excluir atividade: " + task.title} onClick={() => void removeTask(task)}>Excluir</button>
                      </li>
                    ))}
                  </ul>
                )}
                {total > PAGE_SIZE && (
                  <nav className="pagination" aria-label="Paginação das atividades">
                    <button className="button button-outline" disabled={page === 1 || loadingTasks} onClick={() => setPage((n) => Math.max(1, n - 1))}>Anterior</button>
                    <span>Página {page} de {pageCount}</span>
                    <button className="button button-outline" disabled={page >= pageCount || loadingTasks} onClick={() => setPage((n) => n + 1)}>Próxima</button>
                  </nav>
                )}
              </>
            )}
          </section>
        </main>
      </div>
    </div>
  );
}
