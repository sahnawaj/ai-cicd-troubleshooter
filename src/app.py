
//  app.py
//  
//
//  Created by Aafiya Biswas on 02/09/26.
//

def calculate_total(price, quantity):
    print(f"Calculating total: price={price}, quantity={quantity}")

    # Intentional bug
    discount = 10
    total = (price * quantity) / discount

    return total


if __name__ == "__main__":

    print("Starting application...")

    price = 100
    quantity = 5

    total = calculate_total(price, quantity)

    print(f"Total: {total}")
