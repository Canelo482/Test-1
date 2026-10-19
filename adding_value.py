
num1 = 10  # num1 is in the global namespace

def add_numbers():
    num2 = int(input("Enter a number: "))  # num2 is in the local namespace of add_numbers
    total = num1 + num2  # total is in the local namespace of add_numbers
    print(total)

add_numbers()
