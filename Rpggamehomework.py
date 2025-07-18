import os
import random

# ============================================ RPG Game Homework ===========================================


class Character:
    def __init__(self, name, health, attack_power, defence=0, level=1, xp=0, weapon=None):
        self.name = name
        self.health = health
        self.attack_power = attack_power
        self.defence = defence
        self.max_health = health
        self.level = level
        self.xp = xp
        self.xp_to_next_level = self.calculate_xp_to_next_level()
        self.item = None
        self.inventory = {}
        self.inventory = {
            "small_hp_potion": {"item": small_hp_potion, "count": 4},
            "fire_ball_scroll": {"item": fire_ball_scroll, "count": 1}
        }
        self.weapon = weapon

    def calculate_xp_to_next_level(self):
        return int(self.level * 100 * 1.25)

    def gain_xp(self, amount):
        self.xp += amount

        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next_level
        self.max_health = int(self.max_health * 1.1)
        self.health = int(self.max_health)
        self.attack_power += 2
        self.defence += 1
        self.xp_to_next_level = self.calculate_xp_to_next_level()
        print(f"            🎆🎆🎆  {self.name} has leveled up to level {self.level}! Health increased to: {self.health}, Attack Power increased to: {self.attack_power}, Defence increased: {self.defence}  🎆🎆🎆")

    def add_to_inventory(self, item):
        item_key = next((key for key, val in item_lookup.items() if val == item), item["name"])
        if item_key in self.inventory:
            self.inventory[item_key]["count"] += 1
        else:
            self.inventory[item_key] = {"item": item, "count": 1}
        print(f"                      😊  {self.name} got: {item['name']}  😊")



    def use_item(self, item_name, enemy=None):
        item_name = item_name.strip()

        if item_name not in self.inventory:
            print(f"            ❌ {item_name} not found in inventory.")
            return

        item_info = self.inventory[item_name]
        item = item_info["item"]

        if item_info["count"] <= 0:
            print(f"            ❌ No more {item_name} left in inventory.")
            del self.inventory[item_name]
            return

        if item["type"] in ("potion_small", "potion_med", "potion_large"):
            if self.health >= self.max_health:
                print(
                    f"🧪  {self.name} is already at full health! Potion not needed.")
                return

            old_health = self.health
            self.health += item["heal_amount"]
            if self.health > self.max_health:
                self.health = self.max_health
            healed_amount = self.health - old_health
            print(
                f"\n\n🧪  {self.name} used {item['name']} and healed for {healed_amount} HP! Current: {self.health}/{self.max_health}  🧪")

        elif item["type"] == "fire_scroll":
            if enemy is None:
                print(f"❌ Cannot use {item['name']} without an enemy present.")
                return

            damage = 50
            enemy.health -= damage
            if enemy.health < 0:
                enemy.health = 0
            print(
                f"                      🔥  {self.name} used {item['name']} on {enemy.name} and dealt {damage} damage! Remaining HP: {enemy.health}  🔥")
            if enemy.health <= 0:
                print(f"                        ☠️  {enemy.name} has been defeated!\n")
                self.gain_xp(enemy.xp_dropped)
                self.handle_enemy_drops(enemy)

        else:
            print(f"❌ {item['name']} is not a usable item.")
            return

        item_info["count"] -= 1
        if item_info["count"] <= 0:
            print(
                f"❌ {item['name']} has been used up and removed from inventory.")
            del self.inventory[item_name]

    def handle_enemy_drops(self, enemy):
        dropped_any = False  # Flag to track if anything dropped

        for drop in enemy.drops:
            chance_range = drop.get("chance_range")
            item_key = drop["item"]
            item_obj = item_lookup.get(item_key)

            if not item_obj:
                continue  

        
            roll = random.randint(1, 100)
            if chance_range and isinstance(chance_range, tuple):
                low, high = chance_range
                if low <= roll <= high:
                    self.add_to_inventory(item_obj)
                    dropped_any = True  # Mark that something was dropped

        if dropped_any:
            print(f"                      🎁  {enemy.name} dropped some loot!")

    def display_inventory(self):
        if not self.inventory:
            print(f"{self.name}'s inventory is empty.")
        else:
            print(
                "\n          ========================================================\n")
            print(f"\n              {self.name}'s Inventory ")
            for item_info in self.inventory.values():
                item = item_info["item"]
                count = item_info["count"]
                name = item["name"]
                description = item["description"]
                print(f"  - {name} (x{count}) — {description}")
            print("         ========================================================\n")

    def attack(self, opponent):
        opponent.health -= self.attack_power
        print(
            f"          {self.name} has attacks {opponent.name} with a {self.weapon} for {self.attack_power} damage!")
        if opponent.health <= 0:
            print(
                f"                        ☠️  {opponent.name} has been defeated!\n")
            opponent.health = 0
        else:
            print(
                f"            {opponent.name} has {opponent.health} hp remaining.")

    def calculate_damage(self, base_damage, target):
        if random.randint(1, 100) <= target.defence:
            print(
                f"                        🌀 {target.name} DODGED the attack! No damage taken.\n")
            return 0

        actual_damage = base_damage
        if random.randint(1, 100) <= 10:
            crit_multiplier = random.uniform(1.1, 1.25)
            crit_damage = actual_damage * (crit_multiplier - 1)
            actual_damage += crit_damage
            print(
                f"                        💥 Critical Hit! Dealt (+{int(round(crit_damage, 1))} bonus) for a total of  {int(actual_damage)} points 💥\n")

        return int(actual_damage)

    def display_stats(self):
        if self.inventory:
            inventory_display = ', '.join(
                f"  - {info['item']['name']} (x{info['count']})"
                for info in self.inventory.values()
            )
        else:
            inventory_display = '  (Empty)'

        print(f'''                     ========================================================\n
                                {self.name}'s Stats\n  
                    Class: {self.__class__.__name__}
                    Health: {self.health} / {self.max_health} 
                    Attack Power: {self.attack_power}
                    Defence: {self.defence}
                    Level: {self.level}
                    XP: {self.xp}/{self.xp_to_next_level}
                    Inventory:
                    {inventory_display}\n
                    ========================================================
        ''')


