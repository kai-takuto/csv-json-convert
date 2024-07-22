import csv


# csvファイルを読み込む工程
def read_csv_to_list(input_file: str) -> list:
    # 読み込んだデータを格納する
    csv_file_date: list[str] = []
    with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
        reader: [str] = csv.DictReader(csvfile)
        # データを抜き取った後に、csv_file_dateに追加する
        for raw in reader:
            csv_file_date.append(raw)
    return csv_file_date
