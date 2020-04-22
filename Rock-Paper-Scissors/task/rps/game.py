# Write your code here
import random

rules = {"rock": "paper", "scissors": "rock", "paper": "scissors"}
validity = False

f_rating = open("rating.txt", "r")
record = {}

for line in f_rating:
    rec = line.split()
    key, value = rec[0], int(rec[1])
    record[key] = value

name = input("Enter your name: ")
print(f"Hello, {name}")

if name in record.keys():
    print("Your rating: " + str(record[name]))
    rating = record[name]
else:
    rating = 0

while True:
    try:
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
        elif user_choice == rules[computer_choice]:
            print(f"Well done. Computer chose {computer_choice} and failed")
            rating += 100
        elif computer_choice == rules[user_choice]:
            print(f"Sorry, but computer chose {computer_choice}")
    else:
        print("Invalid input")

f_rating.close()
