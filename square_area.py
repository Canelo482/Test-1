def calculate_area(side_length=10):
    area = side_length * side_length
    print("The area of a square with sides of length " + str(side_length) + " is " + str(area) + ".")


length = int(input("Enter side length: "))

if length <= 0:
    print("Let's use 10 instead:")
    calculate_area()
else:
    calculate_area(length)
