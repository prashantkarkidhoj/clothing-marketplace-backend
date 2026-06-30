import json

with open("sellers.json", "r") as f:
    all_sellers = json.load(f)

print("\n--- Sellers ---")
for i, seller in enumerate(all_sellers):
    print(f"{i + 1}. {seller['shop']} — {seller['name']}")

choice = int(input("\nSelect a seller number: ")) - 1
selected = all_sellers[choice]

print(f"\nManaging: {selected['shop']}")
print("\nProducts:")
for i, product in enumerate(selected['products']):
    print(f"{i + 1}. {product['name']} | {product['size']} | {product['color']} | Qty: {product['quantity']}")

action = input("\nWhat do you want to do? (update/delete): ").lower()

product_choice = int(input("Select product number: ")) - 1
selected_product = selected['products'][product_choice]

if action == "update":
    new_qty = input(f"New quantity for {selected_product['name']}: ")
    selected_product['quantity'] = new_qty
    print(f"Updated quantity to {new_qty}.")

elif action == "delete":
    removed = selected['products'].pop(product_choice)
    print(f"Deleted {removed['name']} from {selected['shop']}.")

with open("sellers.json", "w") as f:
    json.dump(all_sellers, f, indent=4)

print("Changes saved.")