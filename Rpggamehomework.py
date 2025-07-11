import os
import random
# ============================================ RPG Game Homework ===========================================
class Character:
    def __init__(self, name, health, attack_power,defence=0,level=1, xp=0):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defence = defence
        self.max_health = health
        self.level = level
        self.xp = xp
        self .xp_to_next_level = self.calculate_xp_to_next_level()
        
    def calculate_xp_to_next_level(self):
        return int(self.level * 100 * 1.25)  
    
    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name} gains {amount} XP!")
        while self.xp >= self.xp_to_next_level:
            self.level_up() 
            
    def level_up(self):
        self.level += 1
                

    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(
            f"{self.name} has attacks {opponent.name} with a stick for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")

    def display_stats(self):
        print(
            f"{self.name}'s Stats \n Health: {self.health} \n attack power: {self.attack_power}")



# =========================================== Character classes ===========================================
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=25)
    
    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} Hits with a Hammer, smashing into {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=90, attack_power=75)
    
    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} casts Meteor strike, A giant Flaming Rock falls and hits {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")
            
class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, health=100, attack_power=50) 
    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} stabs the  {opponent.name} with a Dagger. For {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.") 
class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health=120, attack_power=30)

    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} shoots an arrow at {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")                         


class EvilWizard(Character):
    def __init__(self,):
        super().__init__(name="EvilWizard", health=150, attack_power=40)

    def regenerate(self):
        self.health += 5
        print(f"{self.name} regenerates 5 health, now has {self.health} hp.")

# =========================================== Character Creation ===========================================
# Create a character
def create_character():
    name = input("Enter your character's name: ")
    print("Choose your character:")
    print("1. Warrior")
    print("2. Mage")
    print("3. Rogue")
    print("4. Archer")
    print("5.Exit")
    choice = input("Enter the number of your choice: ")

    if choice == "1":
        return Warrior(name)
    elif choice == "2":
        return Mage(name)
    elif choice == "3":
        return Rogue(name)
    elif choice == "4":
        return Archer(name)
    else:
        print("Exiting the game.")
        exit()
        
os.system('cls' if os.name == 'nt' else 'clear')  

def Battle(player, boss):
    while boss.health > 0 and player.health > 0:
        print("""
              1. Attack again
              2. review stats""")
        choice = input("Enter your choice: ")
        os.system('cls' if os.name == 'nt' else 'clear')  
        if choice == "1":
            player.attack(boss)
            if boss.health > 0:
                boss.regenerate()
                boss.attack(player)
        elif choice == "2":
            player.display_stats()
        else:
            print("Invalid choice. Please try again.")
            continue
        
        


def main():
    player = create_character()
    boss = EvilWizard()
    Battle(player, boss)


main()