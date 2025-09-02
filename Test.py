import math
import random

def base_two(expo):
    product = 2**expo
    return product

def quiz():
    while True:
        expo = random.randint(1, 9)
        product = base_two(expo)
        print(f"""What is 2^{expo}?""")
        player_input = input()
        if int(player_input) == product:
            print("""Good job!""")
            
        elif int(player_input) != product:
            print(f"""Wrong, the correct answer is {product}.""")

quiz()