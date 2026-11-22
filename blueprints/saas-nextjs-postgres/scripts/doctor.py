#!/usr/bin/env python3
"""Check local PostgreSQL profile without printing environment secrets."""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def command(binary):
    executable = shutil.which(binary)
    if not executable:
        print(f"[FALTA] {binary}. Instale antes de continuar.")
        return False
    try:
        result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=8, check=False)
        version = (result.stdout or result.stderr).strip()
        print(f"[OK] {binary}: {version}" if result.returncode == 0 else f"[ERRO] {binary}")
        return result.returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        print(f"[ERRO] Não foi possível executar {binary}")
        return False


def main():
    print("Diagnóstico: __APP_NAME__ / PostgreSQL independente")
    good = command("node") and command("npm")
    env_file = ROOT / ".env.local"
    if not env_file.exists():
        print("[PENDENTE] Copie .env.example para .env.local")
    else:
        values = {}
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                key, value = line.split("=", 1)
                values[key.strip()] = value.strip()
        for name in ("DATABASE_URL", "BETTER_AUTH_URL", "BETTER_AUTH_SECRET"):
            print(f"[OK] {name} preenchido" if values.get(name) else f"[PENDENTE] Configure {name}")
        if values.get("BETTER_AUTH_SECRET") and len(values["BETTER_AUTH_SECRET"]) < 32:
            print("[RISCO] BETTER_AUTH_SECRET deve ter ao menos 32 caracteres")
            good = False
    print("[OK] Migração SQL disponível" if (ROOT / "db/schema.sql").exists() else "[FALTA] db/schema.sql")
    print("Próximo: migração do Better Auth, npm run db:migrate e npm run dev.")
    return 0 if good else 1


if __name__ == "__main__":
    raise SystemExit(main())
