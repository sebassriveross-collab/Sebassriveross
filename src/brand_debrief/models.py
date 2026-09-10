"""Estructuras de datos del sistema de investigación de marca.

Todo el pipeline gira alrededor de dos objetos:

- Source: un documento/página consultado (con su estado de acceso).
- Evidence: una afirmación puntual extraída de una o varias Source,
  clasificada como HECHO / INTERPRETACION / HIPOTESIS y con nivel de
  confiabilidad. El resto del sistema (citas, matriz de evidencia,
  auditoría, documento final) se construye leyendo estos registros.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional

EVIDENCE_TYPES = ("HECHO", "INTERPRETACION", "HIPOTESIS")
RELIABILITY_LEVELS = ("Alta", "Media", "Baja", "Por validar")

SOURCE_CATEGORIES = (
    "alpina",
    "competencia",
    "investigacion_mercado",
    "institucional",
    "secundaria",
)


@dataclass
class Source:
    id: str
    name: str
    url: str
    category: str  # ver SOURCE_CATEGORIES
    published_date: Optional[str] = None  # fecha de publicación si se conoce
    retrieved_date: str = field(default_factory=lambda: date.today().isoformat())
    access_status: str = "ok"  # ok | blocked | js_required | paywalled
    reliability: str = "Media"
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Evidence:
    id: str
    claim: str
    evidence_type: str  # HECHO | INTERPRETACION | HIPOTESIS
    topic: str  # ej: "producto_alpin", "target", "mercado", "competencia_milo"
    source_ids: list[str]
    reliability: str = "Media"
    contradicts: list[str] = field(default_factory=list)
    section_refs: list[str] = field(default_factory=list)
    notes: str = ""

    def to_dict(self) -> dict:
        return asdict(self)
