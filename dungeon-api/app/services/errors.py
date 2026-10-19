"""Erreurs métier au format imposé : {"detail": {"error": "...", "message": "..."}}."""

from fastapi import HTTPException


def erreur(status_code: int, code: str, message: str) -> HTTPException:
    """Construit une HTTPException au format imposé par le sujet.

    Utilisation : raise erreur(404, "HERO_NOT_FOUND", "Aucun héros avec l'id 3.")
    """
    return HTTPException(status_code=status_code, detail={"error": code, "message": message})
