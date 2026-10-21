def retrieve_positive_number():
    while True:
        try:
            number = int(input("Enter a positive number: "))
            if number > 0:
                return number
            print("The number must be positive!")
        except ValueError:
            print("That wasn't a number!")


print(retrieve_positive_number())
