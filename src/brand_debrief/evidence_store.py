"""Almacén de fuentes y evidencia para un debrief de marca.

Persiste en dos archivos JSON dentro de research/<brand>/:
  - sources.json   -> registro de documentos/páginas consultados
  - evidence.json  -> afirmaciones puntuales, tipadas y citadas

Responsabilidades clave (ver README para el resto de la arquitectura):
  - Deduplicación de fuentes por URL normalizada (evita volver a registrar
    la misma página dos veces aunque se cite en distintas búsquedas).
  - Deduplicación aproximada de evidencia por similitud de texto, para no
    repetir la misma afirmación con distinta redacción.
  - Verificación estructural mínima: toda evidencia debe apuntar a al
    menos una fuente existente.
"""

from __future__ import annotations

import difflib
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from .models import Source, Evidence, EVIDENCE_TYPES, RELIABILITY_LEVELS


def _normalize_url(url: str) -> str:
    p = urlparse(url.strip())
    path = p.path.rstrip("/")
    return urlunparse((p.scheme.lower(), p.netloc.lower(), path, "", "", ""))


def _short_hash(text: str, n: int = 8) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:n]


class EvidenceStore:
    def __init__(self, brand_dir: Path):
        self.brand_dir = Path(brand_dir)
        self.brand_dir.mkdir(parents=True, exist_ok=True)
        self.sources_path = self.brand_dir / "sources.json"
        self.evidence_path = self.brand_dir / "evidence.json"
        self.sources: dict[str, Source] = {}
        self.evidence: dict[str, Evidence] = {}
        self._load()

    # ---------- persistencia ----------

    def _load(self) -> None:
        if self.sources_path.exists():
            raw = json.loads(self.sources_path.read_text(encoding="utf-8"))
            self.sources = {s["id"]: Source(**s) for s in raw}
        if self.evidence_path.exists():
            raw = json.loads(self.evidence_path.read_text(encoding="utf-8"))
            self.evidence = {e["id"]: Evidence(**e) for e in raw}

    def save(self) -> None:
        self.sources_path.write_text(
            json.dumps([s.to_dict() for s in self.sources.values()], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        self.evidence_path.write_text(
            json.dumps([e.to_dict() for e in self.evidence.values()], ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    # ---------- fuentes ----------

    def add_source(
        self,
        name: str,
        url: str,
        category: str,
        published_date: str | None = None,
        access_status: str = "ok",
        reliability: str = "Media",
        notes: str = "",
    ) -> Source:
        norm = _normalize_url(url)
        for s in self.sources.values():
            if _normalize_url(s.url) == norm:
                return s  # deduplicación por URL normalizada
        sid = f"S{_short_hash(norm)}"
        src = Source(
            id=sid,
            name=name,
            url=url,
            category=category,
            published_date=published_date,
            access_status=access_status,
            reliability=reliability,
            notes=notes,
        )
        self.sources[sid] = src
        return src

    # ---------- evidencia ----------

    def _find_similar_claim(self, claim: str, threshold: float = 0.88) -> Evidence | None:
        for ev in self.evidence.values():
            ratio = difflib.SequenceMatcher(None, claim.lower(), ev.claim.lower()).ratio()
            if ratio >= threshold:
                return ev
        return None

    def add_evidence(
        self,
        claim: str,
        evidence_type: str,
        topic: str,
        source_ids: list[str],
        reliability: str = "Media",
        section_refs: list[str] | None = None,
        notes: str = "",
        allow_duplicate: bool = False,
    ) -> Evidence:
        if evidence_type not in EVIDENCE_TYPES:
            raise ValueError(f"evidence_type debe ser uno de {EVIDENCE_TYPES}")
        if reliability not in RELIABILITY_LEVELS:
            raise ValueError(f"reliability debe ser uno de {RELIABILITY_LEVELS}")
        for sid in source_ids:
            if sid not in self.sources:
                raise ValueError(f"source_id desconocido: {sid} (registra la fuente primero)")

        if not allow_duplicate:
            dup = self._find_similar_claim(claim)
            if dup is not None:
                return dup

        eid = f"E{_short_hash(claim + topic)}"
        ev = Evidence(
            id=eid,
            claim=claim,
            evidence_type=evidence_type,
            topic=topic,
            source_ids=source_ids,
            reliability=reliability,
            section_refs=section_refs or [],
            notes=notes,
        )
        self.evidence[eid] = ev
        return ev

    # ---------- consultas ----------

    def by_topic(self, topic: str) -> list[Evidence]:
        return [e for e in self.evidence.values() if e.topic == topic]

    def by_type(self, evidence_type: str) -> list[Evidence]:
        return [e for e in self.evidence.values() if e.evidence_type == evidence_type]

    def source(self, source_id: str) -> Source:
        return self.sources[source_id]
