"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { type FormEvent, useEffect, useState } from "react";
import { getSupabase } from "../../lib/supabase";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [sending, setSending] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");
  const supabase = getSupabase();

  useEffect(() => {
    if (!supabase) return;
    let alive = true;
    void supabase.auth.getUser().then(({ data }) => {
      if (alive && data.user) router.replace("/dashboard");
    });
    return () => { alive = false; };
  }, [router, supabase]);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!supabase || sending) return;
    setError("");
    setSending(true);
    try {
      const { error: authError } = await supabase.auth.signInWithOtp({
        email: email.trim(),
        options: { emailRedirectTo: window.location.origin + "/dashboard" },
      });
      if (authError) throw authError;
      setSent(true);
    } catch (cause) {
      setError(cause instanceof Error ? cause.message : "Não conseguimos enviar o acesso.");
    } finally {
      setSending(false);
    }
  }

  return (
    <main className="center-page" id="conteudo">
      <div className="center-card">
        <Link href="/" className="brand" aria-label="__APP_NAME__ - início">
          <span className="brand-mark" aria-hidden="true">S</span>
          <span>__APP_NAME__</span>
        </Link>
        <p className="eyebrow">Bem-vindo</p>
        <h1>Acesse seu espaço.</h1>
        <p>Entre com seu e-mail. Você receberá um link seguro, sem precisar criar senha.</p>
        {!supabase ? (
          <div className="feedback feedback-error" role="alert">
            O acesso ainda não foi configurado. Defina as variáveis do Supabase em
            <code> .env.local </code> seguindo o README e reinicie o servidor.
          </div>
        ) : sent ? (
          <div className="feedback" role="status">
            Link enviado! Confira sua caixa de entrada e a pasta de spam.
          </div>
        ) : (
          <form className="form-stack" onSubmit={handleSubmit}>
            <label htmlFor="email">E-mail</label>
            <input
              id="email"
              name="email"
              type="email"
              autoComplete="email"
              inputMode="email"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              placeholder="voce@empresa.com"
              maxLength={254}
              required
            />
            <button className="button button-primary full-width" type="submit" disabled={sending || !email.trim()}>
              {sending ? "Enviando link…" : "Receber link de acesso"}
            </button>
          </form>
        )}
        {error && <p className="feedback feedback-error" role="alert">{error}</p>}
        <p className="form-note">O envio de e-mail depende do provedor configurado no Supabase.</p>
        <Link href="/" className="back-link">← Voltar à página inicial</Link>
      </div>
    </main>
  );
}
