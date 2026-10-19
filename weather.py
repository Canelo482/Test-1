def sunny():
    print("On a sunny day, sandals are appropriate footwear.")


def rainy():
    print("On a rainy day, galoshes are appropriate footwear.")


def snowy():
    print("On a snowy day, boots are appropriate footwear.")


weather = input("What is the weather? (sunny, rainy, snowy): ").strip().lower()

if weather == "sunny":
    sunny()
elif weather == "rainy":
    rainy()
elif weather == "snowy":
    snowy()
else:
    print("Invalid option! Please choose sunny, rainy, or snowy.")
