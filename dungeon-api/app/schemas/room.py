"""Schémas de la salle et du déplacement (palier 2 — FT-5, FT-6)."""

from typing import Literal

from pydantic import BaseModel, Field


class MoveRequest(BaseModel):
    """Corps de POST /heroes/{id}/move. Une direction inconnue renvoie 422."""

    direction: Literal["nord", "sud", "est", "ouest"] = Field(examples=["nord"])


class MonsterRead(BaseModel):
    """Monstre affronté dans la salle (uniquement si un combat est en cours)."""

    nom: str
    pv: int
    pv_max: int
    attaque: int


class RoomRead(BaseModel):
    """Description de la salle où se trouve le héros."""

    id: str
    nom: str
    description: str
    sorties: dict[str, str] = Field(
        description="Direction -> identifiant de la salle atteinte",
        examples=[{"nord": "hall"}],
    )
    monstre: MonsterRead | None = None
