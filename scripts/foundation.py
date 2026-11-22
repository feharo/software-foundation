#!/usr/bin/env python3
"""Single, dependency-free entrypoint for Software Foundation."""
import argparse
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
CATALOG = ROOT / "standards" / "performance.json"
PROFILES = ROOT / "profiles"
FRONTEND_TECH = {"nextjs", "react", "vue", "angular", "svelte"}
SKIP_DIRS = {".git", "node_modules", ".next", "dist", "build", "coverage", ".venv", "venv", ".turbo"}
PROFILE_NAMES = {p.stem for p in PROFILES.glob("*.json")}


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return None


def package_data(project):
    obj = load_json(project / "package.json")
    return obj if isinstance(obj, dict) else {}


def detect(project):
    """Inspect conventional manifests; never read private environment values."""
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError("Diretório do projeto não encontrado: " + str(project))
    pkg = package_data(project)
    deps = set()
    for key in ("dependencies", "devDependencies"):
        if isinstance(pkg.get(key), dict):
            deps.update(pkg[key])
    tech = set()
    if "next" in deps:
        tech.update({"nextjs", "react"})
    if "react" in deps:
        tech.add("react")
    if "@nestjs/core" in deps:
        tech.add("nestjs")
    if "express" in deps or "fastify" in deps or "@nestjs/core" in deps:
        tech.add("node-api")
    if "@supabase/supabase-js" in deps or "@supabase/ssr" in deps:
        tech.add("supabase")
    if "pg" in deps or "postgres" in deps or "postgresql" in deps:
        tech.add("postgres")
    if "better-auth" in deps:
        tech.add("better-auth")
    if "prisma" in deps or "@prisma/client" in deps:
        tech.add("orm")
        schema = project / "prisma" / "schema.prisma"
        if schema.is_file() and schema.stat().st_size < 200_000:
            if "postgresql" in schema.read_text(encoding="utf-8", errors="replace"):
                tech.add("postgres")
    if "drizzle-orm" in deps:
        tech.add("orm")
    if "vue" in deps:
        tech.add("vue")
    if "@angular/core" in deps:
        tech.add("angular")
    if "svelte" in deps or "@sveltejs/kit" in deps:
        tech.add("svelte")
    if (project / "pyproject.toml").is_file() or (project / "requirements.txt").is_file():
        tech.add("python")
    if (project / "go.mod").is_file():
        tech.add("go")
    if (project / "Cargo.toml").is_file():
        tech.add("rust")
    if (project / "supabase" / "config.toml").is_file() or (project / "supabase" / "schema.sql").is_file():
        tech.add("supabase")
    if (project / "docker-compose.yml").is_file() or (project / "compose.yaml").is_file():
        tech.add("docker")
    if (project / "db" / "schema.sql").is_file():
        tech.add("sql")
    if (project / "app" / "api").is_dir() or (project / "pages" / "api").is_dir():
        tech.add("api")
    return {"path": project, "tech": sorted(tech), "package": pkg}


def suggested_profile(detected):
    tech = set(detected["tech"])
    if "nextjs" in tech and "nestjs" in tech:
        return "nextjs-nestjs"
    if "nextjs" in tech and "supabase" in tech:
        return "nextjs-supabase"
    if "nextjs" in tech and "postgres" in tech:
        return "nextjs-postgres"
    if "nextjs" in tech:
        return "nextjs-generic"
    if "react" in tech or "vue" in tech or "angular" in tech or "svelte" in tech:
        return "react-spa"
    if tech.intersection({"nestjs", "node-api", "python", "go", "rust", "api"}):
        return "api-service"
    return "generic"


def check_project(project):
    result = detect(project)
    path = result["path"]
    has_source = any((path / key).exists() for key in (
        "package.json", "pyproject.toml", "requirements.txt", "go.mod", "Cargo.toml",
        "src", "app", "pages", "main.py", "README.md"
    ))
    if not has_source:
        raise ValueError("A pasta não parece conter um projeto. Selecione a raiz do código.")
    return result


def manifest(profile):
    return {
        "schema_version": 1,
        "foundation_version": VERSION,
        "profile": profile,
        "catalog_sha256": hashlib.sha256(CATALOG.read_bytes()).hexdigest(),
    }


