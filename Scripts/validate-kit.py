#!/usr/bin/env python3
"""
SDD-SAAS Kit - Validacao de Consistencia Interna
Uso: python Scripts/validate-kit.py [--kit-path <caminho>]
Retorna exit code 0 se tudo OK, 1 se houver erros.

Pre-commit hook (Linux/Mac):
  cp Scripts/validate-kit.py .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
  (ou adicione `python Scripts/validate-kit.py || exit 1` ao hook existente)
"""
import re
import sys
import argparse
from pathlib import Path

# Arquivos gerados pelo kit em cada projeto (nao existem na raiz do kit-fonte)
GENERATED_FILES = {
    "STATE.md", "PROJECT.md", "HANDOFF.md", "KNOWLEDGE.md",
    "GLOSSARY.md", "DISCOVERY.md", "CLAUDE.md",
}


def check_slash_commands(kit: Path) -> tuple[int, int, list[str]]:
    """Check 1: every /command in CLAUDE.md has a matching .md and vice versa."""
    issues = []
    claude_md = kit / "Slash Commands" / "CLAUDE.md"
    commands_dir = kit / "Slash Commands"

    if not claude_md.exists():
        return 0, 0, [f"CLAUDE.md nao encontrado em {commands_dir}"]

    content = claude_md.read_text(encoding="utf-8")
    # Match both `- /command-name` (list items) and `/command-name` in backticks
    documented = set(
        re.findall(r"- /([a-z][a-z0-9-]+)", content) +
        re.findall(r"`/([a-z][a-z0-9-]+)", content)
    )

    existing = {p.stem for p in commands_dir.glob("*.md") if p.name != "CLAUDE.md"}

    for cmd in sorted(documented - existing):
        issues.append(f"  -> /{cmd} documentado no CLAUDE.md mas sem arquivo '{cmd}.md'")
    for cmd in sorted(existing - documented):
        issues.append(f"  -> '{cmd}.md' existe mas nao esta documentado no CLAUDE.md")

    total = len(documented | existing)
    ok = total - len(issues)
    return ok, total, issues


def check_init_skill_files(kit: Path) -> tuple[int, int, list[str]]:
    """Check 2: every kit source file referenced in init-sdd-saas.md exists in the kit root."""
    issues = []
    skill_file = kit / "Skills" / "init-sdd-saas.md"

    if not skill_file.exists():
        return 0, 0, ["Skills/init-sdd-saas.md nao encontrado"]

    content = skill_file.read_text(encoding="utf-8")

    # Match uppercase .md filenames (kit source files, not generated ones)
    referenced = set(re.findall(r"\b([A-Z][A-Z_a-z]+\.md)\b", content))
    # Exclude files that are generated outputs, not kit source files
    kit_source_refs = referenced - GENERATED_FILES

    checked = 0
    for fname in sorted(kit_source_refs):
        checked += 1
        if not (kit / fname).exists():
            issues.append(f"  -> {fname} referenciado em init-sdd-saas.md mas nao encontrado na raiz do kit")

    ok = checked - len(issues)
    return ok, checked, issues


def check_orientacao_references(kit: Path) -> tuple[int, int, list[str]]:
    """Check 3: every uppercase .md kit file mentioned in ORIENTACAO.md exists in the kit."""
    issues = []
    orientacao = kit / "ORIENTACAO.md"

    if not orientacao.exists():
        return 0, 0, ["ORIENTACAO.md nao encontrado"]

    content = orientacao.read_text(encoding="utf-8")

    # Match backtick-wrapped uppercase .md filenames
    referenced = set(re.findall(r"`([A-Z][A-Z_a-z]+\.md)`", content))
    # Exclude project-generated files (they don't live in the kit root)
    kit_source_refs = referenced - GENERATED_FILES

    def exists_anywhere(fname: str) -> bool:
        if (kit / fname).exists():
            return True
        if (kit / "Slash Commands" / fname).exists():
            return True
        return any(kit.rglob(fname))

    checked = 0
    for fname in sorted(kit_source_refs):
        checked += 1
        if not exists_anywhere(fname):
            issues.append(f"  -> {fname} referenciado em ORIENTACAO.md mas nao encontrado no kit")

    ok = checked - len(issues)
    return ok, checked, issues


def check_version_consistency(kit: Path) -> tuple[int, int, list[str]]:
    """Check 4: VERSION, ARCHITECTURE.md and ORIENTACAO.md all reference the same version."""
    issues = []
    checked = 3

    version_file = kit / "VERSION"
    if not version_file.exists():
        return 0, checked, ["  -> Arquivo VERSION nao encontrado na raiz do kit"]

    kit_version = version_file.read_text(encoding="utf-8").strip()

    arch_md = kit / "ARCHITECTURE.md"
    if arch_md.exists():
        if kit_version not in arch_md.read_text(encoding="utf-8"):
            issues.append(f"  -> ARCHITECTURE.md nao menciona a versao {kit_version}")
    else:
        issues.append("  -> ARCHITECTURE.md nao encontrado")

    orientacao = kit / "ORIENTACAO.md"
    if orientacao.exists():
        if kit_version not in orientacao.read_text(encoding="utf-8"):
            issues.append(f"  -> ORIENTACAO.md nao menciona a versao {kit_version}")
    else:
        issues.append("  -> ORIENTACAO.md nao encontrado")

    ok = checked - len(issues)
    return ok, checked, issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida consistencia interna do SDD-SAAS Kit")
    parser.add_argument("--kit-path", default=".", help="Caminho para a raiz do kit (padrao: diretorio atual)")
    args = parser.parse_args()

    kit = Path(args.kit_path).resolve()
    if not (kit / "ARCHITECTURE.md").exists():
        print(f"Erro: '{kit}' nao parece ser a raiz do SDD-SAAS Kit (ARCHITECTURE.md nao encontrado).")
        return 1

    print("SDD-SAAS Kit - Validacao de Consistencia Interna")
    print("=" * 50)
    print()

    results = []
    total_issues = 0

    checks = [
        ("Check 1 - Slash commands (CLAUDE.md <-> arquivos .md)", check_slash_commands),
        ("Check 2 - Arquivos de referencia do init-sdd-saas", check_init_skill_files),
        ("Check 3 - Referencias de arquivos do kit em ORIENTACAO.md", check_orientacao_references),
        ("Check 4 - Consistencia de versao (VERSION / ARCHITECTURE.md / ORIENTACAO.md)", check_version_consistency),
    ]

    for label, fn in checks:
        ok, total, issues = fn(kit)
        total_issues += len(issues)
        status = "[OK]" if not issues else "[!] "
        print(f"{status} {label}: {ok}/{total} OK")
        for issue in issues:
            print(issue)
        results.append((label, ok, total, issues))

    print()
    ok_checks = sum(1 for _, _, _, issues in results if not issues)
    print(f"Resultado: {ok_checks}/{len(checks)} checks OK", end="")
    if total_issues:
        print(f" -- {total_issues} problema(s) encontrado(s)")
    else:
        print(" -- kit consistente")

    return 1 if total_issues else 0


if __name__ == "__main__":
    sys.exit(main())
