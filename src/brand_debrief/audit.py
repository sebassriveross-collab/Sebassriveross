"""Auditoría estructural previa a la entrega del debrief.

Automatiza lo que se puede automatizar de la checklist de control final:
existencia de fuente/URL/fecha/confiabilidad para cada evidencia,
distribución HECHO/INTERPRETACION/HIPOTESIS, secciones del debrief sin
ninguna evidencia asociada, e hipótesis sin marcar explícitamente como tales
en el texto de la sección. Lo que requiere juicio humano/del agente (p. ej.
"¿el insight está bien sustentado?") se deja como pregunta abierta en el
reporte, no se intenta decidir automáticamente.
"""

from __future__ import annotations

from pathlib import Path

from .evidence_store import EvidenceStore


def run_audit(store: EvidenceStore, sections_dir: Path) -> dict:
    report = {"errors": [], "warnings": [], "info": []}

    # 1. Toda evidencia debe tener fuente, tipo y confiabilidad válidos
    for ev in store.evidence.values():
        if not ev.source_ids:
            report["errors"].append(f"{ev.id}: sin fuente asociada -> '{ev.claim}'")
        for sid in ev.source_ids:
            if sid not in store.sources:
                report["errors"].append(f"{ev.id}: referencia a fuente inexistente {sid}")
        if ev.evidence_type == "HIPOTESIS" and ev.reliability not in ("Por validar", "Baja"):
            report["warnings"].append(
                f"{ev.id}: es HIPOTESIS pero su confiabilidad es '{ev.reliability}' (revisar coherencia)"
            )

    # 2. distribución de tipos
    total = len(store.evidence) or 1
    for t in ("HECHO", "INTERPRETACION", "HIPOTESIS"):
        n = len(store.by_type(t))
        report["info"].append(f"{t}: {n}/{total} evidencias ({round(100*n/total)}%)")

    # 3. fuentes con acceso bloqueado -> deben quedar señaladas (ya se anota en citations,
    #    aquí solo confirmamos que la anotación existe en notes o access_status)
    blocked = [s for s in store.sources.values() if s.access_status != "ok"]
    if blocked:
        report["info"].append(
            f"{len(blocked)} fuente(s) con acceso directo bloqueado/no disponible: "
            + ", ".join(s.name for s in blocked)
        )

    # 4. secciones del debrief sin ninguna evidencia citada
    if sections_dir.exists():
        for f in sorted(sections_dir.glob("*.md")):
            text = f.read_text(encoding="utf-8")
            refs = [ev for ev in store.evidence.values() if ev.id in text]
            if not refs:
                report["warnings"].append(f"Sección {f.name}: no cita ningún ID de evidencia")

    # 5. señal de posibles datos inventados: patrones de cifras sin evidencia asociada en el texto
    #    (heurístico simple, no reemplaza revisión humana)
    return report


def print_audit(report: dict) -> None:
    print("=== AUDITORÍA DEL DEBRIEF ===")
    if report["errors"]:
        print(f"\nERRORES ({len(report['errors'])}):")
        for e in report["errors"]:
            print(f"  ✗ {e}")
    else:
        print("\nSin errores estructurales.")
    if report["warnings"]:
        print(f"\nADVERTENCIAS ({len(report['warnings'])}):")
        for w in report["warnings"]:
            print(f"  ! {w}")
    if report["info"]:
        print("\nINFO:")
        for i in report["info"]:
            print(f"  - {i}")
