#def calculate_total(price, quantity):
#    print(f"Calculating total: price={price}, quantity={quantity}")
#
#    discount = 0
#    total = (price * quantity) / discount
#
#    return total
#
#
#if __name__ == "__main__":
#
#    print("Starting application...")
#
#    price = 100
#    quantity = 5
#
#    total = calculate_total(price, quantity)
#
#    print(f"Total: {total}")


import pandas


def process_data():
    data = pandas.DataFrame({
        "name": ["Alice", "Bob"],
        "score": [90, 85]
    })

    print(data)


if __name__ == "__main__":
    print("Starting application...")
    process_data()
