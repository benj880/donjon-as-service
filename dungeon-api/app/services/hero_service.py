"""Logique applicative des héros : création, consultation, salle, déplacement."""

from sqlmodel import Session, select

from app.models.hero import Hero
from app.schemas.hero import HeroCreate, HeroRead
from app.schemas.room import MonsterRead, RoomRead
from app.services.dungeon_map import START_ROOM, get_monster_of_room, get_room
from app.services.errors import erreur


def calculer_pv_max(force: int) -> int:
    """PV max = 20 + force × 2.

    Palier 3 : ce calcul deviendra la propriété pv_max de la classe métier Heros (app/domain).
    """
    return 20 + force * 2


def to_hero_read(hero: Hero) -> HeroRead:
    """Convertit le héros stocké en réponse API (masque monstre_pv)."""
    return HeroRead(
        id=hero.id,
        nom=hero.nom,
        classe=hero.classe,
        force=hero.force,
        agilite=hero.agilite,
        intelligence=hero.intelligence,
        pv=hero.pv,
        pv_max=hero.pv_max,
        salle_actuelle=hero.salle_actuelle,
        or_=hero.or_,
        victoire=hero.victoire,
        en_combat=hero.monstre_pv is not None,
        est_vivant=hero.pv > 0,
    )


# ---------- Palier 1 : héros ----------

def create_hero(session: Session, data: HeroCreate) -> Hero:
    """Crée un héros dans la salle de départ, PV au maximum."""
    pv_max = calculer_pv_max(data.force)
    hero = Hero(
        **data.model_dump(),
        pv=pv_max,
        pv_max=pv_max,
        salle_actuelle=START_ROOM,
    )
    session.add(hero)
    session.commit()
    session.refresh(hero)
    return hero


def list_heroes(session: Session) -> list[Hero]:
    return list(session.exec(select(Hero)).all())


def get_hero_or_404(session: Session, hero_id: int) -> Hero:
    hero = session.get(Hero, hero_id)
    if hero is None:
        raise erreur(404, "HERO_NOT_FOUND", f"Aucun héros avec l'identifiant {hero_id}.")
    return hero


# ---------- Palier 2 : donjon ----------

def describe_room(hero: Hero) -> RoomRead:
    """Décrit la salle du héros, avec le monstre si un combat est en cours."""
    room = get_room(hero.salle_actuelle)

    monstre = None
    if hero.monstre_pv is not None:
        modele = get_monster_of_room(hero.salle_actuelle)
        monstre = MonsterRead(
            nom=modele["name"],
            pv=hero.monstre_pv,
            pv_max=modele["hp"],
            attaque=modele["attack"],
        )

    return RoomRead(
        id=hero.salle_actuelle,
        nom=room["name"],
        description=room["description"],
        sorties=room["exits"],
        monstre=monstre,
    )


def move_hero(session: Session, hero: Hero, direction: str) -> RoomRead:
    """Déplace le héros. 400 NO_EXIT si pas de sortie ; combat démarré en salle hantée."""
    # Palier 3 : ajouter ici les vérifications 409 HERO_DEAD et IN_COMBAT.
    room = get_room(hero.salle_actuelle)
    destination = room["exits"].get(direction)
    if destination is None:
        raise erreur(400, "NO_EXIT", f"Il n'y a pas de passage vers le {direction}.")

    hero.salle_actuelle = destination
    # Donjon maudit : le monstre réapparaît avec tous ses PV à chaque entrée
    monstre = get_monster_of_room(destination)
    hero.monstre_pv = monstre["hp"] if monstre is not None else None

    session.add(hero)
    session.commit()
    session.refresh(hero)
    return describe_room(hero)