def adoption_plan(project, profile=None):
    discovered = check_project(project)
    target = discovered["path"]
    chosen = profile or suggested_profile(discovered)
    if chosen not in PROFILE_NAMES:
        raise ValueError("Perfil desconhecido: " + chosen + ". Veja profiles/.")
    content = {
        ".foundation/manifest.json": json.dumps(manifest(chosen), ensure_ascii=False, indent=2) + "\n",
        ".foundation/profile.json": (PROFILES / (chosen + ".json")).read_text(encoding="utf-8"),
        ".foundation/standards/performance.json": CATALOG.read_text(encoding="utf-8"),
        ".foundation/docs/frontend-playbook.md": (ROOT / "docs/frontend-playbook.md").read_text(encoding="utf-8"),
        ".foundation/agent-guide.md": (ROOT / "templates/AGENTS.md").read_text(encoding="utf-8"),
        "AGENTS.md": (ROOT / "templates/AGENTS.md").read_text(encoding="utf-8"),
        "CLAUDE.md": (ROOT / "templates/CLAUDE.md").read_text(encoding="utf-8"),
    }
    plan = {"project": str(target), "profile": chosen, "detected": discovered["tech"],
            "create": [], "identical": [], "preserve": [], "conflict": []}
    for relative, text in content.items():
        path = target / relative
        if not path.parent.resolve().is_relative_to(target):
            plan["conflict"].append(relative + " (caminho indireto fora do projeto)")
            continue
        if path.is_symlink():
            plan["conflict"].append(relative + " (link simbólico não é alterado)")
            continue
        if not path.exists():
            plan["create"].append(relative)
        elif path.is_file() and path.read_text(encoding="utf-8", errors="replace") == text:
            plan["identical"].append(relative)
        elif relative in ("AGENTS.md", "CLAUDE.md"):
            plan["preserve"].append(relative)
        else:
            plan["conflict"].append(relative + " (arquivo existente diferente; não sobrescrever)")
    return plan, content


def adopt(project, profile=None, apply=False):
    plan, content = adoption_plan(project, profile)
    if not apply:
        return plan
    if plan["conflict"]:
        raise ValueError("Adoção interrompida antes de escrever. Conflitos: " + "; ".join(plan["conflict"]))
    root = Path(plan["project"])
    for relative in plan["create"]:
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        # Exclusive creation: refuse to overwrite if another process created the file.
        with target.open("x", encoding="utf-8") as stream:
            stream.write(content[relative])
    plan["applied"] = True
    return plan


