def ask_options(question, options):
    answer ="" 
    while answer not in options:
        answer = input(question).lower()
        if answer not in options:
            print("Please answer with one of the following: " + ", ".join(options))
    return answer

products = []
while True:
    product_type = input("What product do you want to sell? (or type 'done' to finish) ")
    if product_type.lower() == "done":
        break
    size = ask_options("What size? (small/medium/large) ", ["small", "medium", "large"])
    color = ask_options("What color? (red/blue/green) ", ["red", "blue", "green"])
    address = input("What is the delivery address? ")
    products.append((product_type, size, color, address))

print("\nYour listed products:")
for product in products:
    print(f"Product: {product[0]}, Size: {product[1]}, Color: {product[2]}, Address: {product[3]}")