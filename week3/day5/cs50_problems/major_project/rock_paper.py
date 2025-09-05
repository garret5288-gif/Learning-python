# Rock, Paper, Scissors Game
import random #import the random module to enable random choice for the computer

options = ["rock", "paper", "scissors"] #list of valid options
running = True #boolean variable to control the game loop

while running: #main game loop

    player = None #initialize player variable
    computer = random.choice(options) #computer randomly selects an option from the list

    while player not in options: #input validation loop
        player = input("Enter rock, paper, or scissors: ").strip().lower() # Normalize input to lowercase and remove extra spaces

    print(f"Player: {player}")
    print(f"Computer: {computer}")
    if player == computer: # Check for a tie
        print("It's a tie!")
    
    elif (player == "rock" and computer == "scissors"): # Player wins scenarios
        print("You win!")
    
    elif (player == "paper" and computer == "rock"):
        print("You win!")   
    
    elif (player == "scissors" and computer == "paper"):
        print("You win!")
    
    else:
        print("You lose!") # All other scenarios result in a loss

    play_again = input("Play again? (y/n): ").strip().lower() == "y" # Prompt to play again
    if not play_again: # If the player does not want to play again, exit the loop
        running = False
print("Thanks for playing!")
