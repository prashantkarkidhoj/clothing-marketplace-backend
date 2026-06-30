# Question 1
ownership = ""
while ownership != "yes" and ownership != "no":
    ownership = input("Do you own a restaurant? (yes/no) ").lower()
    if ownership != "yes" and ownership != "no":
        print("Please type yes or no only.")

# Yes path
if ownership == "yes":
    share = ""
    while share != "fully" and share != "partially":
        share = input("Do you fully or partially own it? (fully/partially) ").lower()
        if share != "fully" and share != "partially":
            print("Please type fully or partially only.")
    
    if share == "fully":
        print("You should buy a new restaurant.")
    elif share == "partially":
        print("You should consider buying full ownership.")

# No path — YOUR JOB
elif ownership == "no":
    new=""
    while new !="yes" and new !="no":
        new = input("do you have a new restaurant in mind?(yes/no)").lower()
        if new!="yes" and new!="no":
            print("please answer in yes and no only.")
    if new=="yes":
        profit=""
        while profit!="yes" and profit!="no":
            profit = input("do you think it will be profitable?(yes/no)").lower()
            if profit!="yes" and profit!="no":
                print("please answer in yes and no only.")
    
        if profit=="yes":
            print("you should buy the restaurant.")
        elif profit=="no":
            print("you should not buy the restaurant.")
    elif new=="no":
        print("you should not buy a restaurant.")
    
    