#!/usr/bin/env python3
"""Beginner-friendly checks. This never prints secrets or sends data."""
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def check_command(binary, min_major):
    executable = shutil.which(binary)
    if not executable:
        print(f"[FALTA] {binary}: instale antes de prosseguir")
        return False
    result = subprocess.run([executable, "--version"], capture_output=True, text=True, timeout=8, check=False)
    version = (result.stdout or result.stderr).strip()
    match = re.search(r"([0-9]+)[.]", version)
    if binary == "node" and match and int(match.group(1)) < min_major:
        print(f"[ATUALIZAR] Node.js 22+ necessário (encontrado {version})")
        return False
    print(f"[OK] {binary}: {version}")
    return result.returncode == 0


def main():
    print("Diagnóstico __APP_NAME__")
    ok = check_command("node", 22) and check_command("npm", 0)
    env_path = ROOT / ".env.local"
    if not env_path.exists():
        print("[PENDENTE] .env.local não encontrado; copie .env.example")
    else:
        entries = {}
        for raw_line in env_path.read_text(encoding="utf-8").splitlines():
            if "=" in raw_line and not raw_line.lstrip().startswith("#"):
                key, value = raw_line.split("=", 1)
                entries[key.strip()] = value.strip()
        expected = ["NEXT_PUBLIC_SUPABASE_URL", "NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY"]
        missing = [name for name in expected if not entries.get(name)]
        print("[OK] Variáveis de Supabase preenchidas" if not missing else "[PENDENTE] Configure: " + ", ".join(missing))
        if any("service_role" in entries.get(k, "").lower() or "sb_secret_" in entries.get(k, "") for k in expected):
            print("[PERIGO] Chave privada em variável pública: substitua pela publishable key.")
            ok = False
    if (ROOT / "supabase/schema.sql").is_file():
        print("[OK] Migração SQL disponível (execução remota não verificada)")
    else:
        print("[FALTA] supabase/schema.sql")
        ok = False
    if (ROOT / "node_modules").exists():
        print("[OK] Dependências npm presentes")
    else:
        print("[PENDENTE] Execute npm install")
    print("\nPróximo: npm run dev, depois siga o README para configurar o Supabase.")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
