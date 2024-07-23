import csv
import os
import json


def check_file_exist(file_path: str) -> bool:
    """
    入力したファイルが自分のPCに入っているのかを確認する関数
    :param file_path: jsonのデータ形式に変換したいファイル
    :return: ファイルが存在していればTrue、存在していなかったらFalseを返す
    """
    if not os.path.exists(file_path):
        print('Error : Input file does not exist.')
        return False
    return True


def read_csv_to_list(csv_file: str) -> list:
    """
    csvファイルを読み込み、jsonファイルに書き込むためのデータを格納する関数
    :param csv_file: jsonのデータ形式に変換したいファイル
    :return: input_fileのデータを格納したリスト
    """
    # 読み込んだデータを処理
    with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
        rows: csv.DictReader = csv.DictReader(csvfile)
        # データを抜き取った後に、csv_file_dateに追加する
        for row in rows:
            yield row


def write_data_to_json(data: list[dict], json_file: str) -> None:
    """
    rowsのデータをjsonファイルに書き込む関数
    :param data: jsonファイルに書き込むためのcsvファイルのデータ
    :param json_file: csvファイルからjsonファイルに書き込むファイル
    :return: None
    """
    with open(json_file, mode='w', newline='', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=4)


def read_json_to_list(json_file: str) -> list[dict]:
    """
    jsonファイルをリスト形式で読み込む関数
    :param json_file: 入力したjsonファイル
    :return:読み込んだデータを格納したリスト
    """
    with open(json_file, mode='r', encoding='utf-8') as jsonfile:
        data: list[dict] = json.load(jsonfile)
    return data


def write_list_to_csv(data: list[dict], csv_file: str) -> None:
    """
    jsonファイルデータを格納したファイルをcsvファイルに書き込む関数
    :param data:読み込んだデータを格納したリスト
    :param csv_file:jsonファイルからcsvファイルに書き込むファイル
    :return:None
    """
    with open(csv_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer: csv.DictWriter = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)
