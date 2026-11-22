#!/usr/bin/env python3
"""Safely verify a redacted Gitleaks scan without leaking matches into CI logs."""
import argparse
import re
import sys
from pathlib import Path

# Gitleaks writes the count to the terminal, e.g. 'INF 72 commits scanned'.
COMMITS = re.compile(r"\b([0-9]+)\s+commits?\s+scanned\b", re.IGNORECASE)
SCANNER_ERROR = re.compile(r"\bfatal:|\berror=\"stderr is not empty\"|\bERR\s+error=", re.IGNORECASE)


def evaluate(log: str, return_code: int):
    counts = [int(match) for match in COMMITS.findall(log)]
    if not counts or max(counts) == 0:
        return False, "Varredura inconclusiva: Gitleaks não confirmou commits examinados."
    if SCANNER_ERROR.search(log):
        return False, "Gitleaks encontrou um erro interno ou falha de acesso ao Git."
    if return_code == 0:
        return True, f"Histórico examinado: {max(counts)} commits. Nenhum achado pelo detector."
    if return_code == 1:
        return False, (
            f"Gitleaks sinalizou possíveis credenciais no histórico ({max(counts)} commits). "
            "Revise a execução privadamente com --redact=100, revogue as credenciais reais "
            "e revise o histórico antes de publicar."
        )
    return False, f"Gitleaks falhou com código {return_code}. A auditoria NÃO foi concluída."


def main(argv=None):
    parser = argparse.ArgumentParser(description="Confere a conclusão do scanner sem imprimir segredos.")
    parser.add_argument("logfile", help="Arquivo temporário de saída do Gitleaks, não será publicado.")
    parser.add_argument("return_code", type=int)
    args = parser.parse_args(argv)
    try:
        message = Path(args.logfile).read_text(encoding="utf-8", errors="replace")
    except OSError:
        print("Falha ao ler resultado do scanner (nenhum segredo será exibido).", file=sys.stderr)
        return 2
    success, summary = evaluate(message, args.return_code)
    print(("OK: " if success else "BLOQUEIO: ") + summary)
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())
