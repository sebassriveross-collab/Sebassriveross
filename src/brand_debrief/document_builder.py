"""Ensambla el documento final del debrief a partir de:

  1. La estructura genérica de secciones (config/debrief_structure.yaml).
  2. El contenido narrativo de cada sección, escrito por quien investiga
     en research/<brand>/sections/<NN>_<slug>.md (texto con citas inline
     del tipo [E1a2b3c4]).
  3. Las secciones generadas automáticamente desde el EvidenceStore:
     notas de contradicción, matriz de evidencia y fuentes.

Esto separa el contenido (redacción/análisis, que requiere criterio) de la
trazabilidad (qué respalda cada afirmación, que se deriva mecánicamente del
store) y es lo que permite auditar el documento antes de entregarlo.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from .evidence_store import EvidenceStore
from .citations import build_sources_section, build_evidence_matrix
from .contradictions import build_contradictions_section


def load_structure(structure_path: Path) -> list[dict]:
    data = yaml.safe_load(structure_path.read_text(encoding="utf-8"))
    return data["sections"]


def build_document(
    brand_config: dict,
    structure_path: Path,
    sections_dir: Path,
    store: EvidenceStore,
) -> str:
    structure = load_structure(structure_path)

    title = f"DEBRIEF — {brand_config['product'].upper()} ({brand_config['brand'].upper()})"
    subtitle = f"Mercado: {brand_config['country']} · Categoría: {brand_config['category']}"
    parts = [f"# {title}\n\n_{subtitle}_\n"]

    missing_sections = []
    for sec in structure:
        sec_id = sec["id"]
        slug = sec["slug"]
        fname = sections_dir / f"{sec_id:02d}_{slug}.md"
        parts.append(f"\n## {sec_id}. {sec['title'].upper()}\n")
        if fname.exists():
            parts.append(fname.read_text(encoding="utf-8").strip())
        else:
            missing_sections.append(fname.name)
            parts.append(
                "_[Sección pendiente: no se encontró contenido investigado para este apartado.]_"
            )

    contradictions_md = build_contradictions_section(store)
    if contradictions_md:
        parts.append("\n" + contradictions_md)

    parts.append("\n" + build_evidence_matrix(store))
    parts.append("\n" + build_sources_section(store))

    if missing_sections:
        parts.append(
            "\n---\n_Nota de generación: faltó contenido para: "
            + ", ".join(missing_sections)
            + "_"
        )

    return "\n".join(parts)
