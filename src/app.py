#
//  app.py
//  
//
//  Created by Aafiya Biswas on 02/09/26.
//

def calculate_total():
    price = 100
    quantity = 5

    # Intentional bug
    return price / 0


if __name__ == "__main__":
    print("Starting application...")
    total = calculate_total()
    print(f"Total: {total}")
