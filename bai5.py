# Lab Session 1 - Bai 5: Tim mau yeu thich trong danh sach
colors = ["Blue", "Yellow", "Pink", "Red", "Black"]  # Red o index 3
fav = input("What is your favorite color? ")
if fav in colors:
    print(f"Your colod is at index {colors.index(fav)} in my list")  # giu chu colod theo de
else:
    print("Sorry, I could not find your color")
