# how many options

option1 = input("Enter Option 1: ")
option2 = input("Enter Option 2: ")
option3 = input("Enter Option 3: ")

# number of criteria
n = int(input("How many criteria? "))

total_weight = 0

score1 = 0
score2 = 0
score3 = 0

for i in range(n):

    print(f"\nCriterion {i+1}")

    criteria = input("Enter criteria name: ")

    weight = int(input("Enter weight: "))
    total_weight += weight

    s1 = int(input(f"Enter score for {option1}: "))
    s2 = int(input(f"Enter score for {option2}: "))
    s3 = int(input(f"Enter score for {option3}: "))

    score1 += weight * s1
    score2 += weight * s2
    score3 += weight * s3

# Final weighted scores
final1 = score1 / total_weight
final2 = score2 / total_weight
final3 = score3 / total_weight

print(f"\nFinal score for {option1}: {final1}")
print(f"Final score for {option2}: {final2}")
print(f"Final score for {option3}: {final3}")