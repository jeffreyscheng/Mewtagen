class Moveset:

    def __init__(self, poke, moves, evs, ivs, usage):
        self.dex = poke
        self.moves = moves
        self.hp_stat = None
        self.atk_stat = None
        self.def_stat = None
        self.spa_stat = None
        self.spd_stat = None
        self.spe_stat = None
        self.usage = None

    def get_stat(self, name, evs, ivs):
        self.__dict__[name] = 0

        # ev = self.get_ev(name, stat)
        # base = self.smogon_movesets[name][stat]
        # if len(self.smogon_movesets[name]['natures']) > 0:
        #     nature = self.smogon_movesets[name]['natures'][0]
        #     nature_coeff = self.natures.loc[nature, stat]
        # else:
        #     nature_coeff = 1
        # if stat == 'hp':
        #     return math.floor(2 * base + 31 + math.floor(ev / 4)) + 110
        # else:
        #     return (math.floor(2 * base + 31 + math.floor(ev / 4)) + 5) * nature_coeff
