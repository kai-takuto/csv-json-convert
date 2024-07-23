import csv
import os
import json
import sys
from typing import Generator


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


def read_csv_to_list(csv_file: str) -> Generator[dict, None, None]:
    """
    csvファイルを読み込み、jsonファイルに書き込むためのデータを格納する関数
    :param csv_file: jsonのデータ形式に変換したいファイル
    :return: Generatorを返す
    """
    with open(csv_file, mode='r', newline='', encoding='utf-8') as csvfile:
        rows: csv.DictReader = csv.DictReader(csvfile)
        for row in rows:
            yield row


def write_data_to_json(data: Generator[dict, None, None], json_file: str) -> None:
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


def convert_csv_to_json(csv_file: str) -> None:
    """
     CSVファイルをJSONファイルに変換する関数
    :param csv_file: jsonファイルに変換したいcsvファイル
    :return: None
    """
    if not check_file_exist(csv_file):
        sys.exit(1)

    csv_data: Generator[dict, None, None] = read_csv_to_list(csv_file)
    data: Generator[dict, None, None] = csv_data
    json_file: str = 'converted.json'
    write_data_to_json(data, json_file)
    print(f'File conversion complete: CSV -> JSON. Output file: {json_file}')


def convert_json_to_csv(json_file: str) -> None:
    """
     JSONファイルをCSVファイルに変換する関数
    :param json_file: csvファイルに変換したいjsonファイル
    :return: None
    """
    if not check_file_exist(json_file):
        sys.exit(1)

    json_data:  list[dict] = read_json_to_list(json_file)
    csv_file: str = 'converted.csv'
    write_list_to_csv(json_data, csv_file)
    print(f'File conversion complete: JSON -> CSV. Output file: {csv_file}')
