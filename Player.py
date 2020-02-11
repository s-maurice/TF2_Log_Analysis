class Player(object):
    # same player on different team counts as new player

    def __init__(self):
        # general info
        self.steam_id = None
        self.player_id = None
        self.name = None
        self.team = {"Red": False, "Blue": False}

        self.round_stats = []

    def trigger(self, trigger_type):
        if trigger_type == "Round_Start":
            # get the last round number
            try:
                last_round_number = self.round_stats[-1].round_number
            except IndexError:
                last_round_number = 0
            self.round_stats.append(PlayerRoundStats(last_round_number+1))  # first round is round 1
        else:
            pass

    def sum_round_stats(self):
        pass


class KillStats(object):
    # stats of each kill, death, or assist
    # can get distance of medic to heal target on assist
    def __init__(self):
        self.type = {"attacker": False, "assister": False, "victim": False}

        self.attacker_id = None
        self.assister_id = None
        self.victim_id = None

        self.attacker_class = None
        self.assister_class = None
        self.victim_class = None

        self.attacker_pos = [0, 0, 0]
        self.assister_pos = [0, 0, 0]
        self.victim_pos = [0, 0, 0]


class DamageStats(object):
    # stats of each damage instance
    def __init__(self):
        self.type = {"attacker": False, "victim": False}

        self.attacker_id = None
        self.victim_id = None

        self.attacker_class = None
        self.victim_class = None

        self.damage = 0
        self.realdamage = 0
        self.weapon = 0


class PlayerRoundStats(object):
    def __init__(self, round_number):
        # general round stats
        self.round_number = round_number
        self.round_length = 0
        self.accuracy = 0

        # all-class stats
        self.kills = []
        self.assists = []
        self.deaths = 0
        self.damage = 0
        self.suicides = 0
        self.damageTaken = 0
        self.healing_received = 0
        self.captures = 0
        self.airshots = 0
        self.enemy_drops = 0

        self.shots_hit = dict()
        self.shots_fired = dict()

        self.pickups_collected = dict()

        self.chat = []

        # medic stats
        self.ubers = dict()
        self.healing = 0
        self.self_drops = 0

        # engineer stats
        self.sentries = dict()
        self.sentry_healing = 0

        # sniper stats
        self.headshots = 0
        self.headshot_kills = 0

        # spy stats
        self.backstabs = 0

    def trigger_damage(self):
        pass

    def trigger_healed(self, healing):
        self.healing += healing

    def receive_healing(self, healing):
        self.healing_received += healing

    def trigger_shot_fired(self, weapon):
        # check if weapon is in dict, else create
        if weapon in self.shots_fired:
            self.shots_fired[weapon] += 1
        else:
            self.shots_fired[weapon] = 1

    def trigger_shot_hit(self, weapon):
        # check if weapon is in dict, else create
        if weapon in self.shots_hit:
            self.shots_hit[weapon] += 1
        else:
            self.shots_hit[weapon] = 1

    def trigger_medic_death(self, ubercharge):
        # ubercharge in these lines is 1 or 0 for drop
        pass

    def trigger_chargeready(self):
        pass

    def trigger_chargedeployed(self):
        pass

    def trigger_kill_assist(self):
        pass

    def trigger_domination(self):
        pass

    def trigger_pointcaptured(self):
        pass

    def trigger_round_win(self):
        pass

    def trigger_captureblocked(self):
        pass

    def say(self, message):
        self.chat.append(message)

    def picked_up_item(self, item):
        # check if item in dict, else create
        if item in self.pickups_collected:
            self.pickups_collected[item] += 1
        else:
            self.pickups_collected[item] = 1

    def killed(self):
        pass
