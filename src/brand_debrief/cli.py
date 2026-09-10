"""CLI del sistema de debrief de marca.

Uso típico (ver README.md para la guía completa):

    python -m brand_debrief add-source --brand alpin --name "Alpina - Ficha Alpin Chocolate" \\
        --url https://alpina.com/alpin-chocolate-caja-200-ml --category alpina --reliability Alta

    python -m brand_debrief add-evidence --brand alpin \\
        --claim "Alpin Chocolate se vende en caja de 200 ml, sixpack de 200 ml y botella de 300 ml" \\
        --type HECHO --topic producto_alpin --sources S1a2b3c4 --reliability Alta

    python -m brand_debrief audit --brand alpin
    python -m brand_debrief build --brand alpin

Este CLI es genérico: cambiando --brand y el archivo config/brands/<brand>.yaml
se reutiliza para cualquier otra marca/producto/país.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

from .evidence_store import EvidenceStore
from .audit import run_audit, print_audit
from .document_builder import build_document

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "config"
RESEARCH_DIR = ROOT / "research"
OUTPUT_DIR = ROOT / "output"


def _brand_config(brand: str) -> dict:
    path = CONFIG_DIR / "brands" / f"{brand}.yaml"
    if not path.exists():
        sys.exit(f"No existe configuración para la marca '{brand}' en {path}")
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def cmd_add_source(args):
    store = EvidenceStore(RESEARCH_DIR / args.brand)
    src = store.add_source(
        name=args.name,
        url=args.url,
        category=args.category,
        published_date=args.published_date,
        access_status=args.access_status,
        reliability=args.reliability,
        notes=args.notes or "",
    )
    store.save()
    print(f"Fuente registrada: {src.id} -> {src.name}")


def cmd_add_evidence(args):
    store = EvidenceStore(RESEARCH_DIR / args.brand)
    ev = store.add_evidence(
        claim=args.claim,
        evidence_type=args.type,
        topic=args.topic,
        source_ids=args.sources.split(","),
        reliability=args.reliability,
        notes=args.notes or "",
    )
    store.save()
    print(f"Evidencia registrada: {ev.id} -> {ev.claim}")


def cmd_list(args):
    store = EvidenceStore(RESEARCH_DIR / args.brand)
    if args.what in ("sources", "all"):
        print(f"\n--- Fuentes ({len(store.sources)}) ---")
        for s in store.sources.values():
            print(f"{s.id} [{s.category}/{s.reliability}/{s.access_status}] {s.name} -> {s.url}")
    if args.what in ("evidence", "all"):
        print(f"\n--- Evidencia ({len(store.evidence)}) ---")
        for e in store.evidence.values():
            print(f"{e.id} [{e.evidence_type}/{e.topic}] {e.claim}")


def cmd_audit(args):
    store = EvidenceStore(RESEARCH_DIR / args.brand)
    report = run_audit(store, RESEARCH_DIR / args.brand / "sections")
    print_audit(report)
    if report["errors"]:
        sys.exit(1)


def cmd_build(args):
    brand_cfg = _brand_config(args.brand)
    store = EvidenceStore(RESEARCH_DIR / args.brand)
    structure_path = CONFIG_DIR / brand_cfg.get("structure_file", "debrief_structure.yaml")
    sections_dir = RESEARCH_DIR / args.brand / "sections"
    doc = build_document(brand_cfg, structure_path, sections_dir, store)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUTPUT_DIR / f"{args.brand}_debrief.md"
    out_path.write_text(doc, encoding="utf-8")
    print(f"Debrief generado en: {out_path}")


def main():
    parser = argparse.ArgumentParser(prog="brand_debrief")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add-source")
    p.add_argument("--brand", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--url", required=True)
    p.add_argument("--category", required=True, choices=[
        "alpina", "competencia", "investigacion_mercado", "institucional", "secundaria"
    ])
    p.add_argument("--published-date", default=None)
    p.add_argument("--access-status", default="ok", choices=["ok", "blocked", "js_required", "paywalled"])
    p.add_argument("--reliability", default="Media", choices=["Alta", "Media", "Baja", "Por validar"])
    p.add_argument("--notes", default="")
    p.set_defaults(func=cmd_add_source)

    p = sub.add_parser("add-evidence")
    p.add_argument("--brand", required=True)
    p.add_argument("--claim", required=True)
    p.add_argument("--type", required=True, choices=["HECHO", "INTERPRETACION", "HIPOTESIS"])
    p.add_argument("--topic", required=True)
    p.add_argument("--sources", required=True, help="IDs de fuente separados por coma")
    p.add_argument("--reliability", default="Media", choices=["Alta", "Media", "Baja", "Por validar"])
    p.add_argument("--notes", default="")
    p.set_defaults(func=cmd_add_evidence)

    p = sub.add_parser("list")
    p.add_argument("--brand", required=True)
    p.add_argument("--what", default="all", choices=["sources", "evidence", "all"])
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("audit")
    p.add_argument("--brand", required=True)
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("build")
    p.add_argument("--brand", required=True)
    p.set_defaults(func=cmd_build)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
