import csv
import json
import sys
from typing import Generator
from pathlib import Path


def check(file_path: str) -> tuple[bool, Path]:
    """
    入力したファイルのパスを確認する関数
    :param file_path: 入力したファイルのパス
    :return: 入力したファイルのパス・True
    """
    if not isinstance(file_path, str):
        raise TypeError(f"argument 'file-path' must be str, but {type(file_path)}.")
    input_file_path: Path = Path(file_path)
    if not input_file_path.exists():
        raise FileNotFoundError(f"file path: {input_file_path} does not exist.")
    if not input_file_path.is_file():
        raise ValueError(f"file path: {input_file_path} is not a file.")
    # if not str(_path).endswith(".csv") or not str(_path).endswith(".json"):
    if input_file_path.suffix not in [".csv", ".json"]:
        raise ValueError(f"file path: {input_file_path} does not have extension 'csv' or 'json'.")
    return True, input_file_path


def read_file(path: Path, as_csv: bool = True) -> Generator[dict, None, None]:
    """
    入力したファイルを読み込む関数
    :param path: 入力したファイルのパス
    :param as_csv: csvファイル
    :return: Generator
    """
    if as_csv:
        with open(path, mode='r', newline='', encoding='utf-8') as csvfile:
            csv_rows = csv.DictReader(csvfile)
            for row in csv_rows:
                yield row
    else:
        with open(path, mode='r', newline='', encoding='utf-8') as jsonfile:
            try:
                json_rows = json.load(jsonfile)
                yield from json_rows
            except json.JSONDecodeError as e:
                raise ValueError(f"Error decoding JSON file: {e}")


def write_file(row_generator: Generator, as_json: bool = True) -> bool:
    """
    読み込んだファイルを書き込む関数
    :param row_generator: read_fileのGenerator
    :param as_json: jsonファイル
    :return: 書き込みが成功したらTrueを返す
    """
    if as_json:
        # TODO: Jsonファイルに書き込む
        with open('output.json', mode='w', newline='', encoding='utf-8') as output_json:
            output_json.write('[')
            first_row = True
            for row in row_generator:
                if not first_row:
                    output_json.write(',\n')
                else:
                    first_row = False
                json.dump(row, output_json, ensure_ascii=False, indent=4)
            output_json.write(']')
    # TODO: CSVファイルに書き込む
    else:
        with open('output.csv', mode='w', newline='', encoding='utf-8') as output_csv:
            writer = csv.writer(output_csv)
            for row in row_generator:
                writer.writerow(row)
    return True


def convert_row_data(row_generator: Generator) -> Generator:
    """
    変換する時に必要な型に変換する関数
    :param row_generator: write
    :return: Generatorを返す
    """
    for row in row_generator:
        converted_row = {}
        for key, value in row.items():
            if isinstance(value, str) and value.lower() == 'na':
                converted_row[key] = None
            else:
                try:
                    converted_row[key] = int(value)
                except ValueError:
                    try:
                        converted_row[key] = float(value)
                    except ValueError:
                        converted_row[key] = value
        yield converted_row


def convert_file(file_path: Path, to_json: bool = True):
    """
    変換する関数
    :param file_path:ファイルのパス
    :param to_json:jsonファイル
    :return:NOne
    """
    # ファイルを読み込む
    row_generator: Generator = read_file(as_csv=to_json, path=file_path)
    # データの中身を変換する
    converted_row_generator: Generator = convert_row_data(row_generator=row_generator)
    # ファイルを出力
    write_file(as_json=to_json, row_generator=converted_row_generator)


def main():
    # TODO: 引数を受け取る
    if len(sys.argv) != 2:
        print("Usage: python convert.py <file_path>")
        sys.exit(1)

    arg_file_path: str = sys.argv[1]
    # 引数が有効な値かチェック
    # 引数で指定したファイル名が有効(存在するか? csv/jsonの形式か?)かチェックする
    try:
        is_to_json, file_path = check(file_path=arg_file_path)
        convert_file(file_path=file_path, to_json=is_to_json)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # convert_csv_to_json('input.csv')
    main()