# ========================================== Items ===========================================
small_hp_potion = {
    "name": " A Coffee 🍵",
    "type": "potion_small",
    "heal_amount": 50,
    "description": "Drink cup of coffee to stay awake.",
    "effect": "Restores 50 health points."
}

medium_hp_potion = {
    "name": "A Energy Drink 🥤",
    "type": "potion_med",
    "heal_amount": 100,
    "description": "Take a Drink to regain energy.",
    "effect": "Restores 100 health points."
}

large_hp_potion = {
    "name": "Take a Nap 🛏️",
    "type": "potion_large",
    "heal_amount": 250,
    "description": "Take a nap to restore a large amount of health.",
    "effect": "Restores 250 health points."
}

fire_ball_scroll = {
    "name": "A Codewars scroll 📜",
    "type": "fire_scroll",
    "description": "A powerful scroll that Raises your Codewar points.",
    "effect": "Deals 50 damage to an enemy.",
}


enemy_drops = [
    {"item": "small_hp_potion", "chance_range": (1, 75)},
    {"item": "medium_hp_potion", "chance_range": (1, 50)},
    {"item": "large_hp_potion", "chance_range": (1, 25)},
    {"item": "fire_ball_scroll", "chance_range": (1, 25)},
]

passing_grade_scroll = {
    "name": "Passing Grade Scroll 🎓",
    "type": "key_item",
    "description": "The final proof of surviving the Coding Temple horrors.",
    "effect": "Required to graduate and win the game."
}




item_lookup = {
    "small_hp_potion": small_hp_potion,
    "medium_hp_potion": medium_hp_potion,
    "large_hp_potion": large_hp_potion,
    "fire_ball_scroll": fire_ball_scroll,
    "passing_grade_scroll": passing_grade_scroll
}


