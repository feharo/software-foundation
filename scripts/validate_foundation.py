#!/usr/bin/env python3
"""Validate the foundation catalog and profiles. No third-party dependencies."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_LEVELS = {"required", "conditional", "advisory"}
ALLOWED_STATUS = {"pass", "fail", "not_applicable", "not_verified"}


def validate(root=ROOT):
    data = json.loads((root / "standards/performance.json").read_text(encoding="utf-8"))
    rules = data["rules"]
    ids = [rule["id"] for rule in rules]
    assert len(rules) == 31, f"Expected 31 rules; found {len(rules)}"
    assert ids == [f"P{i:03d}" for i in range(1, 32)], "Rules must have P001..P031 in order"
    assert len(set(ids)) == 31, "Duplicated ID"
    for rule in rules:
        for key in ("id", "title", "category", "level", "applies_when", "guidance", "evidence"):
            assert isinstance(rule.get(key), str) and rule[key].strip(), f"Missing {key}: {rule}"
        assert rule["level"] in ALLOWED_LEVELS
    for path in (root / "profiles").glob("*.json"):
        profile = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(profile.get("stack"), list) and profile["stack"], str(path)
        for key in ("recommend", "conditional"):
            assert len(profile[key]) == len(set(profile[key])), f"Duplicate in {path}:{key}"
            assert set(profile[key]).issubset(ids), f"Unknown IDs in {path}:{key}"
        assert not set(profile["recommend"]).intersection(profile["conditional"]), f"Overlap in {path}"
    example = json.loads((root / "schemas/audit-report.example.json").read_text(encoding="utf-8"))
    for result in example["results"]:
        assert result["id"] in ids and result["status"] in ALLOWED_STATUS
        assert isinstance(result.get("evidence"), list)
        if result["status"] == "not_applicable":
            assert result.get("reason"), "Exception requires reason"
    skill = (root / "skills/performance-guardian/SKILL.md").read_text(encoding="utf-8")
    assert skill.startswith("---\nname: performance-guardian\n")
    assert "description:" in skill.split("---", 2)[1]
    assert (root / "skills/performance-guardian/agents/openai.yaml").is_file()
    assert (root / "templates/AGENTS.md").is_file()
    print(f"OK: {len(rules)} rules; {len(list((root / 'profiles').glob('*.json')))} profiles; skill and examples valid")
    return True


if __name__ == "__main__":
    validate()
