"""Routes /heroes : uniquement la couche HTTP, la logique est dans hero_service."""

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from app.database import get_session
from app.schemas.hero import HeroCreate, HeroRead
from app.schemas.room import MoveRequest, RoomRead
from app.services import hero_service

router = APIRouter(prefix="/heroes", tags=["Héros"])


@router.post("", response_model=HeroRead, status_code=status.HTTP_201_CREATED)
def create_hero(data: HeroCreate, session: Session = Depends(get_session)):
    """Crée un héros dans la salle de départ avec ses PV au maximum."""
    hero = hero_service.create_hero(session, data)
    return hero_service.to_hero_read(hero)


@router.get("", response_model=list[HeroRead])
def list_heroes(session: Session = Depends(get_session)):
    """Liste tous les héros."""
    return [hero_service.to_hero_read(h) for h in hero_service.list_heroes(session)]


@router.get("/{hero_id}", response_model=HeroRead)
def get_hero(hero_id: int, session: Session = Depends(get_session)):
    """Consulte un héros (404 HERO_NOT_FOUND si inconnu)."""
    hero = hero_service.get_hero_or_404(session, hero_id)
    return hero_service.to_hero_read(hero)


@router.get("/{hero_id}/room", response_model=RoomRead, tags=["Donjon"])
def get_room(hero_id: int, session: Session = Depends(get_session)):
    """Décrit la salle où se trouve le héros."""
    hero = hero_service.get_hero_or_404(session, hero_id)
    return hero_service.describe_room(hero)


@router.post("/{hero_id}/move", response_model=RoomRead, tags=["Donjon"])
def move_hero(hero_id: int, data: MoveRequest, session: Session = Depends(get_session)):
    """Déplace le héros dans une direction et renvoie la nouvelle salle."""
    hero = hero_service.get_hero_or_404(session, hero_id)
    return hero_service.move_hero(session, hero, data.direction)
