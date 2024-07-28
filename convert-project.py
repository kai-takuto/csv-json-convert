import csv
import json
import sys
from typing import Generator, Any
from pathlib import Path


def check(file_path: str) -> tuple[bool, Path]:
    """
    入力したファイルのパスを確認する関数
    :param file_path: 入力したファイルのパス
    :return: 入力したファイルのパス・csvならTrue,jsonならFalseを返す
    """
    if not isinstance(file_path, str):
        raise TypeError(f"argument 'file-path' must be str, but {type(file_path)}.")
    input_file_path: Path = Path(file_path)
    if not input_file_path.exists():
        raise FileNotFoundError(f"file path: {input_file_path} does not exist.")
    if not input_file_path.is_file():
        raise ValueError(f"file path: {input_file_path} is not a file.")
    if input_file_path.suffix not in [".csv", ".json"]:
        raise ValueError(f"file path: {input_file_path} does not have extension 'csv' or 'json'.")
    if input_file_path.suffix.lower() == '.csv':
        is_csv = True
    elif input_file_path.suffix.lower() == '.json':
        is_csv = False
    else:
        raise ValueError(f"ファイルパス '{input_file_path}' の拡張子が '.csv' または '.json' ではありません。")
    return is_csv, input_file_path


def read_file(path: str, as_csv: bool = True) -> Generator:
    """
    入力したファイルを読み込む関数
    :param path: 入力したファイルのパス
    :param as_csv: csvファイル
    :return: Generator
    """
    # TODO:読み込んでいるデータが同じ文字を取得している
    if as_csv:
        with open(path, mode="r", newline="", encoding="utf-8") as csvfile:
            csv_rows = csv.DictReader(csvfile)
            yield from csv_rows
    else:
        with open(path, mode="r", newline="", encoding="utf-8") as jsonfile:
            json_rows = json.load(jsonfile)
            yield from json_rows


def write_file(row_generator: Generator, output_path: str, as_json: bool = True) -> None:
    """
    ファイル 'csv/json' の読み込んだ内容を書き込む関数
    :param row_generator: 読み込んだ内容
    :param output_path: 書き込むファイルのパス
    :param as_json: jsonファイル
    :return:
    """
    if as_json:
        with open(output_path, mode='w', encoding='utf-8') as json_file:
            json.dump(list(row_generator), json_file, indent=4, ensure_ascii=False)
    else:
        first_row = next(row_generator, None)
        if first_row is None:
            raise ValueError("書き込むデータがありません。")

        fieldnames = first_row.keys()
        with open(output_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            # Write the first row and then the rest
            writer.writerow({key: convert_row_data(value, as_json=False) for key, value in first_row.items()})
            for row in row_generator:
                writer.writerow({key: convert_row_data(value, as_json=False) for key, value in row.items()})


def convert_row_data(value, as_json) -> Any:
    """
    文字列・数値・NAの変換を行う関数
    :param value: 変換する値
    :param as_json: Trueの時にcsv-jsonに変換、Falseの時にjson-csvに変換
    :return: 変換後の値を返す
    """
    if as_json:
        if value.strip() == '' or value.strip().upper() == 'NA':
            return None
        try:
            return int(value)
        except ValueError:
            return value
    else:
        if value is None:
            return 'NA'
        return value


def convert_file(file_path: str, to_json: bool = True):
    """
    変換する関数
    :param file_path:ファイルのパス
    :param to_json:jsonファイル
    :return:None
    """
    data_generator = read_file(file_path, as_csv=to_json)

    if to_json:
        json_file_path = "output.json"
        write_file(data_generator, output_path=json_file_path, as_json=to_json)
        print(f"CSVからJSONに変換しました: {json_file_path}")

    else:
        csv_file_path = "output.csv"
        write_file(data_generator, output_path=csv_file_path, as_json=False)
        print(f"JSONからCSVに変換しました: {csv_file_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python convert.py <file_path>")
        sys.exit(1)

    arg_file_path: str = sys.argv[1]

    try:
        is_to_json, arg_file_path = check(file_path=arg_file_path)
        convert_file(file_path=arg_file_path, to_json=is_to_json)
    except (TypeError, FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
