def ask_options(question, options):
    answer ="" 
    while answer not in options:
        answer = input(question).lower()
        if answer not in options:
            print("Please answer with one of the following: " + ", ".join(options))
    return answer
ownership = ask_options("Do you own a restaurant? (yes/no) ", ["yes", "no"])
if ownership == "yes":
    share = ask_options("Do you fully or partially own it? (fully/partially) ", ["fully", "partially"])
    if share == "fully":
        print("You should buy a new restaurant.")
    elif share == "partially":
        print("You should consider buying full ownership.")
elif ownership == "no":
    new = ask_options("Do you have a new restaurant in mind? (yes/no) ", ["yes", "no"])
    if new == "yes":
        profit = ask_options("Do you think it will be profitable? (yes/no) ", ["yes", "no"])
        if profit == "yes":
            print("You should buy the restaurant.")
        elif profit == "no":
            print("You should not buy the restaurant.")
    elif new == "no":
        print("You should start researching restaurants to buy.")