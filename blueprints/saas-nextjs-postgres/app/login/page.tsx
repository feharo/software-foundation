"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { type FormEvent, useState } from "react";
import { authClient } from "../../lib/auth-client";

export default function LoginPage() {
  const router = useRouter();
  const [mode, setMode] = useState<"login" | "signup">("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busy || password.length < 8 || (mode === "signup" && name.trim().length < 2)) return;
    setBusy(true);
    setError("");
    try {
      const response = mode === "login"
        ? await authClient.signIn.email({ email: email.trim(), password })
        : await authClient.signUp.email({ email: email.trim(), password, name: name.trim() });
      if (response.error) {
        setError(response.error.message || "Não conseguimos autenticar sua conta.");
        return;
      }
      router.push("/dashboard");
      router.refresh();
    } catch {
      setError("Serviço indisponível. Confirme a configuração do banco e tente novamente.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <main className="center-page">
      <div className="center-card">
        <Link href="/" className="brand" aria-label="__APP_NAME__ - início">
          <span className="brand-mark" aria-hidden="true">S</span>
          <span>__APP_NAME__</span>
        </Link>
        <p className="eyebrow">{mode === "login" ? "Bem-vindo de volta" : "Seu primeiro acesso"}</p>
        <h1>{mode === "login" ? "Entre no seu espaço." : "Crie sua conta."}</h1>
        <p>Seu acesso é protegido por sessão no servidor e seus dados ficam no PostgreSQL configurado.</p>
        <form onSubmit={submit} className="form-stack">
          {mode === "signup" && (
            <>
              <label htmlFor="name">Nome</label>
              <input id="name" autoComplete="name" minLength={2} maxLength={80} required
                value={name} onChange={(event) => setName(event.target.value)} placeholder="Seu nome" />
            </>
          )}
          <label htmlFor="email">E-mail</label>
          <input id="email" type="email" autoComplete="email" required maxLength={254}
            value={email} onChange={(event) => setEmail(event.target.value)} placeholder="voce@empresa.com" />
          <label htmlFor="password">Senha</label>
          <input id="password" type="password" minLength={8} maxLength={128} required
            autoComplete={mode === "login" ? "current-password" : "new-password"}
            value={password} onChange={(event) => setPassword(event.target.value)} />
          <button type="submit" disabled={busy || !email.trim() || password.length < 8}
            className="button button-primary full-width">
            {busy ? "Processando…" : mode === "login" ? "Entrar" : "Criar conta"}
          </button>
        </form>
        {error && <p className="feedback feedback-error" role="alert">{error}</p>}
        <button className="text-button" type="button" onClick={() => {
          setMode(mode === "login" ? "signup" : "login");
          setPassword("");
          setError("");
        }}>
          {mode === "login" ? "Ainda não tenho conta" : "Já tenho conta"}
        </button>
        <p className="form-note">Perfil inicial: autenticação por senha. Configure verificação de e-mail e recuperação de conta antes da produção.</p>
        <Link href="/" className="back-link">← Voltar ao início</Link>
      </div>
    </main>
  );
}
