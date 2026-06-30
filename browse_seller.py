import json

try:
    with open("sellers.json", "r") as f:
        all_sellers = json.load(f)
except:
    print("No sellers found.")
    exit()

print(f"\n--- {len(all_sellers)} Sellers on the Platform ---\n")

for seller in all_sellers:
    print(f"Shop: {seller['shop']} | Owner: {seller['name']} | Area: {seller['area']}")
    print(f"Products: {len(seller['products'])}")
    for product in seller['products']:
        print(f"  - {product['name']} | {product['size']} | {product['color']} | Qty: {product['quantity']}")
    print()  

    search = input("\nSearch for a product (or press enter to skip): ").lower()

if search:
    print(f"\n--- Results for '{search}' ---\n")
    found = False
    for seller in all_sellers:
        for product in seller['products']:
            if search.lower() in product['name'].lower():
                print(f"Shop: {seller['shop']} | Area: {seller['area']}")
                print(f"  - {product['name']} | {product['size']} | {product['color']} | Qty: {product['quantity']}")
                found = True
    if not found:
        print("No products found.")                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   