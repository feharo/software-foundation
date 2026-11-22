import Link from "next/link";

export default function HomePage() {
  return (
    <>
      <a className="skip-link" href="#conteudo">Pular para conteúdo</a>
      <header className="site-header">
        <div className="container header-inner">
          <Link className="brand" href="/" aria-label="__APP_NAME__ - início">
            <span className="brand-mark" aria-hidden="true">S</span>
            <span>__APP_NAME__</span>
          </Link>
          <nav className="header-links" aria-label="Menu principal">
            <a href="#como-funciona">Como funciona</a>
            <Link className="button button-outline button-small" href="/login">Entrar</Link>
          </nav>
        </div>
      </header>
      <main id="conteudo">
        <section className="hero-section">
          <div className="container hero-grid">
            <div className="hero-copy">
              <p className="eyebrow"><span className="eyebrow-dot" /> Seu próximo passo começa aqui</p>
              <h1>Mais clareza para o que <span>faz seu negócio avançar.</span></h1>
              <p className="lead">Organize seus espaços de trabalho e acompanhe atividades em um só lugar, sem complicação.</p>
              <div className="hero-actions">
                <Link href="/login" className="button button-primary">Começar agora <span aria-hidden="true">→</span></Link>
                <a className="button button-ghost" href="#como-funciona">Conhecer a plataforma</a>
              </div>
              <p className="micro-note">Sem cartão de crédito para explorar a demonstração técnica. A operação requer configuração de conta.</p>
            </div>
            <div className="preview-frame" aria-label="Prévia ilustrativa do painel de atividades">
              <div className="preview-top"><span className="preview-dots" aria-hidden="true"><i/><i/><i/></span><span>Painel de trabalho · Exemplo visual</span></div>
              <div className="preview-body">
                <div className="preview-sidebar"><div className="preview-icon"/><div/><div/><div/></div>
                <div className="preview-content">
                  <div className="preview-title">Seu espaço em ordem</div>
                  <p>Acompanhe as próximas atividades</p>
                  <div className="preview-stats"><div><strong>01</strong><span>Espaços</span></div><div><strong>03</strong><span>Atividades exemplo</span></div></div>
                  <div className="preview-list">
                    <div><span className="preview-check preview-check-active"/><span>Planejar próxima entrega</span><em>Planejado</em></div>
                    <div><span className="preview-check"/><span>Organizar prioridades</span><em>Em andamento</em></div>
                    <div><span className="preview-check"/><span>Revisar resultados</span><em>Pendente</em></div>
                  </div>
                  <small>Prévia estática — sem dados de clientes.</small>
                </div>
              </div>
            </div>
          </div>
        </section>
        <section className="features-section" id="como-funciona" aria-labelledby="features-heading">
          <div className="container">
            <p className="eyebrow">Feito para simplificar</p>
            <h2 id="features-heading">O essencial, sem atrapalhar o seu dia.</h2>
            <div className="feature-grid">
              <article className="feature"><span className="feature-icon" aria-hidden="true">01</span><h3>Uma visão do trabalho</h3><p>Veja e organize as atividades por espaço, com informações claras em cada etapa.</p></article>
              <article className="feature"><span className="feature-icon" aria-hidden="true">02</span><h3>Prioridades no lugar certo</h3><p>Encontre o que precisa com busca, paginação e estados que ajudam a seguir em frente.</p></article>
              <article className="feature"><span className="feature-icon" aria-hidden="true">03</span><h3>Estrutura para evoluir</h3><p>Uma base que pode receber novos módulos conforme seu produto ganha maturidade.</p></article>
            </div>
          </div>
        </section>
        <section className="cta-section">
          <div className="container cta-inner">
            <div><p className="eyebrow">Pronto para testar?</p><h2>Comece por uma operação mais simples.</h2></div>
            <Link href="/login" className="button button-primary button-light">Acessar plataforma <span aria-hidden="true">→</span></Link>
          </div>
        </section>
      </main>
      <footer className="site-footer">
        <div className="container footer-inner"><strong>__APP_NAME__</strong><span>Software em evolução, feito para pessoas.</span></div>
      </footer>
    </>
  );
}
