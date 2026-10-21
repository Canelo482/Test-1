# This function takes a temperature in Celsius and returns it in Fahrenheit.
def celsius_to_fahrenheit(celsius):
    return (1.8 * celsius) + 32

# This function takes a temperature in Fahrenheit and returns it in Celsius.
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

# Get a Celsius temperature from the user and convert it to Fahrenheit.
try:
    celsius = float(input("Enter a temperature in Celsius: "))
    print(celsius_to_fahrenheit(celsius))
except ValueError:
    print("That isn't a valid number!")

# Get a Fahrenheit temperature from the user and convert it to Celsius.
try:
    fahrenheit = float(input("Enter a temperature in Fahrenheit: "))
    print(fahrenheit_to_celsius(fahrenheit))
except ValueError:
    print("That isn't a valid number!")
