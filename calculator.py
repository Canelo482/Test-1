num1 = 0
num2 = 0

def add():
    global num1, num2
    print(str(num1) + " + " + str(num2) + " = " + str(num1 + num2))

def subtract():
    global num1, num2
    print(str(num1) + " - " + str(num2) + " = " + str(num1 - num2))

def multiply():
    global num1, num2
    print(str(num1) + " * " + str(num2) + " = " + str(num1 * num2))

num1 = int(input("What is the first number?: "))
num2 = int(input("What is the second number?: "))
operation = input("Choose an operation (add, subtract, multiply): ")

if operation == "add":
    add()
elif operation == "subtract":
    subtract()
elif operation == "multiply":
    multiply()
else:
    print("Invalid operation! Please choose add, subtract, or multiply.")
