import json

with open("sellers.json", "r") as f:
    seller = json.load(f)

print(f"Seller: {seller['name']}")
print(f"Shop: {seller['shop']}")
print(f"Area: {seller['area']}")
print(f"\nProducts:")
for product in seller["products"]:
    print(f"- {product['name']} | Size: {product['size']} | Color: {product['color']} | Qty: {product['quantity']}")