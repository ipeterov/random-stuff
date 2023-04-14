import json
import random
from collections import defaultdict

group_a = [
    "evil-geniuses",
    "psg-lgd",
    "team-liquid",
    "hokori",
    "rng",
    "og",
    "gaimin-gladiators",
    "soniqs",
    "betboom-team",
    "boom-esports",
]

group_b = [
    "tundra-esports",
    "team-aster",
    "team-secret",
    "thunder-awaken",
    "fnatic",
    "team-spirit",
    "beastcoast",
    "entity",
    "talon-esports",
    "tsm",
]


class Game:
    def __init__(
            self,
            team1,
            team2,
            outcome=None,
            win_chance=None,
            draw_chance=None,
            loss_chance=None,
    ):
        self.team1 = team1
        self.team2 = team2
        self.outcome = outcome
        self.win_chance = win_chance
        self.draw_chance = draw_chance
        self.loss_chance = loss_chance

    def __str__(self):
        return f"{self.team1} played {self.team2}"

    @classmethod
    def from_json(cls, obj):
        return cls(
            team1=obj['team1'],
            team2=obj['team2'],
            outcome=obj['outcome'],
            win_chance=obj['win_chance'],
            draw_chance=obj['draw_chance'],
            loss_chance=obj['loss_chance'],
        )

    def as_json(self):
        return {
            "team1": self.team1,
            "team2": self.team2,
            "outcome": self.outcome,
            "win_chance": self.win_chance,
            "draw_chance": self.draw_chance,
            "loss_chance": self.loss_chance,
        }

    def ask_for_result(self):
        while True:
            outcome = input(f'{self.team1} played {self.team2}. win/draw/loss/tbd? ')
            if outcome in {'win', 'draw', 'loss', 'tbd'}:
                break
            print('enter valid outcome')

        if outcome == 'tbd':
            self.win_chance = 1 / float(input(f"\todds for {self.team1}? "))
            self.draw_chance = 1 / float(input(f"\todds for draw? "))
            self.loss_chance = 1 / float(input(f"\todds for {self.team2}? "))
        else:
            self.outcome = outcome

    def resolve_random(self):
        self.outcome = random.choices(
            ['win', 'draw', 'loss'],
            [self.win_chance, self.draw_chance, self.loss_chance],
        )[0]


class Tournament:
    def __init__(self, teams: list[str]):
        self.games = []

        self.out = []
        self.lower = []
        self.upper = []

        team_pairs = set()
        for team in teams:
            for other_team in teams:
                if team == other_team:
                    continue

                if (other_team, team) in team_pairs:
                    continue

                if (team, other_team) in team_pairs:
                    continue

                team_pairs.add((team, other_team))
                self.games.append(Game(
                    team1=team,
                    team2=other_team,
                ))

    @property
    def scores(self):
        scores = defaultdict(int)
        for game in self.games:
            if game.outcome == 'win':
                scores[game.team1] += 2
            elif game.outcome == 'draw':
                scores[game.team1] += 1
                scores[game.team2] += 1
            elif game.outcome == 'loss':
                scores[game.team2] += 2
        return scores

    @property
    def wins(self):
        scores = defaultdict(int)
        for game in self.games:
            if game.outcome == 'win':
                scores[game.team1] += 1
        return scores

    def ask_for_results(self):
        for game in self.games:
            if game.outcome is not None:
                continue
            game.ask_for_result()

    def resolve_tbd_games(self):
        for game in self.games:
            if game.outcome is None:
                game.resolve_random()

    def determine_brackets(self):
        teams = [
            team for team, _
            in sorted(self.scores.items(), key=lambda x: (x[1], self.wins[team]))
        ]
        self.out = teams[:2]
        self.lower = teams[2:6]
        self.upper = teams[6:]

    def save(self, name):
        with open(name, 'w') as f:
            games = [game.as_json() for game in self.games]
            json.dump(games, f)

    def load(self, name):
        with open(name, 'r') as f:
            self.games = [
                Game.from_json(game_obj)
                for game_obj in json.load(f)
            ]


if __name__ == '__main__':
    # group_stage = Tournament(teams=group_a)
    # group_stage.ask_for_results()
    # group_stage.save("group_a.json")
    
    t = 10000
    for team in group_b:
        upper = 0
        lower = 0
        out = 0
        for _ in range(t):
            group_stage = Tournament(teams=group_b)
            group_stage.load('group_b.json')
            group_stage.resolve_tbd_games()
            group_stage.determine_brackets()

            if team in group_stage.out:
                out += 1
            elif team in group_stage.lower:
                lower += 1
            elif team in group_stage.upper:
                upper += 1

        print(f'{team}: upper - {upper / t * 100}%, lower - {lower / t * 100}%, out - {out / t * 100}%')
