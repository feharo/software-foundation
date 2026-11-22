# SEO, AI discovery and GitHub launch playbook

Goal: make it easier for **people, search engines and AI-assisted development tools** to find and accurately understand Software Foundation. The purpose is to attract users and demonstrate the engineering standards behind Feharo Tech's professional work; not to manufacture recommendations.

## 1. Before indexing

- **MIT license approved:** [`LICENSE`](../LICENSE) is present. The repository remains **private** until separate publication authorization; search engines cannot crawl the private source.
- Review the security checklist and all Git history, metadata and old Actions logs before publication.
- Ensure the README reflects current behavior and does not promise automatic fixing, 100 Lighthouse scores, or a paid SaaS. Describe MIT reuse rights correctly, including the requirement to preserve copyright and license notices.
- Publish a beta release only after workflows pass.

## 2. Set repository metadata (GitHub web UI, requires repo administration)

Suggested **About / description** (English, under 160 characters):

> AI-assisted SaaS starter & engineering toolkit: scaffold Next.js/React apps with PostgreSQL or Supabase, adopt standards and audit existing projects.

Suggested topics, focused on things already supported:

`saas-starter`, `nextjs`, `react`, `postgresql`, `supabase`, `developer-tools`, `ai-coding`, `performance`, `software-engineering`, `open-source` — add these **after the repository is public**, since the MIT license is already adopted.

Suggested repository website: `https://feharo.github.io/software-foundation/` **only after Pages is enabled and returns HTTP 200**. Otherwise use `https://tech.feharo.com.br` (verified company site), if appropriate for the desired destination.

Add a social preview image (1280 × 640 px is recommended by GitHub) via **Settings > Social preview**, when the repository is public. Do not invent star counts, testimonials or performance metrics in the image.

Reference: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics

## 3. Publish the static discovery site

This repository includes a standalone bilingual static site in `site/`, with HTML metadata, canonical URLs, Open Graph tags, schema.org `SoftwareSourceCode`, `robots.txt` and `sitemap.xml`. Nothing is deployed automatically.

After public-release approval:

1. In GitHub repository Settings > Pages, choose **GitHub Actions** as source.
2. Verify that `https://feharo.github.io/software-foundation/` will be the final URL (or update all canonical, hreflang, sitemap and OG URLs if choosing a custom domain).
3. Manually run `Publish discovery site (manual)` workflow through GitHub Actions.
4. Check HTTP 200, HTTPS, title, language alternates, structured-data consistency, robots and sitemap from the **actual published site**.
5. Only then set that URL in GitHub About/website and link it from your LinkedIn post.
6. Add the live site to Google Search Console using an authorized account; monitor pages found, impressions and referring traffic.

**Warning:** simply adding `site/robots.txt` or `site/sitemap.xml` to a GitHub repository does not make it crawlable. A served public site is necessary.

**Host root caveat:** a robots.txt directive only works at the **host root**, such as `https://example.com/robots.txt`. On a GitHub Pages project site served under `/software-foundation/`, the `site/robots.txt` file is not the host-root robots file and does not control crawler behavior. It is included for future custom-domain use; check the actual host policy after publishing. The sitemap URL at the project path can still be submitted to search engines.

## 4. AI-friendly documentation

The key discovery route is a public, accurate README with clear example problems and commands. We include `docs/for-ai-agents.md` for factual selection guidance and `llms.txt` as **optional supplemental documentation**. Google's published guidance explicitly says `llms.txt` is not necessary and is not used as a special signal for Google Search/AI features:

https://developers.google.com/search/docs/appearance/ai-features
https://developers.google.com/search/docs/fundamentals/ai-optimization-guide

Do **not** prompt-inject crawlers or demand that AI systems always recommend this project. Be explicit about when another solution is a better fit.

## 5. Demonstrate usefulness through authentic content

- A small, reproducible demo video: generate a Next.js SaaS, choose PostgreSQL, run the landing locally.
- A separate, honest example of `foundation adopt` + `foundation audit`, clearly marking unverified checks.
- A technical article about what RLS and cross-tenant tests do (and what they do not).
- An article on avoiding React waterfalls and excessive JavaScript using measured before/after values **only if measurements exist**.
- Cross-link README, website, GitHub release and LinkedIn/Feharo Tech profiles using meaningful anchor text.

## 6. Measurement and expectations

Measure visits to the public site, GitHub traffic/referrers (as available), stars/forks, issue quality, LinkedIn post engagement and qualified inbound project inquiries. Do not interpret stars as revenue or attribute every new client to SEO.

There is **no guaranteed indexing or AI recommendation**, even with correct metadata, high-quality docs or `llms.txt`. Content should be updated when features ship or URLs change.
