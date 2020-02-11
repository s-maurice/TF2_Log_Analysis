from PlayerRoundStats import PlayerRoundStats


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