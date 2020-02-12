class PlayerRoundStats(object):
    def __init__(self, round_number):
        # general round stats
        self.round_number = round_number
        self.round_length = 0
        self.round_winner = None

        # all-class stats
        self.kills = []
        self.assists = []
        self.deaths = []
        self.damage = []
        self.damage_received = []
        self.healing_received = []
        self.captures = []
        self.capture_blocks = []
        self.buildings_destroyed = []

        self.shots_hit = dict()
        self.shots_fired = dict()

        self.pickups_collected = []

        self.chat = []

        # medic stats
        self.ubers_used = dict()
        # self.ubers_built = 0
        self.healing_done = []
        self.self_drops = 0

        # engineer stats
        self.buildings_built = []

        # sniper stats
        self.headshots = 0
        self.headshot_kills = 0

        # spy stats
        self.backstabs = 0

    def destroy_building(self, building):
        self.buildings_destroyed.append(building)

    def build_building(self, building):
        self.buildings_built.append(building)

    def do_damage(self, damage_stat):
        self.damage.append(damage_stat)

    def receive_damage(self, damage_stat):
        self.damage_received.append(damage_stat)

    def do_healing(self, heal_trigger_stat):
        self.healing_done.append(heal_trigger_stat)

    def receive_healing(self, heal_trigger_stat):
        self.healing_received.append(heal_trigger_stat)

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

    def say(self, time, message, team_chat):
        self.chat.append(dict(time=time, message=message, team_chat=team_chat))

    def pick_up_item(self, item_pickup_stat):
        self.pickups_collected.append(item_pickup_stat)

    def killed(self, kill_stat):
        self.deaths.append(kill_stat)

    def get_suicides(self):
        # at the end of the round check self.deaths to get suicides

        suicides_death = 0
        for death in self.deaths:
            if death.attacker == death.victim:
                suicides_death += 1

        suicides_kill = 0
        for kill in self.kills:
            if kill.attacker == kill.victim:
                suicides_kill += 1

        # kills and deaths should be the same so verify
        assert suicides_death == suicides_kill
        return suicides_kill

    def get_time_alive(self):
        # at the end of the round check for alive time for each class
        alive_time = dict()
        return alive_time

    def get_enemy_drops(self):
        pass

    def get_self_drops(self):
        pass

    def get_healing_done(self):
        pass

    def get_healing_received(self):
        pass

    def get_airshots(self):
        pass

    def get_accuracy(self):
        # ignore sentry damage
        pass
