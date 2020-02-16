class PlayerTriggerStat(object):
    # stats of a player during a trigger tick
    player_class = None
    position = None  # position not always known, only known during specific ticks

    def __init__(self, parsed_tuple):
        # player assumed to be alive during init
        (steam_id, name, player_id, team) = parsed_tuple
        self.steam_id = steam_id
        self.name = name
        self.player_id = player_id
        self.team = team
        self.alive = True

    def set_position_by_string(self, pos_string):
        # use @property?
        # takes position string, splits by " " and stores pos tuple
        self.position = tuple(pos_string.split(" "))


class PlayersTriggerStat(object):
    # stats of all players during a trigger tick
    players = {"Red": [], "Blue": []}

    def add_player(self, player_trigger_stat):
        assert type(player_trigger_stat) == PlayerTriggerStat
        self.players[PlayerTriggerStat.team].append(PlayerTriggerStat)

    def get_player_by_steam_id(self, steam_id):
        # gets the player with the matching steam_id, return None if player not in
        for player in [i for value in self.players.values() for i in value]:
            if player.steam_id == steam_id:
                return player
        else:
            return None

    def clear_positions(self):
        # goes through the players and removes the positions, as positions are only valid for a single tick
        for player in [i for value in self.players.values() for i in value]:
            player.position = None


class DamageStat(object):
    # stats of each damage instance
    # can check distance, height to see if airshot
    def __init__(self):
        # self.type = {"attacker": False, "victim": False}

        self.attacker = None  # instance of PlayerTriggerStat
        self.victim = None  # instance of PlayerTriggerStat

        self.damage = 0
        self.realdamage = 0
        self.weapon = 0


class KillStat(object):
    # stats of each kill, death, or assist
    # can get distance of medic to heal target on assist
    def __init__(self, attacker, victim, weapon):
        self.uber_drop = None
        self.weapon = weapon

        self.time = None

        self.attacker = attacker  # instance of PlayerTriggerStat with given position
        self.victim = victim  # instance of PlayerTriggerStat with given position

        self.assister = None  # instance of PlayerTriggerStat with given position

    def add_assister(self, assister):
        # adds an assister to the kill stat
        assert assister.position is not None
        self.assister = assister

    def get_dist_attacker_victim(self):
        # gets the distance between the attacker and the victim
        return self.get_dist(self.attacker, self.victim)

    def get_dist_assister_attacker(self):
        # gets the distance between the assister and attacker
        if self.assister is not None:
            return self.get_dist(self.assister, self.attacker)
        else:
            return 0

    @staticmethod
    def get_dist(from_pos, to_pos):
        squared = [(i-ii)**2 for i, ii in zip(from_pos, to_pos)]
        return sum(squared)**0.5


class PointCaptureBlockStat(object):
    # stats of capture point blocks
    def __init__(self):
        self.cp_id = None
        self.cp_name = None

        self.blocker = None  # instance of PlayerTriggerStat with given position


class PointCaptureStat(object):
    # stats of capture point captures
    def __init__(self):
        self.cp_id = None
        self.cp_name = None

        self.num_cappers = 0
        self.cappers = []  # list of PlayerTriggerStats with given position


class HealTriggerStat(object):
    # stat for each heal trigger
    def __init__(self):
        self.healing = 0
        self.arrow = False  # is healing from crusaders crossbow

        self.healer = None  # instance of PlayerTriggerStat
        self.receiver = None  # instance of PlayerTriggerStat


class ItemPickupStat(object):
    # stat from each item pickup
    def __init__(self, item, player):
        self.healing = 0
        self.item = item

        self.player = None  # instance of PlayerTriggerStat
