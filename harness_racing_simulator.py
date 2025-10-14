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
    start_game(horses)


def change_speed(speed,die_roll):
    return SPEED_CHART[speed][die_roll - 1]



def roll_die(die_size):
    return random.randrange(1, die_size+1)


def next_turn():
    input("Tour suivant")


def start_game(horses):
    horse_finished_count = 0
    while True:
        for horse in horses:
            if horse["finished"] is False:
                speed_change = change_speed(horse["speed"], roll_die(6))
                if speed_change is not None:
                    horse["speed"] += speed_change
                else:
                    horse["disqualified"] = True

                distance = DISTANCE_CHART[horse["speed"]]
                horse["distance"] += distance
                if horse["distance"] > 2400:
                    horse["finished"] = True
                    horse_finished_count += 1



        print (horse_finished_count)
        if horse_finished_count > len(horses):
            break


        next_turn()
        print(horses)
    "la course est terminée"



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


if __name__ == '__main__':
    init_game(12)