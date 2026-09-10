"""Generación de citas: lista de fuentes por categoría y matriz de evidencia.

Todo se deriva del EvidenceStore, así que el documento final nunca puede
"desincronizarse" de lo que realmente se investigó: si una afirmación no
está en evidence.json, no puede aparecer citada.
"""

from __future__ import annotations

from .evidence_store import EvidenceStore

CATEGORY_LABELS = {
    "alpina": "Alpina",
    "competencia": "Competencia",
    "investigacion_mercado": "Investigación de mercado",
    "institucional": "Fuentes institucionales",
    "secundaria": "Fuentes secundarias",
}


def build_sources_section(store: EvidenceStore) -> str:
    lines = ["## FUENTES\n"]
    for cat_key, label in CATEGORY_LABELS.items():
        srcs = [s for s in store.sources.values() if s.category == cat_key]
        if not srcs:
            continue
        lines.append(f"### {label}\n")
        for s in sorted(srcs, key=lambda x: x.name.lower()):
            status_note = ""
            if s.access_status != "ok":
                status_note = f" _(acceso directo {s.access_status}; información vía búsqueda/indexación)_"
            pub = f", publicado: {s.published_date}" if s.published_date else ""
            lines.append(
                f"- **{s.name}** — {s.url} (consultado: {s.retrieved_date}{pub}, "
                f"confiabilidad: {s.reliability}){status_note}"
            )
        lines.append("")
    return "\n".join(lines)


def build_evidence_matrix(store: EvidenceStore) -> str:
    lines = [
        "## MATRIZ DE EVIDENCIA\n",
        "| # | Afirmación | Tipo | Fuente(s) | URL | Fecha consulta | Confiabilidad |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, ev in enumerate(
        sorted(store.evidence.values(), key=lambda e: (e.evidence_type, e.topic)), start=1
    ):
        src_names = []
        src_urls = []
        dates = []
        for sid in ev.source_ids:
            s = store.source(sid)
            src_names.append(s.name)
            src_urls.append(s.url)
            dates.append(s.retrieved_date)
        lines.append(
            "| {i} | {claim} | {tipo} | {src} | {url} | {fecha} | {conf} |".format(
                i=i,
                claim=ev.claim.replace("|", "/"),
                tipo=ev.evidence_type,
                src="; ".join(src_names),
                url="; ".join(src_urls),
                fecha="; ".join(sorted(set(dates))),
                conf=ev.reliability,
            )
        )
    return "\n".join(lines)


def inline_citation(store: EvidenceStore, evidence_id: str) -> str:
    """Devuelve una marca de cita corta, ej. [E1a2b3c4 | Semana, 2025]."""
    ev = store.evidence[evidence_id]
    names = [store.source(sid).name for sid in ev.source_ids]
    return f"[{ev.evidence_type[:1]} · {', '.join(names)}]"
