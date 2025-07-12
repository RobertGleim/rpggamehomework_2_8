import os
import random
# ============================================ RPG Game Homework ===========================================


class Character:
    def __init__(self, name, health, attack_power, defence=0, level=1, xp=0):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defence = defence
        self.max_health = health
        self.level = level
        self.xp = xp
        self .xp_to_next_level = self.calculate_xp_to_next_level()
        self.item = None
        self.inventory = {}  # Placeholder for item, can be expanded later

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
        self.health += 5
        self.attack_power += 2
        self.defence += 1
        self.xp_to_next_level = self.calculate_xp_to_next_level()
        print(f"{self.name} has leveled up to level {self.level}! Health increased to: {self.health}, Attack Power increased to: {self.attack_power}, Defence increased: {self.defence}")

    def add_to_inventory(self, item):
        item_name = item["name"]
        if item_name in self.inventory:
            self.inventory[item_name]["count"] += 1
        else:
            self.inventory[item_name] = {"item": item, "count": 1}
        print(
            f"{self.name} picked up: {item_name} (x{self.inventory[item_name]['count']})")

    def use_item(self, item_name, enemy=None):
        item_name = item_name.strip()
        if item_name in self.inventory:
            item_info = self.inventory[item_name]
            item = item_info["item"]

            if item["type"] == "potion":
                old_health = self.health
                self.health += item["heal_amount"]
                if self.health > self.max_health:
                    self.health = self.max_health
                    actual_healed = self.health - old_health
                   
            elif item["type"] == "scroll":
                if enemy:    
                    damage = 50
                    enemy.health -= damage
                    if enemy.health < 0:
                        enemy.health = 0    
                    print(f"{self.name} used {item_name} on {enemy.name} and dealt {damage} damage!")
                    if enemy.health <= 0:
                         print(f"{enemy.name} has been defeated!")
                         self.gain_xp(enemy.xp_dropped)
                         return
                        
            else:
                print(f"{item_name} cannot be used!")
                return
                
                

            item_info["count"] -= 1
            if item_info["count"] == 0:
                del self.inventory[item_name]
            
        else:
            print(f"{item_name} not found in inventory.")

    def display_inventory(self):
        if not self.inventory:
            print(f"{self.name}'s inventory is empty.")
        else:
            print(f"{self.name}'s Inventory:")
            for item_name, item_info in self.inventory.items():
                print(
                    f"{item_name} (x{item_info['count']}) - {item_info['item']['description']}")

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
        inventory_str = (f"{item} (x{count})" for item,
                         count in self.inventory.items())
        if not self.inventory:
            inventory_str = "Empty"

        print(f'''
            =========  {self.name}'s Stats  =========
            Health: {self.health} 
            attack power: {self.attack_power}
            Defence: {self.defence}
            Level: {self.level}
            XP: {self.xp}/{self.xp_to_next_level}
            Inventory: {', '.join(self.inventory) if self.inventory else 'Empty'}
            ==========================
            ''')


hp_potion = {
    "name": "HP Pot",
    "type": "potion",
    "heal_amount": 50,
    "description": "Restores 20 HP."
}

fire_ball_scroll = {
    "name": "Fire Ball Scroll",
    "type": "scroll",
    "description": "A powerful scroll that casts a fireball spell.",
    "effect": "Deals 50 damage to an enemy."
}

enemy_drops = [
    {"item": "HP Pot", "chance": 25},
    # 50% chance to drop health potion
    {"item": "Fire Ball Scroll", "chance": 15},
]


# =========================================== Character classes ===========================================
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=25, defence=15, level=1, xp=0)
        self.inventory = {
            "Health Potion": {"item": hp_potion, "count": 4},
            "Fire Ball Scroll": {"item": fire_ball_scroll, "count": 1}
        }

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
        self.inventory = {
            "Health Potion": {"item": hp_potion, "count": 1},
            "Fire Ball Scroll": {"item": fire_ball_scroll, "count": 1}
        }

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
        self.inventory = {
            "Health Potion": {"item": hp_potion, "count": 1}
        }

    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(
            f"{self.name} stabs {opponent.name} with a Boolean. For {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")


