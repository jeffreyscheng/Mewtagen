from Team import *
from Damage import *
import random
import time


class Battle:

    @staticmethod
    def battle(team1, team2):
        tick = time.clock();
        team1.heal()
        team2.heal()
        team1.current = random.choice(list(team1.party.keys()))
        team2.current = random.choice(list(team2.party.keys()))

        while team1.still_playing() and team2.still_playing():
            if team1.is_fainted() or team1.current is None:
                team1.switch()
            if team2.is_fainted() or team2.current is None:
                team2.switch()
            bool_1_counters_2 = team1.current in Dialgarithm.counters_dict[team2.current]
            bool_2_counters_1 = team2.current in Dialgarithm.counters_dict[team1.current]

            def normal_damage():
                if team1.current.spe_stat > team2.current.spe_stat:
                    team1_moves_first = True
                elif team1.current.spe_stat < team2.current.spe_stat:
                    team1_moves_first = False
                else:
                    team1_moves_first = random.choice([0, 1])
                if team1_moves_first:
                    team2.damage_current(Damage.deal_damage(team1.current, team2.current))
                    if not team2.is_fainted():
                        team1.damage_current(Damage.deal_damage(team2.current, team1.current))
                else:
                    team1.damage_current(Damage.deal_damage(team2.current, team1.current))
                    if not team1.is_fainted():
                        team2.damage_current(Damage.deal_damage(team1.current, team2.current))

            # Case 1: both stay
            if (not bool_1_counters_2) and (not bool_2_counters_1):
                normal_damage()

            # Case 2: 1 stays, 2 switches
            elif bool_1_counters_2:
                if team2.has_living_counter(team1.current):
                    team2.switch(team1.current)
                    team2.damage_current(Damage.deal_damage(team1.current, team2.current))
                else:
                    normal_damage()

            # Case 3: 2 stays, 1 leaves
            elif bool_2_counters_1:
                if team1.has_living_counter(team2.current):
                    team1.switch(team2.current)
                    team1.damage_current(Damage.deal_damage(team2.current, team1.current))
                else:
                    normal_damage()

            # Case 4: both switch
            # I don't think this should ever happen?
            else:
                print('These two Pokemon counter each other somehow')
                print(team1.current.name)
                print(team2.current.name)
                raise RuntimeError("two mons counter each other, both switch?")
        tock = time.clock();
        print('BATTLE FINISHED IN: ' + str(tock - tick) + ' seconds.')
        if team1.still_playing():
            return team1
        else:
            return team2
