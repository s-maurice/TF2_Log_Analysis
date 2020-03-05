class Game(object):
    # class containing the statistics for all events in a game
    def __init__(self):
        self.rounds = [Round(1)]  # create with empty round 1

    def get_latest_round(self):
        # returns the latest round stat if it is not ended, otherwise create new round and return that
        if self.rounds[-1].ended is True:
            cur_round_no = self.rounds[-1].round_no
            self.rounds.append(Round(cur_round_no+1))
        return self.rounds[-1]


class Round(object):
    # class containing the statistics for all players over a single round
    def __init__(self, round_no):
        self.round_no = round_no
        self.ended = False

    def add_trigger_stat(self, trigger_stat):
        # takes incoming trigger stats and adds to the correct player round
        pass


class PlayerRound(object):
    # class containing the statistics for a single player over a single round
    pass


class PlayerLife(object):
    # class containing the statistics for one life of a single player
    pass
