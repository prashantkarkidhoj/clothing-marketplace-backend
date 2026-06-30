from products import Product

class seller:
    def __init__(self,name,shop,area):
        self.name = name
        self.shop = shop
        self.area = area
        self.products = []

    def add_product(self,product):
        self.products.append(product)

    def show_products(self):
        print(f"Products for {self.shop}:")
        for product in self.products:
            print(f"  - {product.name} | {product.size} | {product.color} | Qty: {product.quantity}")

    def reduce_quantity(self, product_name, amount):
        for product in self.products:
            if product.name == product_name:
                if product.quantity >= amount:
                    product.quantity -= amount
                    print(f"Reduced {amount} from {product.name}. New quantity: {product.quantity}")
                else:
                    print(f"Not enough quantity of {product.name} to reduce by {amount}.")
                return
        print(f"Product {product_name} not found.")
class order:
    def __init__(self, buyer_name, seller, product, quantity):
        self.buyer_name = buyer_name
        self.seller = seller
        self.product = product
        self.quantity = quantity
        self.status = "pending"

    def show_order(self):
        print(f"Order: {self.product.name} | Qty: {self.quantity}")
    
    def update_status(self, status):
        self.status = status
        print(f"Order status updated to: {self.status}")
    
    def describe_order(self):
        print(f"Order Details: {self.product.name} | Size: {self.product.size} | Color: {self.product.color} | Qty: {self.quantity}")

ram = seller("Ram", "Ram's Clothing", "Kathmandu")

ram.add_product(Product("shirt", "medium", "red", 10))
ram.add_product(Product("pants", "large", "blue", 5))
ram.add_product(Product("jacket", "small", "black", 2))

ram.reduce_quantity("shirt", 3)
ram.reduce_quantity("pants", 2)
ram.reduce_quantity("jacket", 1)
ram.show_products()

order1 = order("Sita", ram, ram.products[0], 2)
order1.describe_order()
order1.update_status("shipped")
order1.describe_order()