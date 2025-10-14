#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Simulateur de trot attelé, il s'agit d'une course de 12 à 20 chevaux, faisant l'objet d'un tierce,quarte,quinte, elle
se deroule sur un hippodrome rectiligne de 2400m.
"""

import random

SPEED_CHART : dict = {
    0: ( 0,  1,  1,  1,  2,  2),
    1: ( 0,  0,  1,  1,  1,  2),
    2: ( 0,  0,  0,  1,  1,  2),
    3: (-1,  0,  0,  0,  1,  1),
    4: (-1, -1,  0,  0,  0,  1),
    5: (-2, -1,  0,  0,  0,  1),
    6: (-2, -1,  0,  0,  0, None),
                    }
DISTANCE_CHART = [0,23,46,69,92,115,138]


def init_game(num_horses):
    horses = init_horses(num_horses)
    race_type = ask_horse_race_type()
    start_game(horses,race_type)


def change_speed(speed,die_roll):
    return SPEED_CHART[speed][die_roll - 1]



def roll_die(die_size):
    return random.randrange(1, die_size+1)


def next_turn():
    input("Appuyez sur entrée pour avancer la course")


def start_game(horses,race_type):
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
                    print(f"Le cheval {horse["id"]} a une vitesse de {horse["speed"]} et a parcouru une distance de {horse["distance"]}m ")
                elif not horse["disqualified"] and  horse["finished"] :
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
                    number_of_disqualifications =+ 1
                distance = DISTANCE_CHART[horse["speed"]]
                horse["distance"] += distance
                if horse["distance"] > 2400 and not horse["disqualified"]:
                    horse["finished"] = True
                    horse_finished_count += 1
                    finishing_line.append(horse["id"])


        if horse_finished_count >= len(horses) - 1 -  number_of_disqualifications :
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

    print (f"Tous les chevaux sont arrivés, la course est terminée.")
    print (f"Le {race_type} gagnant est le suivant ")
    print(", ".join(map(str, race_result)))



def init_horses(num_horses) :
    horses = []
    for horse in range(1, num_horses + 1):
        horse_dict = {
            "speed": 0,
            "disqualified": False,
            "distance": 0,
            "finished": False,
            "id": horse
        }
        horses.append(horse_dict)

    return horses

def ask_horse_race_type():
    race_type = input("Quel type de course ? (tierce,quarte,quinte) : ")
    if race_type == "quinte" or race_type == "quarte" or race_type == "tierce":
        return race_type
    else:
        print("merci de rentrer un des termes suivants: 'quinte','quarte','tierce'")
        return ask_horse_race_type()

if __name__ == '__main__':
    init_game(12)