# =========================================== Character classes ===========================================
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=150, attack_power=30,
                         defence=15, level=1, xp=0, weapon=None)
        self.weapon = "DOCTYPE Shield 🛡️"
        self.crit_chance = 5

    def attack(self, opponent):
        print("             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n")
        print(f"                                        !! {self.name} Turn !!   \n")
        print(f"                        {self.name} Slams {self.weapon}, smashing into {opponent.name} for {self.attack_power} damage!\n")
        damage = self.calculate_damage(self.attack_power, opponent)
        opponent.health -= damage
        print(f"                        ➡️   Total damage dealt to {opponent.name}: {int(damage)}\n")
        print("             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if random.randint(1, 100) <= self.crit_chance:
            pass

        if opponent.health > 0:
            print(
                f'''             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷
                
                                    {opponent.name} has {opponent.health} hp remaining.
                            
             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷\n
                  ''')


class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health=90, attack_power=55,
                         defence=0, level=1, xp=0, weapon=None)
        self.weapon = "CSS Magic Wand 🪄"
        self.crit_chance = 10

    def attack(self, opponent):

        print("             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(
            f"                                        !! {self.name} Turn !!   \n")
        print(f"                {self.name} casts @keyframe with his {self.weapon},andA giant Flaming Rock falls and hits {opponent.name} for {self.attack_power} damage!\n")
        damage = self.calculate_damage(self.attack_power, opponent)
        opponent.health -= damage
        print(
            f"                ➡️   Total damage dealt to {opponent.name}: {int(damage)}\n")
        print("             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if random.randint(1, 100) <= self.crit_chance:
            pass

        if opponent.health > 0:
            print(
                f'''             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷
                
                                    {opponent.name} has {opponent.health} hp remaining.
                            
             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷\n
                  ''')


class Rogue(Character):
    def __init__(self, name,):
        super().__init__(name, health=100, attack_power=50,
                         defence=5, level=1, xp=0, weapon=None)
        self.weapon = "Boolean Dagger 🗡️"
        self.crit_chance = 25

    def attack(self, opponent):

        print("             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(
            f"                                        !! {self.name} Turn !!   \n")
        print(
            f"                {self.name} stabs {opponent.name} with a {self.weapon}. For {self.attack_power} damage!\n")
        damage = self.calculate_damage(self.attack_power, opponent)
        opponent.health -= damage
        print(
            f"                ➡️   Total damage dealt to {opponent.name}: {int(damage)}\n")
        print("             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if random.randint(1, 100) <= self.crit_chance:
            pass

        if opponent.health > 0:
            print(
                f'''             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷
                
                                    {opponent.name} has {opponent.health} hp remaining.
                            
             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷\n
             ''')


class Archer(Character):
    def __init__(self, name,):
        super().__init__(name, health=120, attack_power=30,
                         defence=5, level=1, xp=0, weapon=None)
        print("         4. JavaScript Archer 🏹\n\n")
        self.weapon = "Array Bow "
        self.crit_chance = 10

    def attack(self, opponent):

        print("         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print(
            f"                                        !! {self.name} Turn !!   \n")
        print(
            f"                {self.name} shoots an {self.weapon} at {opponent.name} for {self.attack_power} damage\n!")
        damage = self.calculate_damage(self.attack_power, opponent)
        opponent.health -= damage
        print(
            f"                 ➡️   Total damage dealt to {opponent.name}: {int(damage)}\n")
        print("         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n")
        if random.randint(1, 100) <= self.crit_chance:
            pass
        if opponent.health <= 0:
            print(f"{self.health} / {self.max_health} hp remaining.")

        if opponent.health >0:
            print(
                f'''             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷
                
                                        {opponent.name} has {opponent.health} hp remaining.
                            
             ⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷⊷\n
                  ''')


class Enemy(Character):
    def __init__(self, name, health, attack_power, defence=0, level=1, xp_dropped=0, weapon=None, drops=None):
        super().__init__(name, health, attack_power, defence, level, weapon=weapon)
        self.xp_dropped = xp_dropped
        self.weapon = weapon
        self.crit_chance = 15
        self.drops = drops or []

    def attack(self, opponent):

        print(
            f"                        {self.name} shoots an {self.weapon} at {opponent.name} for {self.attack_power} damage!\n")
        damage = self.calculate_damage(self.attack_power, opponent)
        opponent.health -= damage
        print(
            f"                        ➡️   Total damage dealt to {opponent.name}: {int(damage)}  \n")
        print(
            f"                        {opponent.name} has {opponent.health} / {opponent.max_health} hp remaining.\n")

    def regenerate(self):
        self.health += 5
        print(
            f"                        {self.name} regenerates 5 health, now has {self.health} hp.\n")
        print(
            "             ________________________________________________________________________________________________________________")


def random_battle():
    enemy_table = [
        {
            "enemy": Enemy("Syntax Error", 100, 20, defence=5, level=1,
                           xp_dropped=20, weapon="Broken Semicolon"),
            "drops": [
            {"item": "small_hp_potion", "chance_range": (1, 75)},
            {"item": "medium_hp_potion", "chance_range": (1, 50)},
            {"item": "large_hp_potion", "chance_range": (1, 25)},
            {"item": "fire_ball_scroll", "chance_range": (1, 25)}
        ],
            "chance_range": (1, 50)
        },
        {
            "enemy": Enemy("Invalid Selectors", 120, 15, defence=10, level=1,
                           xp_dropped=30, weapon="Misplaced ID Tag"),
            "drops": [
            {"item": "small_hp_potion", "chance_range": (1, 75)},
            {"item": "medium_hp_potion", "chance_range": (1, 50)},
            {"item": "large_hp_potion", "chance_range": (1, 25)},
            {"item": "fire_ball_scroll", "chance_range": (1, 25)}
        ],
            "chance_range": (51, 65)
        },
        {
            "enemy": Enemy("Zero Division Error", 90, 20, defence=25,
                           level=1, xp_dropped=40, weapon="Division Blade"),
            "drops": [
            {"item": "small_hp_potion", "chance_range": (1, 75)},
            {"item": "medium_hp_potion", "chance_range": (1, 50)},
            {"item": "large_hp_potion", "chance_range": (1, 25)},
            {"item": "fire_ball_scroll", "chance_range": (1, 25)}
        ],
            "chance_range": (66, 85)
        },
        {
            "enemy": Enemy("Teacher wants to talk(miniboss)", 150, 25, 20, level=5,
                           xp_dropped=100, weapon="Stack of Extra Credit "),
            "drops": [
            {"item": "small_hp_potion", "chance_range": (1, 75)},
            {"item": "medium_hp_potion", "chance_range": (1, 50)},
            {"item": "large_hp_potion", "chance_range": (1, 25)},
            {"item": "fire_ball_scroll", "chance_range": (1, 25)}
        ],
            "chance_range": (86, 95)
        },
        {
            "enemy": Enemy("Failing Class(Boss)", 200, 40, defence=20, level=1,
                           xp_dropped=150, weapon="Final Github Exam"),
            "drops": [
            {"item": "small_hp_potion", "chance_range": (1, 75)},
            {"item": "medium_hp_potion", "chance_range": (1, 50)},
            {"item": "large_hp_potion", "chance_range": (1, 25)},
            {"item": "fire_ball_scroll", "chance_range": (1, 25)}
        ],
            "chance_range": (96, 100)
        }
    ]

    
    roll = random.randint(1, 100)

    for entry in enemy_table:
        low, high = entry["chance_range"]
        if low <= roll <= high:
            return entry["enemy"]

    return enemy_table[0]["enemy"]


class EvilWizard(Character):
    def __init__(self,):
        super().__init__(name="EvilWizard", health=150, attack_power=40)

    def regenerate(self):
        self.health += 5
        print(
            f"---  {self.name} regenerates 5 health, now has {self.health} hp.")

# =========================================== Character Creation ===========================================


def create_character():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('''
          \n\n          ※※※※※※※※※※※  Welcome to the Coding Temple School of Horrors!!!!  ※※※※※※※※※※※\n\n

            ''')
    while True:
        name = input(
            "          Please Enter your character's name ( or Type '9' to Exit 🚫): \n")
        if not name:
            print(
                "         You must sign up for class to play the game or Go back to being dumb!")
        elif name.lower() in ["9", "exit", "quit"]:
            print('''
                        **************************************************
                        *                                                *
                        *    You have chosen to drop out of class.       *
                        *                                                *
                        *   Thank you for playing the Coding Temple      *
                        *             School Of Horrors!!                *
                        *                                                *
                        **************************************************
                  ''')
            exit()

        else:
            break
    while True:
        print("         Choose your character:")
        print("         1. Html Warrior 🛡️")
        print("         2. CSS Mage 🧙")
        print("         3. Python Rogue 🗡️")
        print("         4. JavaScript Archer 🏹\n\n")
        print("         9.Exit Game 🚫\n")
        choice = input("         Enter the number of your choice: ").strip()

        if not choice:
            print("         You must sign up for a class to play the game!\n")
            continue

        if choice == "1" or choice == "warrior" or choice == "Warrior" or choice == "html warrior" or choice == "Html Warrior" or choice == "Html" or choice == "html":
            return Warrior(name)
        elif choice == "2" or choice == "mage" or choice == "Mage" or choice == "css mage" or choice == "Css Mage" or choice == "Css":
            return Mage(name)
        elif choice == "3" or choice == "rogue" or choice == "Rogue" or choice == "python rogue" or choice == "Python Rogue" or choice == "Python":
            return Rogue(name)
        elif choice == "4" or choice == "archer" or choice == "Archer" or choice == "javascript archer" or choice == "JavaScript Archer" or choice == "JavaScript":
            return Archer(name)
        elif choice == "9" or choice == "exit game" or choice == "Exit Game" or choice == "Exit":
            print('''
                        **************************************************
                        *                                                *
                        *    You have chosen to drop out of class.       *
                        *                                                *
                        *   Thank you for playing the Coding Temple      *
                        *             School Of Horrors!!                *
                        *                                                *
                        **************************************************
                  ''')

            exit()
        else:
            print("         Invalid choice please choose again.")


def Battle(player, enemy):

    while enemy.health > 0 and player.health > 0:
        print("""

                    -------------------------------------------------
                            What would you like to do?

                    1. Attack
                    2. Review Stats
                    3. Review Enemy Stats
                    4. Use Item
                    5. Turn in Homework and Escape\n\n\n
                    9. Drop out of Class (Exit Game)
                    -------------------------------------------------
    """)
        choice = input("Enter your choice: ")
        os.system('cls' if os.name == 'nt' else 'clear')
        if choice == "1" or choice == "attack" or choice == "Attack":
            player.attack(enemy)
            if enemy.health > 0:
                print("             ----------------------------------------------------------------------------------------------------------------\n")
                print(
                    f"                                        !! {enemy.name} Turn !!   \n")

                enemy.attack(player)

            if player.health <= 0:
                print(
                    f"                        ☠️  {player.name} has been defeated!\n")
                return

            if enemy.health > 0:
                enemy.regenerate()

        elif choice == "2" or choice == "stats" or choice == "Stats" or choice == "review stats" or choice == "Review Stats":
            player.display_stats()
        elif choice == "3" or choice == "enemy stats" or choice == "Enemy Stats" or choice == "review enemy stats" or choice == "Review Enemy Stats":
            print(f"                    Enemy: {enemy.name}")
            print(f"                    Health: {enemy.health}")
            print(f"                    Attack Power: {enemy.attack_power}")
            print(f"                    Defence: {enemy.defence}")
            print(f"                    Level: {enemy.level}")
            print(f"                    weapon: {enemy.weapon}")
        elif choice == "4" or choice == "use item" or choice == "Use Item":
            if not player.inventory:
                print(
                    f"            ❌❌❌{player.name} has not found any item, {player.name} is too scared to fight monsters  .")
                continue
            print("         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            print(
                f"                                        {player.name}'s Inventory:\n\n")

            item_list = list(player.inventory.keys())
            for i, item_name in enumerate(item_list, start=1):
                item = player.inventory[item_name]["item"]
                count = player.inventory[item_name]["count"]
                print(
                    f"          {i}. {item['name']} (x{count}) -- {item['description']} -- {item.get('effect', '')}")

            print("         ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n")
            print("          9. Cancel / Exit back to game\n\n")
            item_choice = input("Enter the number of your choice: ")
            os.system('cls' if os.name == 'nt' else 'clear')

            if not item_choice.isdigit():
                print(
                    "         Invalid input. Please enter a number ( you know the things on the top row of your keyboard).")
                continue
            if item_choice == "9" or item_choice.lower() == "cancel" or item_choice.lower() == "exit":
                print(
                    f"                    📕  {player.name} Choose to study and not use an item.")
                continue

            try:
                item_index = int(item_choice) - 1
                if 0 <= item_index < len(item_list):
                    selected_item = item_list[item_index]
                    player.use_item(selected_item, enemy=enemy)
                    if selected_item in player.inventory:
                        item = player.inventory[selected_item]["item"]
                        if item["type"] in ["potion_small", "potion_med", "potion_large"]:
                            pass

                else:
                    print("         Invalid choice. Please try again.")
            except ValueError:
                print(
                    "         Invalid input. Please enter a number corresponding to the item.")

        elif choice == "5" or choice == "escape" or choice == "Escape":
            if random.randint(1, 100) <= 20:
                print(
                    "                  You Turned in your Homework and escaped the battle!  ")
                return
            else:
                print(
                    f"\n                  {player.name} Missed the deadline and failed to Escape!    ")
                print(
                    f"                         {player.name} loses -5 hp !                   \n")
                player.health -= 5
                if player.health <= 0:
                    print("         ================================================")
                    print(
                        "         ************************************************\n\n")
                    print(
                        f"          ---  {player.name} has Failed the class! Game Over.  ---\n\n")
                    print("         ************************************************")
                    print("         ================================================")
                    print("\n         Do you want to continue battling? (yes/no)")
                    print("         1. Yes")
                    print("         2. No")
                    print("         ================================================")
                    choice = input("            Enter your choice: ")
                    os.system('cls' if os.name == 'nt' else 'clear')
                    if choice.lower() in ["yes", "1", "y"]:
                        print("         Starting a new battle...")
                        return main()
                    elif choice.lower() in ["no", "2", "n"]:
                        print("         Exiting the game.")
                        exit()
                    else:
                        print("         Invalid choice. Please try again.")
                else:
                    continue  # continue battle

        elif choice == "9" or choice == "drop out" or choice == "Drop Out":
            print('''
                            **************************************************
                            *                                                *
                            *    You have chosen to drop out of class.       *
                            *                                                *
                            *   Thank you for playing the Coding Temple      *
                            *             School Of Horrors!!                *                     
                            *                                                *
                            **************************************************               
                  ''')

            exit()
        else:
            print("         Invalid choice. Please try again.")

        if enemy.health <= 0:
            print(
                f"                      ☠️   {enemy.name} has been defeated! {player.name} gains {enemy.xp_dropped} XP.\n")
            player.gain_xp(enemy.xp_dropped)
            player.handle_enemy_drops(enemy)


def main():
    player = create_character()
    os.system('cls' if os.name == 'nt' else 'clear')
    while True:
        if "passing_grade_scroll" in player.inventory:
            print('''
                🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓

                        You obtained the Passing Grade Scroll!
                        You passed the Coding Temple School of Horrors!

                        🎉🎉🎉🎉🎉  CONGRATULATIONS! YOU WIN! 🎉🎉🎉🎉🎉

                🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓🎓
                ''')
            exit()
        
        enemy = random_battle()
        print("                    ==================================================\n")
        print(f"\n                       A wild {enemy.name} appears! ")
        Battle(player, enemy)

        if player.health <= 0:

            print("         ************************************************\n\n")
            print(
                f"            ----  ☠️  {player.name} has been defeated! Game Over.  ----\n\n")
            print("         ************************************************")
            print("\n\n         ================================================")
            print("\n           Do you want to continue battling? (yes/no)")
            print("         1. Yes")
            print("         2. No")
            print("         ================================================")
            choice = input("            Enter your choice: ")
            os.system('cls' if os.name == 'nt' else 'clear')
            if choice.lower() == "yes" or choice == "1" or choice == "y":
                print("         Starting a new battle...")
                return main()
            elif choice.lower() == "no" or choice == "2" or choice == "n":
                print("         Exiting the game.")
                exit()
            else:
                print("         Invalid choice. Please try again.")
    
            


main()
