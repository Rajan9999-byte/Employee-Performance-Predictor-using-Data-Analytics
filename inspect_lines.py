with open('src/dashboard.py', encoding='utf-8') as f:
    lines = f.readlines()
print("Line 22:", lines[21].strip()[:80])
print("Line 23:", lines[22].strip()[:80])
print("Line 271:", lines[270].strip()[:80])
print("Total:", len(lines))
