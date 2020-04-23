# Write your code here
import random


def generate_rules(choices):
    """
    input: a list of choices(options as a string)
    output: a dictionary of rules for the game

    This method Generates a random dictionary or rules
    that by rotation of choices.
    """
    rules = {}
    counter_1 = 1
    counter_2 = counter_1
    no_of_choices = len(choices)

    for choice in choices:
        rules[choice] = []
        counter_2 = counter_1
        for x in range(no_of_choices // 2):
            rules[choice].append(choices[counter_2 % no_of_choices])
            counter_2 += 1
        counter_1 += 1

    return rules


def game_loop(rules, rating):
    """
    This method runs the game loop:
        - Calculates score
        - Checks input
    """
    print("Okay, let's start")
    while True:
        validity = False
        try:
            # user_choice = input("Enter your choice: ")
            user_choice = input()
        except EOFError:
            pass

        computer_choice = random.choice(list(rules.keys()))

        if user_choice == "!exit":
            print("Bye!")
            break
        elif user_choice == "!rating":
            print(f"Your rating: {rating}")
            continue
        elif user_choice in list(rules.keys()):
            validity = True

        if validity:
            validity = False
            if user_choice == computer_choice:
                print(f"There is a draw ({user_choice})")
                rating += 50
            elif computer_choice in rules[user_choice]:
                print(f"Well done. Computer chose {computer_choice} and failed")
                rating += 100
            elif user_choice in rules[computer_choice]:
                print(f"Sorry, but computer chose {computer_choice}")
        else:
            print("Invalid input")
    return rating


def main():
    # Open records file and import into dictionary records{}
    f_rating = open("rating.txt", "r")
    record = {}
    for line in f_rating:
        rec = line.split()
        key, value = rec[0], int(rec[1])
        record[key] = value

    # print("Welcome to C H A O T I C Rock-Paper-Scissors")
    # print("Everything here is random nonsense, but follow the RULES")
    name = input("Enter your name: ")
    print(f"Hello, {name}")

    # Checks in record if a previous record exists.
    if name in record.keys():
        rating = record[name]
    else:
        rating = 0
    # print("Your rating: " + str(rating))

    # options = input("Enter the list of playable actions with comma"
    #               + "(Ex: rock,paper,scissors,lizard,spock): ")

    options = input()
    choices = options.split(",")
    choices.reverse()
    # print(choices)
    # random.shuffle(choices)
    rules = generate_rules(choices)
    if options == "":
        rules = {"rock": ["scissors"], "paper": ["rock"], "scissors": ["paper"]}
    # print("The game rules are: ")
    # print(rules)
    # print("To end game, enter !exit\nTo view score, enter !rating")

    rating = game_loop(rules, rating)
    # print(f"Your final score was: {rating}")

    f_rating.close()


if __name__ == "__main__":
    main()
