import Link from "next/link";

export default function NotFound() {
  return (
    <main className="center-page">
      <div className="center-card">
        <p className="eyebrow">Erro 404</p>
        <h1>Não encontramos esta página.</h1>
        <p>Verifique o endereço ou volte para o início.</p>
        <Link className="button button-primary" href="/">Voltar ao início</Link>
      </div>
    </main>
  );
}
