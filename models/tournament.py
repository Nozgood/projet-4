from models.turn import Turn
from models.game import Game
from models.player import Player

import uuid
from datetime import datetime
import random

class Tournament:
    def __init__(
            self,
            name: str,
            place: str,
            startDate: datetime.date,
            endDate: datetime.date,
            all_turns: list[Turn],
            registeredPlayers: list[Player],
            description: str,
            number_of_turns=4,
            actual_turn=1
    ):
        self.ID = uuid.uuid1()
        self.name = name
        self.place = place
        self.startDate = startDate.today()
        self.endDate = endDate
        self.actualTurn = actual_turn
        self.all_turns = all_turns
        self.registeredPlayers = registeredPlayers
        self.description = description
        self.number_of_turns = number_of_turns
        self.actual_turn = actual_turn

    def register_new_player(self, player: Player):
        for registeredPlayer in self.registeredPlayers:
            if player.nationalChessID == registeredPlayer.nationalChessID:
                print("This player has been already registered")
                return
        self.registeredPlayers.append(player)

    def blend_players_first_turn(self):
        blended_players = self.registeredPlayers
        random.shuffle(blended_players)
        return blended_players

    def sort_players_by_score(self):
        sorted_players = self.registeredPlayers
        sorted_players.sort(key=Player.display_score, reverse=False)
        return sorted_players

    def create_turn(self):
        players = list[Player]
        if self.actualTurn == 1:
            players = self.blend_players_first_turn()
        else:
            players = self.sort_players_by_score()
        turn_name = "round " + str(self.actualTurn)
        start_date = datetime.today()
        start_hour = datetime.time().strftime("%H:%M:%S")
        all_games = self.create_games(players)
        turn = Turn(turn_name, players, len(all_games), all_games, start_date, start_hour)
        self.all_turns.append(turn)
        return turn

    def create_games(self, players: list[Player]):
        all_games = list[Game]
        for i in range(0, len(players), 2):
            game = players[i:i+2]
            all_games.append(game)
        return all_games

    def update_players_points(self, game: Game):
        self.find_and_update_player_by_id(game.playerOneInfo.nationalChessID, game.playerOneInfo.score)
        self.find_and_update_player_by_id(game.playerTwoInfo.nationalChessID, game.playerTwoInfo.score)

    def find_and_update_player_by_id(self, nationalChessID: str, new_score: int):
        for player in self.registeredPlayers:
            if player.nationalChessID == nationalChessID:
                player.score = new_score
        print("we didn't find a player with this national chess ID in this tournament")
        return

    def update_actual_turn(self):
        if self.actualTurn == self.number_of_turns:
            print("it was the last turn of the tournament")
            return
        self.actualTurn += 1

    def end_turn(self, turn: Turn):
        turn.end_turn()
        for game in turn.all_games:
            self.update_players_points(game)
        self.update_actual_turn()

    def post(self):
        pass

    def get(self, tournamentID):
        pass

    def put(self, tournamentID):
        pass
