"""Detección de información potencialmente contradictoria.

No decide automáticamente "cuál dato es el correcto": agrupa la evidencia
por tema (topic) y señala los casos donde dos afirmaciones del mismo tema
tienen contenido numérico o categórico distinto, o donde una evidencia fue
marcada explícitamente en su campo `contradicts`. La resolución humana
(o del agente, con criterio) queda registrada en `notes`.
"""

from __future__ import annotations

import re
from collections import defaultdict

from .evidence_store import EvidenceStore

_NUM_RE = re.compile(r"\d+[.,]?\d*\s*%?")


def _numbers(text: str) -> list[str]:
    return _NUM_RE.findall(text)


def find_contradictions(store: EvidenceStore) -> list[dict]:
    findings = []

    # 1) contradicciones explícitas
    for ev in store.evidence.values():
        for other_id in ev.contradicts:
            if other_id in store.evidence:
                findings.append(
                    {
                        "type": "explicita",
                        "a": ev.id,
                        "b": other_id,
                        "detail": f"'{ev.claim}' marcada como contradictoria con '{store.evidence[other_id].claim}'",
                    }
                )

    # 2) mismo topic, cifras numéricas distintas -> posible conflicto a revisar
    by_topic: dict[str, list] = defaultdict(list)
    for ev in store.evidence.values():
        by_topic[ev.topic].append(ev)

    for topic, evs in by_topic.items():
        numeric = [(e, _numbers(e.claim)) for e in evs if _numbers(e.claim)]
        if len(numeric) < 2:
            continue
        for i in range(len(numeric)):
            for j in range(i + 1, len(numeric)):
                ev_a, nums_a = numeric[i]
                ev_b, nums_b = numeric[j]
                if set(nums_a) != set(nums_b):
                    findings.append(
                        {
                            "type": "revisar",
                            "a": ev_a.id,
                            "b": ev_b.id,
                            "detail": (
                                f"Mismo tema ('{topic}') con cifras distintas — verificar si describen "
                                f"lo mismo: '{ev_a.claim}' vs '{ev_b.claim}'"
                            ),
                        }
                    )
    return findings


def build_contradictions_section(store: EvidenceStore) -> str:
    findings = find_contradictions(store)
    if not findings:
        return ""
    lines = ["## NOTAS SOBRE INFORMACIÓN POTENCIALMENTE CONTRADICTORIA O A VERIFICAR\n"]
    for f in findings:
        lines.append(f"- ({f['type']}) {f['detail']}")
    return "\n".join(lines)
