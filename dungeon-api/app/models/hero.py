"""Table des héros (palier 2 — FT-4 : persistance SQLite avec SQLModel)."""

from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    """Héros tel qu'il est stocké en base.

    Ce modèle n'est jamais renvoyé directement par l'API : on passe par HeroRead,
    qui masque monstre_pv (et owner_id au palier 4).
    """

    id: int | None = Field(default=None, primary_key=True)
    nom: str
    classe: str
    force: int
    agilite: int
    intelligence: int
    pv: int
    pv_max: int
    salle_actuelle: str
    or_: int = 0
    # None = aucun combat en cours ; sinon PV restants du monstre de la salle
    monstre_pv: int | None = None
    victoire: bool = False
    # Palier 4 : owner_id (clé étrangère vers le joueur) sera ajouté ici.
