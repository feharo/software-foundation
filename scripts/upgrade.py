#!/usr/bin/env python3
"""Safe, hash-aware upgrade of only Software Foundation managed catalog metadata."""
import hashlib
import json
import os
import shutil
import tempfile
from pathlib import Path

from scripts import foundation

MANIFEST = ".foundation/manifest.json"
CATALOG = ".foundation/standards/performance.json"


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def upgrade(project, apply=False):
    root = Path(project).expanduser().resolve()
    foundation.check_project(root)
    expected = foundation.CATALOG.read_bytes()
    new_hash = sha256(expected)
    old_manifest = root / MANIFEST
    installed = root / CATALOG

    for target in (old_manifest, installed):
        if target.is_symlink() or not target.resolve().is_relative_to(root):
            raise ValueError("Arquivo gerenciado fora do projeto ou symlink; operação bloqueada: " + str(target))
        if not target.is_file():
            raise ValueError("Fundação não instalada. Use 'foundation adopt PATH --apply' antes de atualizar.")

    current = foundation.load_json(old_manifest)
    if not isinstance(current, dict) or current.get("schema_version") != 1:
        raise ValueError("Manifesto inválido ou não suportado. Não alterar arquivos manualmente.")
    old_bytes = installed.read_bytes()
    observed_hash = sha256(old_bytes)
    expected_hash = current.get("catalog_sha256")
    if not isinstance(expected_hash, str) or len(expected_hash) != 64:
        raise ValueError("Manifesto sem hash válido; interrompendo por segurança.")

    status = "up_to_date"
    message = "O catálogo local já corresponde à versão da fundação."
    if observed_hash != expected_hash:
        status = "conflict"
        message = "O catálogo local foi alterado após a adoção. Preserve as mudanças e revise um diff manual antes do upgrade."
    elif observed_hash != new_hash or current.get("foundation_version") != foundation.VERSION:
        status = "update_available"
        message = "Catálogo gerenciado pronto para atualização. Código e configurações do SaaS permanecem intactos."
    result = {
        "project": str(root),
        "status": status,
        "installed_version": str(current.get("foundation_version", "unknown")),
        "available_version": foundation.VERSION,
        "old_sha256": observed_hash,
        "new_sha256": new_hash,
        "message": message,
        "applied": False,
    }
    if not apply or status != "update_available":
        return result

    # Back up both files before touching them. No overwrites of user backup.
    backup_dir = root / ".foundation" / "backups" / ("pre-upgrade-" + observed_hash[:12])
    if backup_dir.exists():
        raise ValueError("Backup da revisão já existe; revise antes de executar novamente.")
    backup_dir.mkdir(parents=True)
    shutil.copy2(old_manifest, backup_dir / "manifest.json")
    shutil.copy2(installed, backup_dir / "performance.json")

    updated = dict(current)
    updated["foundation_version"] = foundation.VERSION
    updated["catalog_sha256"] = new_hash
    new_manifest = (json.dumps(updated, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

    # Replace with files in the same directory; restore both if the second write fails.
    try:
        _atomic_write(installed, expected)
        _atomic_write(old_manifest, new_manifest)
    except OSError:
        shutil.copy2(backup_dir / "performance.json", installed)
        shutil.copy2(backup_dir / "manifest.json", old_manifest)
        raise

    result["status"] = "updated"
    result["applied"] = True
    result["backup"] = str(backup_dir.relative_to(root))
    result["message"] = "Catálogo atualizado com backup preservado; aplicações, banco e dependências não foram alterados."
    return result


def _atomic_write(path, data):
    fd, temp = tempfile.mkstemp(prefix=".foundation-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)
