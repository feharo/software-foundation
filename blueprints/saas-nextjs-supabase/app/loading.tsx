export default function Loading() {
  return <main className="center-page" aria-busy="true" aria-label="Carregando">
    <div className="center-card">
      <div className="skeleton skeleton-title" />
      <div className="skeleton skeleton-line" style={{ marginTop: 15 }} />
      <div className="skeleton skeleton-panel" style={{ height: 130, marginTop: 20 }} />
    </div>
  </main>;
}
