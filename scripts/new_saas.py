#!/usr/bin/env python3
"""Create a new SaaS from the versioned Software Foundation blueprint."""
import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "blueprints" / "saas-nextjs-supabase"
POSTGRES_OVERLAY = ROOT / "blueprints" / "saas-nextjs-postgres"
DATABASES = {"supabase", "postgres"}
POSTGRES_EXCLUDE = {"lib/supabase.ts"}
NAME_LIMIT = 70
SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")
REPLACE = {"__APP_NAME__", "__APP_SLUG__", "__PRIMARY_COLOR__"}
EXTRA_FILES = {
    "standards/performance.json": ".foundation/standards/performance.json",
    "docs/frontend-playbook.md": ".foundation/docs/frontend-playbook.md",
    "templates/AGENTS.md": "AGENTS.md",
    "templates/CLAUDE.md": "CLAUDE.md",
    # MIT attribution for starter-origin code, without licensing user additions.
    "LICENSE": "LICENSE-SOFTWARE-FOUNDATION",
}


def valid_name(value):
    value = value.strip()
    if not value or len(value) > NAME_LIMIT or not re.fullmatch(r"[\w .,&-]+", value, re.UNICODE):
        raise ValueError("Nome inválido (1-70 caracteres, sem quebras de linha ou < >).")
    return value


def make_slug(name):
    import unicodedata
    normalized = unicodedata.normalize("NFKD", name)
    ascii_name = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    if not slug or not slug[0].isalpha():
        slug = "app-" + slug
    return slug[:40].rstrip("-")


def valid_slug(slug):
    if not 3 <= len(slug) <= 40 or not SLUG_PATTERN.fullmatch(slug):
        raise ValueError("Slug inválido: use 3-40 caracteres, letras minúsculas, números e hífens.")
    return slug


def valid_color(color):
    if not COLOR_PATTERN.fullmatch(color):
        raise ValueError("Cor inválida: use hexadecimal de 6 dígitos como #2558CF.")
    channels = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    luminance = 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]
    if 1.05 / (luminance + 0.05) < 4.5:
        raise ValueError("Escolha uma cor principal mais escura (contraste mínimo 4.5:1 com texto branco).")
    return color.lower()


def create(name, output, slug=None, color="#2558cf", database="supabase"):
    name = valid_name(name)
    slug = valid_slug(slug or make_slug(name))
    color = valid_color(color)
    if database not in DATABASES:
        raise ValueError("Banco inválido: use supabase ou postgres.")
    destination = Path(output).expanduser().resolve()
    if destination.exists():
        raise FileExistsError("A pasta de destino já existe; escolha outra para não sobrescrever arquivos.")
    if not BLUEPRINT.is_dir():
        raise FileNotFoundError("Blueprint SaaS não encontrado. Execute a partir do repositório completo.")
    mapping = {"__APP_NAME__": name, "__APP_SLUG__": slug, "__PRIMARY_COLOR__": color}
    paths = {p.relative_to(BLUEPRINT): p for p in BLUEPRINT.rglob("*") if p.is_file()}
    if database == "postgres":
        if not POSTGRES_OVERLAY.is_dir():
            raise FileNotFoundError("Overlay PostgreSQL não encontrado.")
        # Exclude all Supabase-only files, including local CLI config and migrations.
        for relative in list(paths):
            if relative.parts[0] == "supabase" or relative.as_posix() in POSTGRES_EXCLUDE:
                paths.pop(relative, None)
        paths.update({p.relative_to(POSTGRES_OVERLAY): p for p in POSTGRES_OVERLAY.rglob("*") if p.is_file()})
    destination.mkdir(parents=True)
    try:
        for relative, source in sorted(paths.items()):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            data = source.read_text(encoding="utf-8")
            for placeholder, value in mapping.items():
                data = data.replace(placeholder, value)
            if any(placeholder in data for placeholder in REPLACE):
                raise RuntimeError(f"Placeholder não resolvido em {source.name}")
            target.write_text(data, encoding="utf-8")
        profile = ROOT / "profiles" / f"nextjs-{database}.json"
        profile_target = destination / ".foundation" / "profile.json"
        profile_target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(profile, profile_target)
        manifest_target = destination / ".foundation" / "manifest.json"
        manifest_content = {
            "schema_version": 1,
            "foundation_version": (ROOT / "VERSION").read_text(encoding="utf-8").strip(),
            "profile": f"nextjs-{database}",
            "catalog_sha256": hashlib.sha256((ROOT / "standards/performance.json").read_bytes()).hexdigest(),
        }
        manifest_target.write_text(json.dumps(manifest_content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        for source_path, target_path in EXTRA_FILES.items():
            source = ROOT / source_path
            target = destination / target_path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
        if database == "supabase":
            # Reuse the same SQL baseline for hosted SQL Editor and local CLI migrations.
            # No separate, stale copy of the RLS policies is maintained.
            migration_dir = destination / "supabase" / "migrations"
            migration_dir.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(destination / "supabase" / "schema.sql",
                            migration_dir / "20261122000000_initial.sql")
    except Exception:
        shutil.rmtree(destination)
        raise
    return destination


def setup_copy_command(platform_name=None):
    """Show commands a new user can actually run on the current OS."""
    os_name = platform_name if platform_name is not None else sys.platform
    return "Copy-Item .env.example .env.local" if os_name == "win32" else "cp .env.example .env.local"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inicie um SaaS com Supabase ou PostgreSQL independente.")
    parser.add_argument("--name", help="Nome exibido no produto")
    parser.add_argument("--slug", help="Identificador técnico do projeto")
    parser.add_argument("--output", help="Pasta do novo produto")
    parser.add_argument("--database", "--db", choices=sorted(DATABASES), default=None,
                        help="Banco/autenticação: supabase ou postgres (sem Supabase)")
    parser.add_argument("--primary-color", default="#2558cf", help="Cor principal #RRGGBB")
    parser.add_argument("--non-interactive", action="store_true", help="Não abrir perguntas")
    options = parser.parse_args(argv)
    try:
        if options.non_interactive and not options.name:
            parser.error("--name é obrigatório no modo não interativo")
        name = options.name or input("Como seu SaaS se chamará? ").strip()
        slug = options.slug or make_slug(name)
        output = options.output or str(Path.cwd() / slug)
        database = options.database
        if not options.non_interactive and database is None:
            print("Infraestrutura de dados:")
            print("  1) Supabase — serviço gerenciado de banco + autenticação")
            print("  2) PostgreSQL independente — VPS, Docker ou banco gerenciado; Better Auth")
            choice = input("Escolha [1]: ").strip()
            if choice not in ("", "1", "2"):
                raise ValueError("Opção inválida; escolha 1 ou 2.")
            database = "postgres" if choice == "2" else "supabase"
        database = database or "supabase"
        if not options.non_interactive:
            user_slug = input(f"Identificador [{slug}]: ").strip()
            slug = user_slug or slug
            user_output = input(f"Pasta [{output}]: ").strip()
            output = user_output or output
        dest = create(name, output, slug, options.primary_color, database=database)
        print(f"\nProjeto criado em: {dest}")
        print("\nPróximos passos:")
        print(f"  cd {dest}")
        print("  npm install")
        print("  " + setup_copy_command())
        print("  npm run dev")
        print("\nA landing funcionará imediatamente. Para login e banco, leia o README.md gerado.")
        return 0
    except (ValueError, FileExistsError, FileNotFoundError, RuntimeError, OSError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
