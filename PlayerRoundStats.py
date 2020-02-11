class PlayerRoundStats(object):
    def __init__(self, round_number):
        # general round stats
        self.round_number = round_number
        self.round_length = 0
        self.round_winner = None

        self.accuracy = 0

        # all-class stats
        self.kills = []
        self.assists = []
        self.deaths = []
        self.suicides = 0
        self.damage = []
        self.damage_received = []
        self.healing_received = 0
        self.captures = []
        self.capture_blocks = []
        self.airshots = 0
        self.enemy_drops = 0

        self.shots_hit = dict()
        self.shots_fired = dict()

        self.pickups_collected = dict()

        self.chat = []

        # medic stats
        self.ubers_used = dict()
        self.ubers_built = 0
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

    def do_damage(self, damage_stat):
        self.damage.append(damage_stat)

    def receive_damage(self, damage_stat):
        self.damage_received.append(damage_stat)

    def do_healing(self, healing):
        self.healing += healing

    def receive_healing(self, healing):
        self.healing_received += healing

    def fire_shot(self, weapon):
        # check if weapon is in dict, else create
        if weapon in self.shots_fired:
            self.shots_fired[weapon] += 1
        else:
            self.shots_fired[weapon] = 1

    def hit_shot(self, weapon):
        # check if weapon is in dict, else create
        if weapon in self.shots_hit:
            self.shots_hit[weapon] += 1
        else:
            self.shots_hit[weapon] = 1

    def trigger_chargeready(self):
        # chargeready is instantly followed by chargedeployed, so ignore
        pass

    def use_uber(self, medigun):
        # check if item in dict, else create
        if medigun in self.ubers_used:
            self.ubers_used[medigun] += 1
        else:
            self.ubers_used[medigun] = 1

    def trigger_kill_assist(self, kill_stat):
        self.assists.append(kill_stat)

    def trigger_domination(self):
        # ignore dominations
        pass

    def capture_capture_point(self, point_capture_stat):
        self.captures.append(point_capture_stat)

    def trigger_round_win(self, winner):
        self.round_winner = winner

    def trigger_round_length(self, round_time):
        self.round_length = round_time

    def block_capture_point(self, point_capture_block_stat):
        self.capture_blocks.append(point_capture_block_stat)

    def say(self, time, message):
        self.chat.append(dict(time=time, message=message))

    def pick_up_item(self, item):
        # check if item in dict, else create
        if item in self.pickups_collected:
            self.pickups_collected[item] += 1
        else:
            self.pickups_collected[item] = 1

    def killed(self, kill_stat):
        self.deaths.append(kill_stat)

    def get_suicides(self):
        # at the end of the round check self.deaths to get suicides
        pass

    def get_time_alive(self):
        # at the end of the round check for alive time
        pass
