"use client";

import { useEffect } from "react";

export default function ErrorPage({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Substitute sanitized tracing in production. No personal data is logged.
    if (process.env.NODE_ENV === "development") console.error("Page error", error);
  }, [error]);

  return (
    <main className="center-page">
      <div className="center-card" role="alert">
        <p className="eyebrow">Algo não saiu como esperado</p>
        <h1>Não conseguimos carregar esta página.</h1>
        <p>Você pode tentar novamente. Se o problema continuar, procure o suporte.</p>
        <button className="button button-primary" onClick={reset}>Tentar novamente</button>
      </div>
    </main>
  );
}
