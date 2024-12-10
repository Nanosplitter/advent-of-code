reports = []

with open('input.txt') as f:
    lines = f.readlines()

    for line in lines:
        reports.append([int(i) for i in line.split()])

unsafe_reports = 0
for report in reports:
    
    if sorted(report) != report and sorted(report)[::-1] != report:
        unsafe_reports += 1
        continue
  
    for i in range(1, len(report)):
        if abs(report[i] - report[i - 1]) not in [1, 2, 3]:
            unsafe_reports += 1
            break

print(len(reports) - unsafe_reports)