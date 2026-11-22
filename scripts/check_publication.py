#!/usr/bin/env python3
"""Check tracked checkout files for common publication blockers without printing secrets.

This is deliberately NOT a replacement for historical secret scanning or manual review.
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 1_000_000
SAFE_ENV = {".env.example", ".env.sample", ".env.template"}
SENSITIVE_FILES = {"id_rsa", "id_dsa", "id_ed25519", ".npmrc", ".pypirc", "credentials.json", "service-account.json"}
TOKEN_PATTERNS = (
    ("private_key", re.compile(r"-----BEGIN (?:[A-Z ]+ )?PRIVATE KEY-----")),
    ("github_token", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b")),
    ("cloud_secret", re.compile(r"\b(?:sb_secret_[A-Za-z0-9]{24,}|sk_live_[A-Za-z0-9]{20,})\b")),
    ("aws_key", re.compile(r"\bAKIA[A-Z0-9]{16}\b")),
)


def tracked_paths(root=ROOT):
    try:
        outcome = subprocess.run(
            ["git", "-C", str(root), "ls-files", "-z"], check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20,
        )
    except (FileNotFoundError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
        raise ValueError("git ls-files indisponível: a verificação exige um checkout Git") from error
    return [Path(v.decode("utf-8", errors="replace")) for v in outcome.stdout.split(b"\x00") if v]


def scan_files(root, files):
    issues = []
    for rel in files:
        name = rel.name.lower()
        path = root / rel
        if path.is_symlink():
            issues.append((str(rel), "symlink_requires_review"))
            continue
        if not path.is_file():
            continue
        if name in SENSITIVE_FILES or (name.startswith(".env") and name not in SAFE_ENV):
            issues.append((str(rel), "sensitive_filename"))
        if path.stat().st_size > MAX_BYTES:
            issues.append((str(rel), "large_file_manual_review"))
            continue
        try:
            content = path.read_bytes()
        except OSError:
            issues.append((str(rel), "unreadable"))
            continue
        if b"\x00" in content:
            continue
        text = content.decode("utf-8", errors="replace")
        for key, pattern in TOKEN_PATTERNS:
            if pattern.search(text):
                issues.append((str(rel), key))
    return issues


def check(root=ROOT, strict=False, paths=None):
    root = Path(root).resolve()
    issues = scan_files(root, paths if paths is not None else tracked_paths(root))
    for filename, problem in issues:
        print("BLOQUEIO: " + filename + ": " + problem)
    required = ("README.md", "SECURITY.md", "CONTRIBUTING.md")
    for filename in required:
        if not (root / filename).is_file():
            issues.append((filename, "missing_community_file"))
            print("BLOQUEIO: " + filename + " ausente")
    if not (root / "LICENSE").is_file():
        message = "LICENSE ausente: escolher licença antes de tornar o repositório público."
        if strict:
            issues.append(("LICENSE", "license_not_approved"))
            print("BLOQUEIO: " + message)
        else:
            print("PENDENTE (não bloqueia CI privado): " + message)
    if issues:
        print(f"Falhou: {len(issues)} problema(s). O scanner NÃO examina histórico Git.")
        return False
    print("OK: verificação de checkout concluída. Histórico Git e logs exigem auditoria separada.")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Verifique o checkout antes de abrir o repositório.")
    parser.add_argument("--strict", action="store_true", help="Exigir licença além da checagem de segredos.")
    args = parser.parse_args(argv)
    try:
        return 0 if check(strict=args.strict) else 1
    except (ValueError, OSError) as error:
        print("Erro: " + str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
