#!/usr/bin/env python3
"""
SDD-SAAS Kit - Validacao Estrutural do Design Lock
Uso: python Scripts/validate-design-lock.py <caminho-para-design-contract.json> [--artifact <caminho-artifact.html>]
Retorna exit code 0 se as regras estruturais passarem, 1 se houver falhas.

Valida programaticamente as regras 1, 2, 3, 4, 5, 6, 8, 9, 11 e 12 do DESIGN_LOCK_CHECKLIST.md
(integridade referencial do JSON). As regras 7, 10 e 13 exigem julgamento humano/agente e
nao sao verificadas por este script.

Este script roda contra o design-contract.json de um PROJETO (nao existe um arquivo de
exemplo na raiz do kit-fonte).
"""
import json
import sys
import argparse
from pathlib import Path


def load_contract(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def check_screens_reference_valid_user_stories(contract: dict, user_story_ids: set[str]) -> list[str]:
    """Regra 2: toda tela referencia userStoryIds existentes."""
    issues = []
    if not user_story_ids:
        return issues  # sem lista de USs conhecida, pula (informar via --user-stories)
    for screen in contract.get("screens", []):
        for us in screen.get("userStoryIds", []):
            if us not in user_story_ids:
                issues.append(f"  -> tela '{screen.get('id')}' referencia userStoryId inexistente: {us}")
    return issues


def check_every_user_story_has_screen(contract: dict, user_story_ids: set[str]) -> list[str]:
    """Regras 1 e 11: toda US tem >=1 tela que a cobre (gap zero)."""
    issues = []
    if not user_story_ids:
        return issues
    covered = set()
    for screen in contract.get("screens", []):
        covered.update(screen.get("userStoryIds", []))
    for us in sorted(user_story_ids - covered):
        issues.append(f"  -> {us} sem nenhuma tela que a cubra (gap de cobertura)")
    return issues


def check_actions_reference_valid_api_expectations(contract: dict) -> list[str]:
    """Regra 3: toda action aponta apiExpectationIds validos ou e UI-only."""
    issues = []
    api_ids = {a["id"] for a in contract.get("apiExpectations", [])}
    for screen in contract.get("screens", []):
        for action in screen.get("actions", []):
            api_refs = action.get("apiExpectationIds")
            if not api_refs:
                continue  # ausencia = UI-only, permitido
            for api_id in api_refs:
                if api_id not in api_ids:
                    issues.append(
                        f"  -> action '{action.get('id')}' (tela '{screen.get('id')}') "
                        f"referencia apiExpectationId inexistente: {api_id}"
                    )
    return issues


def check_api_expectations_reference_valid_screens_and_actions(contract: dict) -> list[str]:
    """Regra 4: toda apiExpectation referencia screenIds e actionIds existentes."""
    issues = []
    screen_ids = {s["id"] for s in contract.get("screens", [])}
    action_ids = {a["id"] for s in contract.get("screens", []) for a in s.get("actions", [])}
    for api in contract.get("apiExpectations", []):
        for sid in api.get("screenIds", []):
            if sid not in screen_ids:
                issues.append(f"  -> apiExpectation '{api.get('id')}' referencia screenId inexistente: {sid}")
        for aid in api.get("actionIds", []):
            if aid not in action_ids:
                issues.append(f"  -> apiExpectation '{api.get('id')}' referencia actionId inexistente: {aid}")
    return issues


def check_data_requirements_reference_valid_screens(contract: dict) -> list[str]:
    """Regra 5: todo dataRequirement referencia sourceScreenIds existentes."""
    issues = []
    screen_ids = {s["id"] for s in contract.get("screens", [])}
    for dr in contract.get("dataRequirements", []):
        for sid in dr.get("sourceScreenIds", []):
            if sid not in screen_ids:
                issues.append(f"  -> dataRequirement '{dr.get('id')}' referencia sourceScreenId inexistente: {sid}")
    return issues


def check_navigation_targets_valid_screens(contract: dict) -> list[str]:
    """Regra 6: itens de navigation apontam telas existentes."""
    issues = []
    screen_ids = {s["id"] for s in contract.get("screens", [])}
    for nav in contract.get("navigation", {}).get("primary", []):
        target = nav.get("targetScreenId")
        if target not in screen_ids:
            issues.append(f"  -> navigation '{nav.get('id')}' aponta targetScreenId inexistente: {target}")
    return issues


def check_every_screen_has_idle_state(contract: dict) -> list[str]:
    """Regra 8: toda tela tem ao menos o estado 'idle'."""
    issues = []
    for screen in contract.get("screens", []):
        if "idle" not in screen.get("states", []):
            issues.append(f"  -> tela '{screen.get('id')}' nao declara o estado 'idle'")
    return issues


def check_components_list_screens(contract: dict) -> list[str]:
    """Regra 9: componentes listam as telas onde sao usados."""
    issues = []
    for comp in contract.get("components", []):
        if not comp.get("usedInScreenIds"):
            issues.append(f"  -> componente '{comp.get('id')}' nao lista usedInScreenIds")
    return issues


def check_unique_ids(contract: dict) -> list[str]:
    """Regra 12: IDs unicos em screens, components, apiExpectations, dataRequirements."""
    issues = []
    for key in ("screens", "components", "apiExpectations", "dataRequirements"):
        ids = [item["id"] for item in contract.get(key, [])]
        seen = set()
        for id_ in ids:
            if id_ in seen:
                issues.append(f"  -> ID duplicado em '{key}': {id_}")
            seen.add(id_)
    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Valida regras estruturais do Design Lock (SDD-SAAS)")
    parser.add_argument("contract_path", help="Caminho para o design-contract.json do projeto")
    parser.add_argument("--user-stories", nargs="*", default=[], help="Lista de US-xx conhecidas do SPEC (opcional, para regras 1/2/11)")
    args = parser.parse_args()

    contract_path = Path(args.contract_path).resolve()
    if not contract_path.exists():
        print(f"Erro: '{contract_path}' nao encontrado.")
        return 1

    contract = load_contract(contract_path)
    user_story_ids = set(args.user_stories)

    print("SDD-SAAS Kit - Validacao Estrutural do Design Lock")
    print("=" * 50)
    print()

    checks = [
        ("Regra 2 - Telas referenciam userStoryIds existentes", lambda: check_screens_reference_valid_user_stories(contract, user_story_ids)),
        ("Regras 1/11 - Toda US tem >=1 tela (gap zero)", lambda: check_every_user_story_has_screen(contract, user_story_ids)),
        ("Regra 3 - Actions referenciam apiExpectationIds validos ou sao UI-only", lambda: check_actions_reference_valid_api_expectations(contract)),
        ("Regra 4 - apiExpectations referenciam screenIds/actionIds existentes", lambda: check_api_expectations_reference_valid_screens_and_actions(contract)),
        ("Regra 5 - dataRequirements referenciam sourceScreenIds existentes", lambda: check_data_requirements_reference_valid_screens(contract)),
        ("Regra 6 - navigation aponta telas existentes", lambda: check_navigation_targets_valid_screens(contract)),
        ("Regra 8 - Toda tela declara estado 'idle'", lambda: check_every_screen_has_idle_state(contract)),
        ("Regra 9 - Componentes listam usedInScreenIds", lambda: check_components_list_screens(contract)),
        ("Regra 12 - IDs unicos por categoria", lambda: check_unique_ids(contract)),
    ]

    total_issues = 0
    for label, fn in checks:
        issues = fn()
        total_issues += len(issues)
        status = "[OK]" if not issues else "[!] "
        print(f"{status} {label}")
        for issue in issues:
            print(issue)

    print()
    if total_issues:
        print(f"Resultado: {total_issues} problema(s) encontrado(s) -- regras 7, 10 e 13 exigem verificacao manual")
    else:
        print("Resultado: regras estruturais OK -- regras 7, 10 e 13 exigem verificacao manual (Agente Design Lock)")

    return 1 if total_issues else 0


if __name__ == "__main__":
    sys.exit(main())
