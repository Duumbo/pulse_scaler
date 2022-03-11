#!/usr/bin/env python
# -*- coding-UFT-8 -*-
"""Regroups all the necessary utils for the extrapolations."""
from typing import cast
import numpy as np

FloatList = list[float] | np.ndarray[float, np.dtype[np.float64]]


def lin_extr(
        points: np.ndarray[float, np.dtype[np.float64]],
        scale: np.ndarray[float, np.dtype[np.float64]]) -> float:
    """Linear extrapolator."""
    if len(points) != len(scale):
        raise ValueError("Incorrect length of points.")
    zne_expval: float = np.polyfit(scale, points, 1)[-1]
    return zne_expval


def epsilon(
        epsilon_0: FloatList,
        epsilon_m1: FloatList | None = None,
        normal_expval: float | None = None) -> float:
    """
    # Algorithme epsilon.

    Retourne la valeur à laquelle une série converge. Le paramètre
    epsilon_m1 est pour garder en mémoire la série précédente et
    n'est pas nécessaire à définir pour l'utilisation usuelle de la fonction.
    Param: epsilon_0: Série initiale à faire converger.
    Param: epsilon_m1: Série précédente à l'itération actuelle.
    Param: normal_expval: Valeur de l'itération initiale, do not set.
    Retour: float: valeur à laquelle la série converge.
    """
    if epsilon_m1 is None:  # S'il s'agit de la première itération.
        epsilon_m1 = [0 for _ in epsilon_0]
        normal_expval = epsilon_0[0]
    if len(epsilon_0) <= 1:  # Briser la récursivité.
        normal_expval = cast(float, normal_expval)
        epsilon_0 = cast(list[float], epsilon_0)
        return (float(epsilon_0) + normal_expval) / 2
    # Initiallise le tableau de la nouvelle série.
    epsilon_1: np.ndarray[float, np.dtype[np.float64]] = np.array([])

    # Itère une fois de moins que le nombre d'éléments
    for i in range(len(epsilon_0) - 1):
        # Génère la nouvelle série
        delta = epsilon_0[i + 1] - epsilon_0[i]
        epsilon_1 = np.append(epsilon_1, epsilon_m1[i + 1] + (1.0 / delta))

    # Faire un itération de epsilon avec la nouvelle série obtenue.
    return epsilon(epsilon_1, epsilon_0, normal_expval)


def rich_extr(points: list[float], scale: list[int]) -> float:
    """Richardson extrapolator."""
    order = len(points) - 1
    zne_expval: float = np.polyfit(scale, points, deg=order)[-1]
    return zne_expval


def poly_extr(points: list[float], scale: list[int], order: int = 2) -> float:
    """Polynomial extrapolator."""
    raise NotImplementedError
