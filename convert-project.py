import csv
import json

# csvファイルを読み込む工程
with open('input.csv', mode='r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
# 読み込んだデータを格納する
csv_file_date: list[str] = []
# データを抜き取った後に、csv_file_dateに追加する
for raw in reader:
    csv_file_date.append(raw)
