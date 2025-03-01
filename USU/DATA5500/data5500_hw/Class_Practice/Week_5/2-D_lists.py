# 2d lists
# multiplication table
tab = []
for i in range(10):
    tab.append([])

for i in range(10):
    for j in range(10):
        tab[i].append(i * j)

print("tab: ", tab, "\n")

for row in tab:
    print(row)

for i in range(10):
    for j in range(10):
        print(tab[i][j], end = " ")
    print()

# list of student scores
jonny = [40, 48, 50]
sally = [49, 50, 50]
jenny = [50, 50, 50]

student_scores = [jonny, sally, jenny]

for student in student_scores:
    print(student)

for student in student_scores:
    for score in student:
        print(score, end = ' ')

# checkpoint activity
# create 3 lists that represent student's homework scores
arika = [100, 95, 92, 97]
rikaa = [84, 60, 78, 82]
ikaar = [87, 88, 75, 70]

student_scores = [arika, rikaa, ikaar]

# calculate the average hw score for each student
for student in student_scores:
    average_score = 0
    for score in student:
        average_score += score
    print("Student average: ", average_score/len(student))

# calculate the average hw score for all 3 students
overall_average = 0
hw_count = 0
for student in student_scores:
    for score in student:
        overall_average += score
        hw_count += 1

print("Overall average: ", overall_average/hw_count)