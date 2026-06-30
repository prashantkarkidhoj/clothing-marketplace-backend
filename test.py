
def ask_numbers (question):
    answer ="" 
    while not answer.isdigit():
        answer = input(question)
        if not answer.isdigit():
            print("please only enter number")
    return answer

quantity = ask_numbers("How many products do you want to sell? ")
print(f"You want to sell {quantity} products.")
