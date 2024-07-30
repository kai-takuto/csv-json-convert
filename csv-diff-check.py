import difflib


fl1 = "input.csv"
fl2 = "output.csv"
with open(fl1, 'r', encoding='utf-8') as file1, open(fl2, 'r', encoding='utf-8') as file2:
    text1 = file1.readlines()
    text2 = file2.readlines()


differ = difflib.Differ()
diff = list(differ.compare(text1, text2))


line_number1 = 0
line_number2 = 0
print(f"1stファイル：{fl1}")
print(f"2ndファイル：{fl2}")
for line in diff:
    if line.startswith('- '):
        line_number1 += 1
        print(f"1stファイル, 行{line_number1}: {line[2:]}")
    elif line.startswith('+ '):
        line_number2 += 1
        print(f"2ndファイル, 行{line_number2}: {line[2:]}")
    elif line.startswith('  '):
        line_number1 += 1
        line_number2 += 1



