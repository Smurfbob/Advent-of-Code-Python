from Bingo import *

game: BingoGame = BingoGame("resource/Input.txt")

for board in game.play_game_until_winner():
    print(board["board"].get_sum_of_unmarked_numbers() * game.last_call)
