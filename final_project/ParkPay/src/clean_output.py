files = ["controller.py", "core/note.py", "core/park.py", "core/report.py", "core/visitor.py", "init_data.py", "service_test.py", "utilities/utils.py"]

file = open("data", "r+")
content = file.readlines()
file.close()

cleaned = []

for line in content:
    for f in files:
        if f in line:
            cleaned.append(line.split()[:3])
            
TOTAL_LINES = 0
TOTAL_MISS = 0

print("file  \t\t\t Total lines\t Total Missed\t Percentage Covered(%)")
for cleaned_data in cleaned:
    print(cleaned_data[0], " " * (30-len(cleaned_data[0])), cleaned_data[1], "\t", cleaned_data[2], "\t\t", float(((int(cleaned_data[1])-int(cleaned_data[2]))/int(cleaned_data[1]))*100), "%")
    TOTAL_LINES += int(cleaned_data[1])
    TOTAL_MISS += int(cleaned_data[2])
print("TOTALS:",  " " * (29-len("TOTALS")), TOTAL_LINES, "\t", TOTAL_MISS, "\t\t", ((TOTAL_LINES-TOTAL_MISS)/TOTAL_LINES)*100, "%" )
