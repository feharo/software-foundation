#!/usr/bin/env python3
"""Create a new SaaS from the versioned Software Foundation blueprint."""
import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BLUEPRINT = ROOT / "blueprints" / "saas-nextjs-supabase"
NAME_LIMIT = 70
SLUG_PATTERN = re.compile(r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*$")
COLOR_PATTERN = re.compile(r"^#[0-9a-fA-F]{6}$")
REPLACE = {"__APP_NAME__", "__APP_SLUG__", "__PRIMARY_COLOR__"}


def valid_name(value):
    value = value.strip()
    if not value or len(value) > NAME_LIMIT or any(ch in value for ch in "\\r\\n\\x00<>"):
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
    return color.lower()


def create(name, output, slug=None, color="#2558cf"):
    name = valid_name(name)
    slug = valid_slug(slug or make_slug(name))
    color = valid_color(color)
    destination = Path(output).expanduser().resolve()
    if destination.exists():
        raise FileExistsError("A pasta de destino já existe; escolha outra para não sobrescrever arquivos.")
    if not BLUEPRINT.is_dir():
        raise FileNotFoundError("Blueprint SaaS não encontrado. Execute a partir do repositório completo.")
    mapping = {"__APP_NAME__": name, "__APP_SLUG__": slug, "__PRIMARY_COLOR__": color}
    paths = [p for p in BLUEPRINT.rglob("*") if p.is_file()]
    destination.mkdir(parents=True)
    try:
        for source in paths:
            target = destination / source.relative_to(BLUEPRINT)
            target.parent.mkdir(parents=True, exist_ok=True)
            data = source.read_text(encoding="utf-8")
            for placeholder, value in mapping.items():
                data = data.replace(placeholder, value)
            if any(placeholder in data for placeholder in REPLACE):
                raise RuntimeError(f"Placeholder não resolvido em {source.name}")
            target.write_text(data, encoding="utf-8")
    except Exception:
        shutil.rmtree(destination)
        raise
    return destination


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inicie um SaaS Next.js + Supabase com práticas de qualidade.")
    parser.add_argument("--name", help="Nome exibido no produto")
    parser.add_argument("--slug", help="Identificador técnico do projeto")
    parser.add_argument("--output", help="Pasta do novo produto")
    parser.add_argument("--primary-color", default="#2558cf", help="Cor principal #RRGGBB")
    parser.add_argument("--non-interactive", action="store_true", help="Não abrir perguntas")
    options = parser.parse_args(argv)
    try:
        if options.non_interactive and not options.name:
            parser.error("--name é obrigatório no modo não interativo")
        name = options.name or input("Como seu SaaS se chamará? ").strip()
        slug = options.slug or make_slug(name)
        output = options.output or str(Path.cwd() / slug)
        if not options.non_interactive:
            user_slug = input(f"Identificador [{slug}]: ").strip()
            slug = user_slug or slug
            user_output = input(f"Pasta [{output}]: ").strip()
            output = user_output or output
        dest = create(name, output, slug, options.primary_color)
        print(f"\nProjeto criado em: {dest}")
        print("\nPróximos passos:")
        print(f"  cd {dest}")
        print("  npm install")
        print("  cp .env.example .env.local")
        print("  npm run dev")
        print("\nA landing funcionará imediatamente. Para login e banco, leia o README.md gerado.")
        return 0
    except (ValueError, FileExistsError, FileNotFoundError, RuntimeError, OSError) as error:
        print(f"Erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
