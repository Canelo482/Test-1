# Write your function for converting Celsius to Fahrenheit here.
# Make sure to include a comment at the top that says what
# each function does!

# This function takes a temperature in Celsius and returns it in Fahrenheit.
def celsius_to_fahrenheit(celsius):
    return (1.8 * celsius) + 32

# Now write your function for converting Fahrenheit to Celsius.

# This function takes a temperature in Fahrenheit and returns it in Celsius.
def fahrenheit_to_celsius(fahrenheit):
    return (fahrenheit - 32) / 1.8

# Now change 0C to F:
print(celsius_to_fahrenheit(0.0))

# Change 100C to F:
print(celsius_to_fahrenheit(100.0))

# Change 40F to C:
print(fahrenheit_to_celsius(40.0))

# Change 80F to C:
print(fahrenheit_to_celsius(80.0))
