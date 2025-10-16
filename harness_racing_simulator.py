#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulateur de trot attelé, il s'agit d'une course de 12 à 20 chevaux, faisant l'objet d'un tiercé, quarté, quinte, elle
se déroule sur un hippodrome rectiligne de 2400m.
"""

import random
from math import floor

# Le dictionnaire contenant les evolutions de la vitesse d'un cheval
SPEED_CHART: dict = {
    0: (0, 1, 1, 1, 2, 2),
    1: (0, 0, 1, 1, 1, 2),
    2: (0, 0, 0, 1, 1, 2),
    3: (-1, 0, 0, 0, 1, 1),
    4: (-1, -1, 0, 0, 0, 1),
    5: (-2, -1, 0, 0, 0, 1),
    6: (-2, -1, 0, 0, 0, None),
}
# Le tableau des distances parcourues selon le jet de dé
DISTANCE_CHART = [0, 23, 46, 69, 92, 115, 138]


# ----------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions utilitaires -----------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


def cross_multiplication(a, b, c):
    """
    Fait un produit en croix et renvoie le résultat arrondi à l’inférieur ("floor").
    Sert ici à convertir une distance (en m) vers une échelle d’affichage (en caractères).

    :param a:
    :param b:
    :param c:
    :return:
    """
    return floor((b * c) / a)


def change_speed(speed, die_roll):
    """
    Renvoie la variation de vitesse (peut être négative, nulle, positive ou None) en consultant le tableau SPEED_CHART
     selon la vitesse actuelle et le résultat d’un dé à six faces.
    :param speed:
    :param die_roll:
    :return:
    """
    return SPEED_CHART[speed][die_roll - 1]


def roll_die(die_size):
    """
    Simule un lancer de dé à die_size faces et renvoie une valeur entière uniforme entre 1 et die_size
    :param die_size: nombre de faces
    :return:
    """
    return random.randrange(1, die_size + 1)


def next_turn():
    """
    Met la simulation en pause jusqu’à ce que l’utilisateur appuie sur Entrée (permet d’avancer tour par tour).
    :return:
    """
    input("Appuyez sur entrée pour avancer la course")


# ----------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions de contrôles d'entrées utilisateur  -----------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


def ask_int_in_range(prompt, min_val, max_val):
    """
    Valide l'entrée utilisateur, retire les espaces, s'assure qu'il s'agit bien d'un nombre et qu'il se situe
    entre la valeur minimale et la valeur maximale
    :param prompt:
    :param min_val:
    :param max_val:
    :return:
    """
    while True:
        txt = input(prompt).strip()
        if txt.isdigit():
            val = int(txt)
            if min_val <= val <= max_val:
                return val
        print(f"Valeur invalide. Entrez un entier entre {min_val} et {max_val}.")


def ask_horse_race_type():
    """
    Demande à l’utilisateur le type de course ("tierce", "quarte", "quinte").
    Repose la question tant que l’entrée n’est pas valide. Renvoie la chaîne choisie.
    :return:
    """
    race_type = input("Quel type de course ? (tierce,quarte,quinte) : ")
    if race_type == "quinte" or race_type == "quarte" or race_type == "tierce":
        return race_type
    else:
        print("merci de rentrer un des termes suivants: 'quinte','quarte','tierce'")
        return ask_horse_race_type()


# ----------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions principales de jeu   --------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


def start_game_graphical(horses, race_type):
    """
    Lance la simulation graphique (ASCII) d’une course de trot attelé sur 2400 m.
    À chaque tour (10 s simulées) : met à jour la vitesse selon un jet de dé, avance chaque cheval, gère disqualifications et arrivées, affiche une barre avec la position (♘).
    Arrête quand tous les chevaux sauf les disqualifiés ont franchi la ligne, puis affiche le tiercé/quarté/quinté suivant le race_type.
    :param horses:
    :param race_type:
    :return:
    """
    horse_finished_count = 0
    finishing_line = []
    number_of_disqualifications = 0
    turns_count = 0
    race_result = []
    while True:
        if turns_count != 0:
            # Affichage
            for horse in horses:
                distance_remaining = 2400 - horse["distance"]
                distance_remaining_gui = cross_multiplication(2400, 120, distance_remaining)
                distance_gui = cross_multiplication(2400, 120, horse["distance"])
                if horse["finished"]: horse["color"] = "\033[92m"
                if horse["disqualified"]: horse["color"] = "\033[91m"
                if horse["distance"] > 0:
                    print("" + horse["color"] + " |" + " " * distance_gui + "♘" + " " * distance_remaining_gui + "|")
                else:
                    print("♘ |" + " " * 120 + "|")

        else:
            print("Les chevaux sont au départ")
            for _ in horses:
                print("♘ |" + " " * 120 + "|")

        for horse in horses:
            # logique
            if horse["finished"] is False:
                speed_change = change_speed(horse["speed"], roll_die(6))
                if speed_change is not None:
                    horse["speed"] += speed_change
                else:
                    horse["disqualified"] = True
                    number_of_disqualifications = + 1
                distance = DISTANCE_CHART[horse["speed"]]
                horse["distance"] += distance
                if horse["distance"] > 2400 and not horse["disqualified"]:
                    horse["finished"] = True
                    horse_finished_count += 1
                    finishing_line.append(horse["id"])
                elif horse["distance"] > 2400:
                    horse["finished"] = True

        if horse_finished_count >= len(horses) - 1 - number_of_disqualifications:
            break
        # selon le type de course on sélectionne 3,4,5 chevaux
        match race_type:
            case "quinte":
                race_result = finishing_line[:5]
            case "quarte":
                race_result = finishing_line[:4]
            case "tierce":
                race_result = finishing_line[:3]

        turns_count += 1
        next_turn()

    print(f"Tous les chevaux sont arrivés, la course est terminée.")
    print(f"Le {race_type} gagnant est le suivant ")
    print(", ".join(map(str, race_result)))


def start_game(horses, race_type):
    """
    Lance la simulation en version texte (sans la barre de progression graphique).
    À chaque tour : calcule les changements de vitesse, avance les chevaux via DISTANCE_CHART,
    gère disqualifications/arrivées, affiche l’état, attend Entrée avec next_turn.
    À la fin, annonce le tiercé/quarté/quinté en fonction de race_type.
        :param horses: La liste des chevaux
        :param race_type: le type de course
        :return:
        """

    horse_finished_count = 0
    finishing_line = []
    number_of_disqualifications = 0
    turns_count = 0
    race_result = []
    while True:
        if turns_count != 0:
            print("la course a commencé il y a " + str(turns_count * 10) + " sec")
            for horse in horses:
                if not horse["disqualified"] and not horse["finished"]:
                    print(
                        f"Le cheval  {horse["id"]} a une vitesse de {horse["speed"]} et a parcouru une distance de {horse["distance"]}m ")
                elif not horse["disqualified"] and horse["finished"]:
                    print(f"Le cheval {horse["id"]} a fini la course")
                elif horse["disqualified"] and not horse["finished"]:
                    print(f"Le cheval {horse["id"]} a été disqualifié !")
        else:
            print("Les chevaux sont au départ")

        for horse in horses:
            if horse["finished"] is False:
                speed_change = change_speed(horse["speed"], roll_die(6))
                if speed_change is not None:
                    horse["speed"] += speed_change
                else:
                    horse["disqualified"] = True
                    number_of_disqualifications = + 1
                distance = DISTANCE_CHART[horse["speed"]]
                horse["distance"] += distance
                if horse["distance"] > 2400 and not horse["disqualified"]:
                    horse["finished"] = True
                    horse_finished_count += 1
                    finishing_line.append(horse["id"])

        if horse_finished_count >= len(horses) - 1 - number_of_disqualifications:
            break
        # selon le type de course on sélectionne 3,4,5 chevaux
        match race_type:
            case "quinte":
                race_result = finishing_line[:5]
            case "quarte":
                race_result = finishing_line[:4]
            case "tierce":
                race_result = finishing_line[:3]

        turns_count += 1
        next_turn()

    print(f"Tous les chevaux sont arrivés, la course est terminée.")
    print(f"Le {race_type} gagnant est le suivant ")
    print(", ".join(map(str, race_result)))


# ----------------------------------------------------------------------------------------------------------------------#
# ------------------------------ Fonctions d'initialisation ------------------------------------------------------------#
# ----------------------------------------------------------------------------------------------------------------------#


def init_horses(num_horses):
    """
    Crée et renvoie la liste des chevaux (dictionnaires) initialisés : vitesse 0, non disqualifiés, distance 0, non
     arrivés, identifiant, et couleur par défaut pour l’affichage.
    :param num_horses:
    :return:
    """
    horses = []
    for horse in range(1, num_horses + 1):
        horse_dict = {
            "speed": 0,
            "disqualified": False,
            "distance": 0,
            "finished": False,
            "id": horse,
            "color": "\033[0m"
        }
        horses.append(horse_dict)

    return horses


def init_game(gui=False):
    """
    Initialise la course : crée la liste des chevaux via init_horses, demande le type de course avec ask_horse_race_type
    puis lance soit la version graphique (start_game_graphical) si gui=True, soit la version texte (start_game).
    :param gui:
    :return:
    """
    num_horses = ask_int_in_range("Combien de chevaux au départ ? (entre 12 et 20) : ",12,20)
    horses = init_horses(num_horses)
    race_type = ask_horse_race_type()

    if gui:
        start_game_graphical(horses, race_type)
    else:
        start_game(horses, race_type)


if __name__ == '__main__':
    init_game(True)
