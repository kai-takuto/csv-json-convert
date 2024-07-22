import csv
import os


def check_file_exist(csv_file: str) -> bool:
    """
    入力したファイルが自分のPCに入っているのかを確認する関数
    :param csv_file: jsonのデータ形式に変換したいファイル
    :return: ファイルが存在していればTrue、存在していなかったらFalseを返す
    """
    if not os.path.exists(csv_file):
        print('Error : Input file does not exist.')
        return False
    return True


def read_csv_to_list(input_file: str) -> list:
    """
    csvファイルを読み込み、jsonファイルに書き込むためのデータを格納する関数
    :param input_file: jsonのデータ形式に変換したいファイル
    :return: input_fileのデータを格納したリスト
    """
    # 読み込んだデータを処理
    with open(input_file, mode='r', newline='', encoding='utf-8') as csvfile:
        rows: csv.DictReader = csv.DictReader(csvfile)
        # データを抜き取った後に、csv_file_dateに追加する
        for row in rows:
            yield row
