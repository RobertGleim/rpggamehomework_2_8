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
        self.item = None  # Placeholder for item, can be expanded later
        
    def calculate_xp_to_next_level(self):
        return int(self.level * 100 * 1.25)  
    
    def gain_xp(self, amount):
        self.xp += amount
        print(f"{self.name} gains {amount} XP!")
        while self.xp >= self.xp_to_next_level:
            self.level_up() 
            
    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.health =+ 5
        self.attack_power += 2
        self.defence += 1
        self.xp_to_next_level = self.calculate_xp_to_next_level()
        print(f"{self.name} has leveled up to level {self.level}! Health increased to: {self.health}, Attack Power increased to: {self.attack_power}, Defence increased: {self.defence}")        

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
        print(f'''
            =====  {self.name}'s Stats  =====
            Health: {self.health} 
            attack power: {self.attack_power}
            Defence: {self.defence}
            Level: {self.level}
            XP: {self.xp}/{self.xp_to_next_level}
            ==========================
            ''')



# =========================================== Character classes ===========================================
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=25, defence=15, level=1, xp=0)
    
    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} Hits with a DOCTYPE, smashing into {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=90, attack_power=75, defence=0, level=1, xp=0)
    
    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} casts @KeyFrame, A giant Flaming Rock falls and hits {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")
            
class Rogue(Character):
    def __init__(self, name,):
        super().__init__(name, health=100, attack_power=50, defence=5, level=1, xp=0) 
    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} stabs {opponent.name} with a Boolean. For {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.") 
class Archer(Character):
    def __init__(self, name,) :
        super().__init__(name, health=120, attack_power=30, defence=5, level=1, xp=0)

    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(f"{self.name} shoots an Array at {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")                         


class Enemy(Character):
    def __init__(self, name, health, attack_power, defence=0, level=1, xp_dropped=0):
        super().__init__(name, health, attack_power, defence, level)
        self.xp_dropped = xp_dropped

def random_battle():
    enemy_types = [
        Enemy("Syntax Error", 100, 20, defence=5, level=1, xp_dropped=10),
        Enemy("Invalid Selectors", 120, 15, defence=10, level=1, xp_dropped=15),
        Enemy("ZeroDivisionError", 90, 20, defence=25, level=1, xp_dropped=20),
        Enemy("Teacher wants to talk(miniboss)",150, 25, 20, level =5 , xp_dropped=50),
        # Enemy("Failing Class(Boss)", 200, 40, defence=20, level=1, xp_dropped=50)
    ]
    enemy = random.choice(enemy_types)
    return enemy


       
class EvilWizard(Character):
    def __init__(self,):
        super().__init__(name="EvilWizard", health=150, attack_power=40)

    def regenerate(self):
        self.health += 5
        print(f"{self.name} regenerates 5 health, now has {self.health} hp.")

# =========================================== Character Creation ===========================================
# Create a character
def create_character():
    os.system('cls' if os.name == 'nt' else 'clear') 
    print("=========Welcome to the Coding Temple House of Horrors!!!!=========\n\n") 
    
    name = input("Please Enter your character's name: ")
    print("Choose your character:")
    print("1. Html Warrior")
    print("2. CSS Mage")
    print("3. Python Rogue")
    print("4. JavaScript Archer")
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
    elif choice == "5":
        print("Exiting the game.")
        exit()
    else:
        print("Invalid choice please choose again.")
        return create_character()
            
        
os.system('cls' if os.name == 'nt' else 'clear')  

def Battle(player, boss):
    while boss.health > 0 and player.health > 0:
        print("""
        1. Attack 
        2. Review Stats
        3. Exit
    """)
        choice = input("Enter your choice: ")
        os.system('cls' if os.name == 'nt' else 'clear')  
        if choice == "1":
            player.attack(boss)
            if boss.health > 0:
                boss.regenerate()
                boss.attack(player)
        elif choice == "2":
            player.display_stats()
        elif choice == "3":
            print("Returning to main menu.")
            break
               
        else:
            print("Invalid choice. Please try again.")
            continue
        
        


def main():
    player = create_character()
    boss = EvilWizard()
    Battle(player, boss)


main()