from Bingo import *

game: BingoGame = BingoGame("resource/Input.txt")

for board in game.play_game_until_winner():
    print(board["board"].get_sum_of_unmarked_numbers() * game.last_call)

last_winner: BingoBoard = game.get_last_winning_game()
sum_of = last_winner.get_sum_of_unmarked_numbers()
ind: int = game.last_counter
print(sum_of * ind)
