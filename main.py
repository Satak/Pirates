
import os
import cmd
import random

COORDINATES = random.randint(100000, 999999)
COORDINATES = 1
def main():
    """main"""

    # Data
    bank = [
        {
            "owner": "Jack", 
            "deposits": 0
        },
        {
            "owner": "James", 
            "deposits": 0
        }
    ]

    gun = {
        "name": "gun",
        "value": 300,
        "max_damage": 30,
        "loaded": False
    }

    bullets = {
        "name": "bullets",
        "value": 100,
        "amount": 10
    }

    normal_map = {
        "name": "normal_map",
        "value": 3
    }

    pen = {
        "name": "pen",
        "value": 3
    }

    rum = {
        "name": "rum",
        "value": 10,
        "drunk": False
    }

    alligator = {
        "name": "alligator",
        "health": 30,
        "max_damage": 30,
        "defence": 6
    }

    treasure = {
        "name": "treasure",
        "value": 1000,
        "found": False
    }

    person_list = [
        {
            "name": "Jack",
            "lastname": "Sparrow",
            "age": 35,
            "occupation": "Pirate",
            "gold": 0,
            "inventory": [rum, normal_map],
            "say": "Yarrrr",
            "health": 100,
            "defence": 14,
            "drunk": False
        },{
            "name": "James",
            "lastname": "Hook",
            "age": 59,
            "occupation": "Pirate",
            "gold": 100,
            "inventory": [bullets, gun],
            "say": "Yarrrr",
            "health": 100,
            "defence": 13,
            "drunk": False
        },{
            "name": "Sailor",
            "lastname": "Drunken",
            "age": 45,
            "occupation": "Sailor",
            "gold": 10,
            "inventory": [pen],
            "say": "Yarrrr",
            "health": 100,
            "defence": 7,
            "drunk": False
        }
    ]

    # Functions
    def treasure_hunt(coordinates, person):
        if coordinates == COORDINATES and not treasure["found"]:
            if alligator["health"] > 0:
                print("You found a treasure! But it's guarded by the alligator")
                option = input("1.) Shoot it\n2.) Go back\n\n")
                if option == "1":
                    shot = shoot(person, alligator)
                    if not shot:
                        attack_roll = random.randint(1, 20)
                        roll = random.randint(1, alligator["max_damage"])
                        
                        if attack_roll > person["defence"]:
                            if roll < person["health"]:
                                person["health"] -= roll
                                print(f"Alligator bit {person['name']} by {roll} points of damage")
                            else:
                                person["health"] = 0
                                print(f"{person['name']} was eaten by the alligator")
                        else:
                            print(f"Alligator missed {person['name']}, maybe you are not so lucky next time")

                elif option == "2":
                    print("You run back from the jungle...")
                else:
                    treasure_hunt(coordinates, person)
            else:
                if not treasure["found"]:
                    print(f"{person['name']} found the treasure!")
                    treasure["found"] = True
                    person["inventory"].append(treasure)
                else:
                    print("Nothing in this coordinate...")
        else:
            print("Nothing in this coordinate...")

    def look(item_name, person):
        item_found = [item for item in person["inventory"] if item["name"] == item_name]
        if len(item_found) > 0:
            if "coordinates" in item_found[0]:
                print(f"You see coordinates: {item_found[0]['coordinates']}")
            else:
                print(f"You just see item {item_found[0]['name']}")
        else:
            print(f"{person['name']} doesn't have items to draw...")

    def draw(person):
        map_found = [item for item in person["inventory"] if item["name"]  == "normal_map"]
        pen_found = [item for item in person["inventory"] if item["name"]  == "pen"]
        if len(map_found) > 0 and len(pen_found) > 0:
            print(f"{person['name']} successfully draw a valuable treasure map")
            map_found[0]["name"] = "treasure_map"
            map_found[0]["coordinates"] = COORDINATES
            map_found[0]["value"] = 100
        else:
            print(f"{person['name']} doesn't have items to draw...")

    def steal(item_name, stealer, target):
        item_found = [item for item in target["inventory"] if item["name"] == item_name]
        if len(item_found) > 0:
            if target["drunk"]:
                print(f"{stealer['name']} (stealer) successfully stealed '{item_name}' from {target['name']} (target)")
                target["inventory"].remove(item_found[0])
                stealer["inventory"].append(item_found[0])
            else:
                print(f"Target person {target['name']} is too alert being stolen")
        else:
            print(f"Target person {target['name']} doesn't have item named '{item_name}'")
    
    def drink(item_name, person):
        item_found = [item for item in person["inventory"] if item["name"] == item_name and item["name"] == "rum"]

        if len(item_found) > 0 and not item_found[0]["drunk"]:
            print(f"{person['name']} drunk '{item_name}' and is now drunk. Rum bottle doesn't have any value now.")
            item_found[0]["drunk"] = True
            item_found[0]["value"] = 0
            person["drunk"] = True
        else:
            print(f"{person['name']} doesn't have drinkable item name '{item_name}'")

    def get_person(name, person_list):
        person = [person for person in person_list if person["name"] == name and person["health"] > 0]

        if len(person) > 0:
            return person[0]
        else:
            print(f"Alive person named '{name}' not found from the person list")
            return None

    def balance(person):
        bank_account = [account for account in bank if account["owner"] == person["name"]]

        if len(bank_account) > 0:
            print(f"{person['name']} has {bank_account[0]['deposits']} gold in bank" )
        else:
            print(f"Sorry, we can't find an account for the name '{person['name']}'")

    def deposit(amount, person):
        bank_account = [account for account in bank if account["owner"] == person["name"]]
        if isinstance(amount, int ) and person["gold"] >= amount:
            if len(bank_account) > 0:
                bank_account[0]['deposits'] += amount
                person['gold'] -= amount
                print(f"{person['name']} successfully deposited {amount} gold to bank")
                print(f"Bank has now {bank_account[0]['deposits']} gold and the user have {person['gold']} gold")
            else:
                print(f"Sorry, we can't find an account for the name '{person['name']}'")
        else:
            print(f"Can't deposit that much gold ({amount}), {person['name']} have only {person['gold']} gold")

    def withdraw(amount, person):
        bank_account = [account for account in bank if account["owner"] == person["name"]]
        if isinstance(amount, int ) and len(bank_account) > 0:
            if bank_account[0]['deposits'] >= amount:
                bank_account[0]['deposits'] -= amount
                person['gold'] += amount
                print(f"{person['name']} successfully withdraw {amount} gold from bank")
                print(f"Bank has now {bank_account[0]['deposits']} gold and the user have {person['gold']} gold")
            else:
                print(f"Can't withdraw that much gold ({amount}), bank account have only {bank_account[0]['deposits']} gold")
        else:
            print(f"Sorry, we can't find an account for the name '{person['name']}'")

    def sell(seller, buyer, item_name):
        item_found = [item for item in seller["inventory"] if item["name"] == item_name]
        if len(item_found) > 0:
            print(f"{seller['name']} (seller) have an item named '{item_name}' with value {item_found[0]['value']} gold")
            if buyer["gold"] >= item_found[0]["value"]:
                print(f"Item can be sold for {item_found[0]['value']} gold")
                seller["inventory"].remove(item_found[0])
                buyer["inventory"].append(item_found[0])
                buyer["gold"] -= item_found[0]["value"]
                seller["gold"] += item_found[0]["value"]
                print(f"Item sold successfully to {buyer['name']} (buyer). {seller['name']} (seller) now has now total {seller['gold']} gold")
            else:
                print(f"{buyer['name']} (buyer) doesn't have enough money ({buyer['gold']} gold) to buy this item ({item_found[0]['value']} gold)")
        else:
            print(f"{seller['name']} (seller) doesn't have item named '{item_name}'")

    def shoot(shooter, target):
        gun_found = [item for item in shooter["inventory"] if item["name"] == "gun"]
        bullet_found = [item for item in shooter["inventory"] if item["name"] == "bullets"]

        if len(gun_found) > 0 and len(bullet_found) > 0:
            if target["health"] > 0:
                if bullet_found[0]["amount"] > 0:
                    bullet_found[0]["amount"] -= 1
                    print(f"{shooter['name']} shoots {target['name']}, bullets left: {bullet_found[0]['amount']}")
                    attack_roll = random.randint(1, 20)
                    if attack_roll > target["defence"]:
                        roll = random.randint(1, gun_found[0]["max_damage"])
                        if roll > target["health"]:
                            target["health"] = 0
                        else:
                            target["health"] -= roll
                        print(f"{shooter['name']} (shooter) shot {target['name']} (target) {roll} points of damage (health left: {target['health']})")

                    else:
                        print(f"{shooter['name']} (shooter) missed the shot ({attack_roll}/{target['defence']})")
                    # person shot
                    return True
                else:
                    print("Bullets are out")
            else:
                print(f"{shooter['name']} (shooter) can't shoot {target['name']} (target) because it's dead")
        else:
            print(f"{shooter['name']} doesn't have gun or bullets")

    # CMD module
    class Game(cmd.Cmd):
        """Game command loop"""
        os.system("cls")
        intro = 'Welcome to the Game shell. Type help or ? to list commands.\n'
        prompt = '==> '

        def do_treasure_hunt(self, args):
            """treasure_hunt <coordinates: int> <person_name: str>"""
            os.system("cls")

            if " " in args:
                coordinates, person_name = args.split(" ")
                person = get_person(person_name, person_list)

                if person:
                    treasure_hunt(int(coordinates), person)
            else:
                print("treasure_hunt <coordinates: int> <person_name: str>")
 
        def do_look(self, args):
            """look <item_name: str> <person_name: str>"""
            os.system("cls")

            if " " in args:
                item_name, person_name = args.split(" ")
                person = get_person(person_name, person_list)

                if person:
                    look(item_name, person)
            else:
                print("look <item_name: str> <person_name: str>")

        def do_drink(self, args):
            """drink <item_name: str> <person_name: str>"""
            os.system("cls")

            if " " in args:
                item_name, person_name = args.split(" ")
                person = get_person(person_name, person_list)

                if person:
                    drink(item_name, person)
            else:
                print("drink <item_name: str> <person_name: str>")

        def do_draw(self, person_name):
            """draw <person_name: str>"""
            os.system("cls")
            if person_name:
                person = get_person(person_name, person_list)
                if person:
                    draw(person)
            else:
                print("draw <person_name: str>")

        def do_shoot(self, args):
            """shoot <shooter_name: str> <target_name: str>"""
            os.system("cls")

            if " " in args:
                shooter_name, target_name = args.split(" ")
                shooter = get_person(shooter_name, person_list)
                target = get_person(target_name, person_list)

                if shooter and target:
                    shoot(shooter, target)
            else:
                print("shoot <shooter_name: str> <target_name: str>")

        def do_steal(self, args):
            """steal <item_name: str> <stealer_name: str> <target_name: str>"""
            os.system("cls")

            if " " in args:
                item_name, stealer_name, target_name = args.split(" ")
                stealer = get_person(stealer_name, person_list)
                target = get_person(target_name, person_list)

                if stealer and target:
                    steal(item_name, stealer, target)
            else:
                print("steal <item_name: str> <stealer_name: str> <target_name: str>")
        def do_sell(self, args):
            """sell <seller_name: str> <buyer_name: str> <item_name: str>"""
            os.system("cls")

            if " " in args:
                seller_name, buyer_name, item_name = args.split(" ")
                seller = get_person(seller_name, person_list)
                buyer = get_person(buyer_name, person_list)

                if seller and buyer:
                    sell(seller, buyer, item_name)
            else:
                print("sell <seller_name: str> <buyer_name: str> <item_name: str>")

        def do_balance(self, person_name):
            """balance <person_name: str>"""
            os.system("cls")
            person = get_person(person_name, person_list)
            if person:
                balance(person)

        def do_deposit(self, args):
            """deposit <amount: int> <person_name: str>"""
            os.system("cls")

            if " " in args:
                amount, person_name = args.split(" ")
                person = get_person(person_name, person_list)

                if person:
                    deposit(int(amount), person)
            else:
                print("syntax: deposit <amount: int> <person_name: str>")

        def do_withdraw(self, args):
            """withdraw <amount: int> <person_name: str>"""
            os.system("cls")

            if " " in args:
                amount, person_name = args.split(" ")
                person = get_person(person_name, person_list)

                if person:
                    withdraw(int(amount), person)
            else:
                print("syntax: withdraw <amount: int> <person_name: str>")

        def do_persons(self, args):
            """Lists all persons and their items"""
            os.system("cls")

            for person in person_list:
                print(f"Name: {person['name']}\nDrunk: {person['drunk']}\nHealth: {person['health']}\nGold: {person['gold']} g")
                if len(person["inventory"]) > 0:
                    print("Items:")
                    for item in person["inventory"]:
                        print(f"\t{item['name']}, {item['value']} gold")
                print("\n")

        def do_exit(self, args):
            """Exit the program"""
            return True
    
    Game().cmdloop()
main()
