export default function Loading() {
  return (
    <main className="dashboard-shell" aria-label="Carregando painel">
      <div className="dashboard-skeleton">
        <div className="skeleton skeleton-title" />
        <div className="skeleton skeleton-line" />
        <div className="skeleton skeleton-panel" />
      </div>
    </main>
  );
}
