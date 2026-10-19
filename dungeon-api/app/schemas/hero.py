"""Schémas d'entrée / sortie des héros (palier 1 — FT-1, FT-2, FT-3)."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator


class HeroCreate(BaseModel):
    """Corps de POST /heroes. Toute la validation est faite ici (erreur 422 sinon)."""

    nom: str = Field(min_length=3, max_length=20, examples=["Aragorn"])
    classe: Literal["guerrier", "mage", "voleur"]
    force: int = Field(ge=1, le=8, examples=[6])
    agilite: int = Field(ge=1, le=8, examples=[2])
    intelligence: int = Field(ge=1, le=8, examples=[2])

    @model_validator(mode="after")
    def verifier_somme_stats(self) -> "HeroCreate":
        total = self.force + self.agilite + self.intelligence
        if total != 10:
            raise ValueError(
                f"La somme force + agilite + intelligence doit valoir 10 (actuellement {total})."
            )
        return self


class HeroRead(BaseModel):
    """Réponse renvoyée pour un héros : monstre_pv est remplacé par en_combat / est_vivant."""

    id: int
    nom: str
    classe: str
    force: int
    agilite: int
    intelligence: int
    pv: int
    pv_max: int
    salle_actuelle: str
    or_: int
    victoire: bool
    en_combat: bool
    est_vivant: bool
