# Game Characters: Player and Enemy classes with attack and health management
# Demonstrates OOP concepts in Python

class Player: # Player character class
    def __init__ (self, name, health):
        self.name = name
        self.health = health

    def attack(self, other): # Attack another character
        if not isinstance(other, Enemy):
            print("Can only attack an enemy.")
            return
        damage = 10
        other.health -= damage # reduce enemy's health
        print(f"{self.name} attacks {other.species} for {damage} damage!")
        if other.health <= 0: # Check if the enemy is defeated
            other.health = 0
            print(f"{other.species} has been defeated!")

    def dead(self): # Check if player is dead
        return self.health <= 0
    
    def display_info(self): # Display player info
        status = "Dead" if self.dead() else f"Health: {self.health}"
        print(f"Player: {self.name}, {status}")

class Enemy: # Enemy character class
    def __init__ (self, species, health):
        self.species = species
        self.health = health

    def attack(self, player): # Attack a player
        if not isinstance(player, Player):
            print("Can only attack a player.")
            return
        damage = 5
        player.health -= damage # reduce player's health
        print(f"{self.species} attacks {player.name} for {damage} damage!")
        if player.health <= 0: # Check if the player is defeated
            player.health = 0 
            print(f"{player.name} has been defeated!")

    def dead(self): # Check if enemy is dead
        return self.health <= 0

    def display_info(self): # Display enemy info
        status = "Dead" if self.dead() else f"Health: {self.health}"
        print(f"Enemy: {self.species}, {status}")

Garret = Player("Garret", 100)
Goblin = Enemy("Goblin", 30)

Garret.display_info()
Goblin.display_info()

def main(): # Main program loop
    while not Garret.dead() and not Goblin.dead():
        Garret.attack(Goblin)
        if Goblin.dead():
            break
        Goblin.attack(Garret)
        Garret.display_info()
        Goblin.display_info()

if __name__ == "__main__":
    main()