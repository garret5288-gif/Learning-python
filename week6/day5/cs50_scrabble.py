# CS50 Scrabble Game
# This program allows two players to enter words and calculates their Scrabble scores.

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
values = [1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10]

def get_word(player_num): # get word from player
    return input(f"Player {player_num}, enter a word: ")

def get_score(word): # calculate score of the word
    return sum([values[letters.index(char)] for char in word.upper() if char in letters])

def print_scores(score1, score2): # print both players' scores
    print("Player 1 score:", score1)
    print("Player 2 score:", score2)

def print_winner(score1, score2): # determine and print the winner
    if score1 > score2:
        print("Player 1 wins!")
    elif score2 > score1:
        print("Player 2 wins!")
    else:
        print("It's a tie!")

def main(): # main function to run the game
    word1 = get_word(1)
    word2 = get_word(2)
    score1 = get_score(word1)
    score2 = get_score(word2)
    print_scores(score1, score2)
    print_winner(score1, score2)

main()
