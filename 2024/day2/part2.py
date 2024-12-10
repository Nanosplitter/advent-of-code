def is_safe(report):
  if sorted(report) != report and sorted(report)[::-1] != report:
      return False
      
  for i in range(1, len(report)):
    if abs(report[i] - report[i - 1]) not in [1, 2, 3]:
      return False
  
  return True

reports = []

with open('input.txt') as f:
  lines = f.readlines()

  for line in lines:
    reports.append([int(i) for i in line.split()])

safe_reports = 0
for report in reports:
  safe = False
  for i in range(len(report)):
    test_report = report.copy()
    test_report.pop(i)

    if is_safe(test_report):
      safe = True

  safe_reports += safe

print(safe_reports)