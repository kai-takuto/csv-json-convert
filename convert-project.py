import csv
import json
import sys
from typing import Generator, Union
from pathlib import Path


def check(file_path: str) -> tuple[bool, Path]:
    """
    入力したファイルのパスを確認する関数
    :param file_path: 入力したファイルのパス
    :return: 入力したファイルのパス・csvならTrue,jsonならFalseを返す
    """
    if not isinstance(file_path, str):
        raise TypeError(f"Argument 'file-path' must be a string, but received type {type(file_path)}.")
    input_file_path: Path = Path(file_path)
    if not input_file_path.exists():
        raise FileNotFoundError(f"File path '{input_file_path}' does not exist.")
    if not input_file_path.is_file():
        raise ValueError(f"File path '{input_file_path}' is not a file.")
    is_csv = True if input_file_path.suffix.lower() == ".csv" else False
    return is_csv, input_file_path


def read_file(path: str, as_csv: bool = True) -> Generator:
    """
    入力したファイルを読み込む関数
    :param path: 入力したファイルのパス
    :param as_csv: 変換したいファイル "csv=True/json=False" のbool値
    :return: Generator
    """
    if as_csv:
        with open(path, mode="r", encoding="utf-8") as csv_file:
            rows = csv.DictReader(csv_file)
            for row in rows:
                csv_rows = {key: convert_row_data(value, row_data=as_csv) for key, value in row.items()}
                yield csv_rows
    else:
        with open(path, mode="r", encoding="utf-8") as json_file:
            json_rows = json.load(json_file)
            if not json_rows:
                raise ValueError("JSON file is empty.")
            if not isinstance(json_rows, list):
                raise ValueError("JSON data must be a list.")
            yield from json_rows


def write_file(row_generator: Generator, output_path: str, as_json: bool = True) -> None:
    """
    ファイル "csv/json" の読み込んだ内容を書き込む関数
    :param row_generator: 読み込んだ内容
    :param output_path: 書き込むファイルのパス
    :param as_json: 読み込んだファイル "csv = True / json = False" のbool値
    :return:
    """
    if as_json:
        with open(output_path, mode="w", encoding="utf-8") as json_file:
            json.dump(list(row_generator), json_file, indent=4, ensure_ascii=False)
    else:
        with open(output_path, mode="w", encoding="utf-8", newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for key, row in enumerate(row_generator):
                if key == 0:
                    csv_writer.writerow(row.keys())
                csv_writer.writerow(row.values())


def convert_row_data(value, row_data: True) -> Union[str, int, None]:
    """
    "文字列 -> str / 数値 -> int / NA -> null"に変換を行う関数
    :param value: 変換する値
    :param row_data: 変換したい ファイル"csv / json" の読み取ったデータ
    :return: 変換後の値を返す
    """
    if row_data:
        if value.strip() == "" or value.strip().upper() == "NA":
            return None
        try:
            return int(value)
        except ValueError:
            return value
    else:
        if value is None:
            return "NA"
        elif isinstance(value, int):
            return str(value)
        return value


def convert_file(file_path: Path, to_json: bool = True) -> None:
    """
    "csv/json"のファイルを読み込むread_file関数と読み込んだ内容を書き込むwrite_file関数を行い、変換作業をする関数
    読み込んだファイルがcsvならTrueが返されるので、csv-jsonへの変換が行われる。
    :param file_path: 書き込むファイルのパス
    :param to_json: 変換するファイル"csv-json = True / json-csv = False"のbool値
    :return: None
    """
    data_generator: Generator = read_file(str(file_path), as_csv=to_json)

    output_file_path = "output.json" if to_json else "output.csv"

    write_file(row_generator=data_generator, output_path=output_file_path, as_json=to_json)
    print(f"Converted {'from CSV to JSON' if to_json else 'from JSON to CSV'}: {output_file_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python convert.py <file_path>")
        sys.exit(1)

    arg_file_path: str = sys.argv[1]

    try:
        is_to_json, file_path = check(file_path=arg_file_path)
        convert_file(file_path=file_path, to_json=is_to_json)
    except (TypeError, FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
