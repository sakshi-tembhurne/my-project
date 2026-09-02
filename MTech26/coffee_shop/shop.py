from  numpy import MENU                                                   # How to use MENU variable from menu.py file??


class CoffeeShop:

    def __init__(self):
        pass                                                        # What variable should i hold here?

    def display_menu(self):
        print("\n========== MENU ==========")
        print("1. Coffee")
        print("2. Juices")
        print("3. Starters")
        print("4. Soups")

    def display_category(self, category):

        if category == "":                                          # Add something here
            print("\n--- COFFEE ---")

            for item, price in self.menu["coffee"].items():
                print(f"{item.title()} - ₹{price}")

        elif category == "":                                        # Add something here
            print("\n--- JUICES ---")

            for item, price in self.menu["juice"].items():                                      # How do you iterate over a dictionary to print the available juice items
                print(f"{item.title()} - ₹{price}")

        elif category == "starters":
            print("\n--- STARTERS ---")

            for item, price in self.menu["starters"].items():
                print(f"{item.title()} - ₹{price}")

        elif category == "soups":
            print("\n--- SOUPS ---")

            for item, price in self.menu["soups"].items():
                print(f"{item.title()} - ₹{price}")

                                                                    # Do we need an "else" here

    def order(self, category, item, quantity):

        if category in self.menu:                                            # What is to be added to check here?

            if item in self.menu[category]:
                price = self.menu[category][item]
                return price * quantity

            else:
                print("Item not available!")

        else:
            print("Category not available!")

        return None