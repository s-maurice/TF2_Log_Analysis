class PlayerTriggerStat(object):
    # stats of a player during a trigger tick
    def __init__(self, player_id, player_class):
        self._player_id = player_id
        self.player_class = player_class
        self.position = None


class DamageStats(object):
    # stats of each damage instance
    # can check distance, height to see if airshot
    def __init__(self):
        # self.type = {"attacker": False, "victim": False}

        self.attacker = None  # instance of PlayerTriggerStat
        self.victim = None  # instance of PlayerTriggerStat

        self.damage = 0
        self.realdamage = 0
        self.weapon = 0


class KillStats(object):
    # stats of each kill, death, or assist
    # can get distance of medic to heal target on assist
    def __init__(self):
        # self.type = {"attacker": False, "assister": False, "victim": False}
        self.uber_drop = None

        self.time = None

        self.attacker = None  # instance of PlayerTriggerStat with given position
        self.assister = None  # instance of PlayerTriggerStat with given position
        self.victim = None  # instance of PlayerTriggerStat with given position


class PointCaptureBlockStats(object):
    # stats of capture point blocks
    def __init__(self):
        self.cp_id = None
        self.cp_name = None

        self.blocker = None  # instance of PlayerTriggerStat with given position


class PointCaptureStats(object):
    # stats of capture point captures
    def __init__(self):
        self.cp_id = None
        self.cp_name = None

        self.num_cappers = 0
        self.cappers = []  # list of PlayerTriggerStats with given position
