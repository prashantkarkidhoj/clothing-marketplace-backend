import json

def ask_options(question, options):
    answer ="" 
    while answer not in options:
        answer = input(question).lower()
        if answer not in options:
            print("Please answer with one of the following: " + ", ".join(options))
    return answer

def ask_numbers (question):
    answer ="" 
    while not answer.isdigit():
        answer = input(question)
        if not answer.isdigit():
            print("please only enter number")
    return answer

seller = {
    "name": input('Enter your name: '),
    "shop": input('Enter your shop name: '),
    "area": input('Enter your area: '),
    "products": []  # empty list, will fill with products
}
seller["products"] = []

while True:
    product_name = input("\nEnter product name (or 'done' to finish): ")
    if product_name.lower() == "done":
        break
    
    product = {
        "name": product_name,
        "size": ask_options("Size (small/medium/large): ", ["small", "medium", "large"]),
        "color": ask_options("Color (red/blue/green): ", ["red", "blue", "green"]),
        "quantity": ask_numbers("How many products do you want to sell? ")
    }
    
    seller["products"].append(product)

print("\n--- Complete Seller Profile ---")
print(f"Seller: {seller['name']} | Shop: {seller['shop']} | Area: {seller['area']}")
print(f"Total Products: {len(seller['products'])}")
for product in seller["products"]:
    print(f"- {product['name']} | Size: {product['size']} | Color: {product['color']} | Qty: {product['quantity']}")

try:
    with open("sellers.json", "r") as f:
        all_sellers = json.load(f)
except:
    all_sellers = []

all_sellers.append(seller)

with open("sellers.json", "w") as f:
    json.dump(all_sellers, f, indent=4)

print("\nSeller data saved to sellers.json")