def static_checks(project, detected):
    pkg = detected["package"]
    scripts = pkg.get("scripts") if isinstance(pkg.get("scripts"), dict) else {}
    tech = set(detected["tech"])
    checks = []
    def add(key, status, evidence, action):
        checks.append({"id": key, "status": status, "evidence": evidence, "recommendation": action})

    workflows = list((project / ".github" / "workflows").glob("*.yml")) + list((project / ".github" / "workflows").glob("*.yaml"))
    add("ci_present", "present" if workflows else "missing",
        [str(path.relative_to(project)) for path in workflows[:8]],
        "Adicionar CI que execute build, testes e verificações de segurança.")
    test_dirs = ("tests", "__tests__", "test", "e2e")
    tests_found = [name for name in test_dirs if (project / name).is_dir()]
    if not tests_found:
        for folder in ("src", "app", "components"):
            base = project / folder
            if not base.is_dir():
                continue
            matches = [p for p in base.rglob("*") if p.is_file() and
                       p.name.endswith((".test.ts", ".test.tsx", ".spec.ts", ".spec.tsx", ".test.js", ".spec.js"))
                       and not any(parent in SKIP_DIRS for parent in p.relative_to(project).parts)]
            if matches:
                tests_found = [str(p.relative_to(project)) for p in matches[:5]]
                break
    add("tests_present", "present" if tests_found else "missing", tests_found,
        "Adicionar testes automatizados da jornada principal, casos de erro e autorização.")
    if (project / "package.json").is_file():
        lockfiles = [name for name in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lock", "bun.lockb") if (project / name).is_file()]
        add("lockfile_present", "present" if lockfiles else "missing", lockfiles,
            "Fixar dependências usando o lockfile do gerenciador escolhido.")
        add("build_script", "present" if "build" in scripts else "missing",
            ["package.json: scripts.build"] if "build" in scripts else [],
            "Definir um script de build reproduzível no package.json.")
        add("test_script", "present" if "test" in scripts else "missing",
            ["package.json: scripts.test"] if "test" in scripts else [],
            "Adicionar comando de teste automatizado (ou documentar alternativa no CI).")
    else:
        for id in ("lockfile_present", "build_script", "test_script"):
            add(id, "not_applicable", [], "Não é um projeto Node identificado.")
    tsconfig = load_json(project / "tsconfig.json")
    if "nextjs" in tech or "react" in tech:
        strict = isinstance(tsconfig, dict) and tsconfig.get("compilerOptions", {}).get("strict") is True
        add("typescript_strict", "present" if strict else "not_verified",
            ["tsconfig.json: compilerOptions.strict"] if strict else [],
            "Verificar TypeScript strict e manter checagem de tipos no CI.")
    else:
        add("typescript_strict", "not_applicable", [], "Não foi identificada uma aplicação React/Next.")
    ignore = project / ".gitignore"
    ignore_text = ignore.read_text(encoding="utf-8", errors="replace") if ignore.is_file() else ""
    patterns = {line.strip() for line in ignore_text.splitlines() if line.strip() and not line.lstrip().startswith("#")}
    protected = ".env" in patterns or ".env*" in patterns or ".env.*" in patterns
    add("env_gitignore", "present" if protected else "missing",
        [".gitignore"] if protected else [], "Ignorar arquivos de ambiente com credenciais no Git; não copiar segredos.")
    add("tenant_isolation", "not_verified", [],
        "Testar com pelo menos dois usuários/tenants: leitura, alteração e exclusão cruzada.")
    return checks


def audit(project):
    detected = check_project(project)
    root = detected["path"]
    profile = suggested_profile(detected)
    existing_manifest = load_json(root / ".foundation" / "manifest.json")
    if isinstance(existing_manifest, dict) and existing_manifest.get("profile") in PROFILE_NAMES:
        profile = existing_manifest["profile"]
    rules = load_json(CATALOG)["rules"]
    has_ui = bool(set(detected["tech"]).intersection(FRONTEND_TECH))
    result_rules = []
    for rule in rules:
        reason = "Requer teste ou medida em execução real; inspeção estática não comprova conformidade."
        status = "not_verified"
        if not has_ui and rule["category"] in ("frontend", "assets"):
            status = "not_applicable"
            reason = "Nenhuma interface web detectada nesta análise; reavaliar se houver UI externa."
        result_rules.append({"id": rule["id"], "title": rule["title"], "level": rule["level"],
                             "category": rule["category"], "status": status,
                             "reason": reason, "evidence": [],
                             "expected_evidence": rule["evidence"]})
    checks = static_checks(root, detected)
    return {
        "schema_version": 1, "project": root.name, "profile": profile,
        "detected_stack": detected["tech"], "inspection": "static_only",
        "summary": {
            "rules_not_verified": sum(r["status"] == "not_verified" for r in result_rules),
            "rules_not_applicable": sum(r["status"] == "not_applicable" for r in result_rules),
            "static_checks_missing": sum(c["status"] == "missing" for c in checks),
        },
        "checks": checks, "results": result_rules,
        "limitations": [
            "Inspeção estática não mediu latência, Core Web Vitals, segurança efetiva ou isolamento entre tenants.",
            "Presence of a workflow or test file does not mean that it passes.",
            "Nenhum código ou configuração foi alterado por esta auditoria.",
        ],
    }


def markdown_report(report):
    s = report["summary"]
    lines = ["# Auditoria estática — " + report["project"], "",
             "Perfil sugerido: `" + report["profile"] + "`",
             "Stack detectada: " + (", ".join(report["detected_stack"]) or "não identificada"), "",
             "Regras não verificadas: " + str(s["rules_not_verified"]) +
             " | Não aplicáveis: " + str(s["rules_not_applicable"]) +
             " | Checks estruturais ausentes: " + str(s["static_checks_missing"]), "",
             "## Verificações estruturais", "",
             "| Check | Estado | Próximo passo |", "|---|---|---|"]
    for c in report["checks"]:
        lines.append("| " + c["id"] + " | " + c["status"] + " | " + c["recommendation"].replace("|", "/") + " |")
    lines += ["", "## Catálogo de performance", "",
              "Cada regra requer evidência real antes de ser declarada conforme.", "",
              "| Regra | Estado | Evidência esperada |", "|---|---|---|"]
    for r in report["results"]:
        lines.append("| " + r["id"] + " — " + r["title"] + " | " + r["status"] +
                     " | " + r["expected_evidence"].replace("|", "/") + " |")
    lines += ["", "## Limitações", ""]
    lines += ["- " + line for line in report["limitations"]]
    return "\n".join(lines) + "\n"


def show_adoption(plan):
    print("Projeto: " + plan["project"])
    print("Perfil: " + plan["profile"])
    print("Stack: " + (", ".join(plan["detected"]) or "desconhecida"))
    for title, key in (("Criar", "create"), ("Já idênticos", "identical"),
                       ("Preservados", "preserve"), ("Conflitos", "conflict")):
        print(title + ": " + (", ".join(plan[key]) if plan[key] else "nenhum"))
    if plan.get("applied"):
        print("Padrões instalados. Código e arquivos existentes não foram sobrescritos.")
    else:
        print("Modo de prévia: nenhum arquivo foi alterado. Use --apply para instalar os padrões.")


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if argv and argv[0] == "init":
        from scripts import new_saas
        return new_saas.main(argv[1:])

    parser = argparse.ArgumentParser(prog="foundation", description="Dois caminhos, um sistema: criar ou evoluir software.")
    cmd = parser.add_subparsers(dest="command", required=True)
    cmd.add_parser("init", help="Gerar um SaaS novo (Supabase ou PostgreSQL).")
    ad = cmd.add_parser("adopt", help="Integrar padrões ao projeto existente sem sobrescrever código.")
    ad.add_argument("path", nargs="?", default=".")
    ad.add_argument("--profile", choices=sorted(PROFILE_NAMES))
    ad.add_argument("--apply", action="store_true", help="Criar somente arquivos novos, após verificar conflitos.")
    ad.add_argument("--json", action="store_true", help="Exibir plano JSON.")
    au = cmd.add_parser("audit", help="Auditoria estática das 31 regras e checks estruturais; sem mutações.")
    au.add_argument("path", nargs="?", default=".")
    au.add_argument("--format", choices=("text", "json", "markdown"), default="text")
    au.add_argument("--output", help="Salvar relatório, sem sobrescrever arquivos existentes.")
    doc = cmd.add_parser("doctor", help="Verificar ferramentas locais, sem conexões externas.")
    doc.add_argument("path", nargs="?", default=".")
    up = cmd.add_parser("upgrade", help="Comparar e atualizar o catálogo gerenciado sem tocar no código.")
    up.add_argument("path", nargs="?", default=".")
    up.add_argument("--apply", action="store_true", help="Aplicar só após validar hashes, com backup local.")
    up.add_argument("--json", action="store_true", help="Exibir estado em JSON.")
    args = parser.parse_args(argv)
    try:
        if args.command == "adopt":
            plan = adopt(args.path, profile=args.profile, apply=args.apply)
            if args.json:
                print(json.dumps(plan, ensure_ascii=False, indent=2))
            else:
                show_adoption(plan)
            return 0
        if args.command == "audit":
            report = audit(args.path)
            if args.format == "json":
                output = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
            elif args.format == "markdown":
                output = markdown_report(report)
            else:
                output = markdown_report(report)
            if args.output:
                target = Path(args.output).expanduser().resolve()
                if target.exists():
                    raise ValueError("O relatório já existe. Escolha novo caminho; não sobrescrever.")
                target.parent.mkdir(parents=True, exist_ok=True)
                with target.open("x", encoding="utf-8") as stream:
                    stream.write(output)
                print("Relatório gravado: " + str(target))
            else:
                print(output, end="")
            return 0
        if args.command == "upgrade":
            from scripts import upgrade as updater
            result = updater.upgrade(args.path, apply=args.apply)
            if args.json:
                print(json.dumps(result, ensure_ascii=False, indent=2))
            else:
                print("Projeto: " + result["project"])
                print("Estado: " + result["status"])
                print("Origem: " + result["installed_version"] +
                      " | Fundação atual: " + result["available_version"])
                print(result["message"])
            return 2 if result["status"] == "conflict" else 0
        if args.command == "doctor":
            discovered = check_project(args.path)
            print("Foundation " + VERSION + " — Diagnóstico local")
            print("Projeto: " + str(discovered["path"]))
            print("Perfil sugerido: " + suggested_profile(discovered))
            print("Python: " + sys.version.split()[0])
            if any(k in discovered["tech"] for k in ("react", "nextjs", "nestjs", "node-api")):
                for command in ("node", "npm"):
                    print(command + ": " + ("disponível" if shutil.which(command) else "não encontrado"))
            print("Banco, autenticação, testes e deploy reais NÃO verificados.")
            return 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("Erro: " + str(error), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
