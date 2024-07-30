import csv

csv_file = 'input.csv'

int_count = 0
str_count = 0
float_count = 0
na_count = 0
bool_count = 0


def is_bool(value_bool):
    return value_bool.lower() in ['true', 'false']


total_read_values = 0

with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
    reader = csv.reader(file)
    for row in reader:
        for value in row:
            value_str = value.strip()
            total_read_values += 1
            if value_str == '':
                na_count += 1
            elif is_bool(value_str):
                bool_count += 1
            elif value_str.isdigit():
                int_count += 1
            else:
                try:
                    float_value = float(value_str)
                    float_count += 1
                except ValueError:
                    if "NA" in value_str:
                        na_count += 1
                    else:
                        str_count += 1

print("データの数")
print(f"int: {int_count}")
print(f"str: {str_count}")
print(f"float: {float_count}")
print(f"NA: {na_count}")
print(f"bool: {bool_count}")

print(f"合計 {total_read_values}")

total_count = int_count + str_count + float_count + na_count + bool_count
if total_read_values == total_count:
    print("合計の数が一致")
else:
    print("合計の数が不一致")
