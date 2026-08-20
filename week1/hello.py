# Week 1, Lab 1

# Activity 1 & 2

print("==============================")
print("Welcome here")
print("My first post!")
print("==============================")

Username = "cool_creator"
bio = "Fun Blogger"
followers = 100

print("Username:", Username)
print("Bio:", bio)
print("Followers:", followers)

# Activity 3
followers += 50
print("Day 1:", followers)

followers += 20
print("Day 2:", followers)

followers -= 10
print("Day 3:", followers)

# Activity 4 & 5
username = input("Enter Username: ")
age = int(input("Enter Age: "))
category = input("Enter Content Category: ")

print("\nInstagram Profile")
print("====================")
print("Username: ", username)
print("Age: ",age)
print("Category: ", category)

if age>40 and category == "fun":
    print("You are old what is fun for you??")