class Archer(Character):
    def __init__(self, name,):
        super().__init__(name, health=120, attack_power=30, defence=5, level=1, xp=0)
        self.inventory = {
            "Health Potion": {"item": hp_potion, "count": 1}
        }

    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(
            f"{self.name} shoots an Array at {opponent.name} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(f"{opponent.name} has been defeated!")
            opponent.health = 0
        else:
            print(f"{opponent.name} has {opponent.health} hp remaining.")


class Enemy(Character):
    def __init__(self, name, health, attack_power, defence=0, level=1, xp_dropped=0):
        super().__init__(name, health, attack_power, defence, level)
        self.xp_dropped = xp_dropped

    def regenerate(self):
        self.health += 5
        print(f"{self.name} regenerates 5 health, now has {self.health} hp.")
        print("===========================================")


def random_battle():
    enemy_types = [
        Enemy("Syntax Error", 100, 20, defence=5, level=1, xp_dropped=20),
        Enemy("Invalid Selectors", 120, 15,
              defence=10, level=1, xp_dropped=30),
        Enemy("ZeroDivisionError", 90, 20, defence=25, level=1, xp_dropped=40),
        Enemy("Teacher wants to talk(miniboss)",
              150, 25, 20, level=5, xp_dropped=100),
        Enemy("Failing Class(Boss)", 200, 40,
              defence=20, level=1, xp_dropped=150)
    ]
    # def regenerate(self):
    #     self.health += 5
    #     print(f"{self.name} regenerates 5 health, now has {self.health} hp.")

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


def Battle(player, enemy):
    while enemy.health > 0 and player.health > 0:
        print("""
        1. Attack 
        2. Review Stats
        3. review Enemy Stats
        4. Use Item
        5. escape
    """)
        choice = input("Enter your choice: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == "1" or choice == "attack" or choice == "Attack":
            player.attack(enemy)
            if enemy.health > 0:
                enemy.regenerate()
                enemy.attack(player)
            else:
                print(
                    f"{enemy.name} has been defeated! {player.name} gains {enemy.xp_dropped} XP.")
                player.gain_xp(enemy.xp_dropped)

        elif choice == "2" or choice == "stats" or choice == "Stats" or choice == "review stats" or choice == "Review Stats":
            player.display_stats()
        elif choice == "3" or choice == "enemy stats" or choice == "Enemy Stats" or choice == "review enemy stats" or choice == "Review Enemy Stats":
            print(f"Enemy: {enemy.name}")
            print(f"Health: {enemy.health}")
            print(f"Attack Power: {enemy.attack_power}")
            print(f"Defence: {enemy.defence}")
            print(f"Level: {enemy.level}")
        elif choice == "4" or choice == "use item" or choice == "Use Item":
            if not player.inventory:
                print(f"{player.name}'s inventory is empty.")
                continue
            print(
                f"=============={player.name}'s Inventory:====================")
            item_list = list(player.inventory.keys())
            for i, item_name in enumerate(item_list, start=1):
                count = player.inventory[item_name]["count"]
                print(f"{i}. {item_name} (x{count})")

            print("=============================================================")
            item_choice = input("Enter the number of your choice: ")

            try:
                item_index = int(item_choice) - 1
                if 0 <= item_index < len(item_list):
                    selected_item = item_list[item_index]
                    # Use item and print healing message if applicable
                    old_health = player.health
                    player.use_item(selected_item, enemy=enemy)
                    # Check if item is a potion and healing occurred
                    item = player.inventory.get(selected_item, {}).get("item")
                    if item and item.get("type") == "potion":
                        actual_healed = player.health - old_health
                        print(
                            f"{player.name} used {selected_item} and healed for {actual_healed} HP!")
                        print(
                            f"{player.name}'s current health: {player.health}/{player.max_health}"
                            )
                
                else:
                    print("Invalid choice. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number corresponding to the item.")
                

        elif choice == "5" or choice == "escape" or choice == "Escape":
            print("Returning to main menu.")

        else:
            print("Invalid choice. Please try again.")


def main():
    player = create_character()
    while True:
        enemy = random_battle()
        print(f"\n==== A wild {enemy.name} appears! ===\n")
        Battle(player, enemy)

        if player.health <= 0:
            print(f"{player.name} has been defeated! Game Over.")
            break

        print("\nDo you want to continue battling? (yes/no)")
        print("1. Yes")
        print("2. No")

        choice = input("Enter your choice: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice.lower() == "yes" or choice == "1":
            continue
        elif choice.lower() == "no" or choice == "2":
            print("Exiting the game.")
            exit()
        else:
            print("Invalid choice. Please try again.")


main()
