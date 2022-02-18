from __future__ import annotations

import csv
import os
from datetime import datetime
from typing import Any

from speedtest_tool_fastcom.module import logmng, utility


@utility.recording
def check_record_file(file_path: str, convert_byte: bool) -> str:
    """記録先の確認及び無ければ作成する

    Args:
        file_path (str): 記録先
    Returns:
        str: ネットワーク速度計測結果 csv ファイルパス
    """

    dir_path: str = os.path.dirname(file_path)
    is_dir_exists: bool = os.path.exists(dir_path)
    is_file_exists: bool = os.path.exists(file_path)

    if not is_dir_exists:
        logmng.logger.info("保存先ディレクトリが見つかりません。")
        logmng.logger.info(f">> {dir_path}")

        os.makedirs(dir_path, exist_ok=True)

        logmng.logger.info("保存先ディレクトリを作成しました。")
        logmng.logger.info(f">> {dir_path}")
    else:
        pass

    if not is_file_exists:
        logmng.logger.info("csv ファイルが見つかりません。")
        logmng.logger.info(f">> {file_path}")

        with open(file_path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if convert_byte:
                writer.writerow(
                    (
                        "Tested Datetime",
                        "Download Speed(MByte/s)",
                        "Upload Speed(MByte/s)",
                    )
                )
            else:
                writer.writerow(
                    (
                        "Tested Datetime",
                        "Download Speed(MBit/s)",
                        "Upload Speed(MBit/s)",
                    )
                )
            logmng.logger.info("csv ファイル作成及びヘッダ行を追加しました。")
            logmng.logger.info(f">> {file_path}")
    else:
        pass

    return file_path


@utility.recording
def write_line_to_csv(dir_path: str, record: tuple[Any, ...]) -> None:
    """既存の csv ファイルに1行書き込む

    Args:
        dir_path (str): 書き込み先 csv ファイル
        record (tuple[Any, ...]): 書き込むデータレコード
    """

    is_exists: bool = os.path.exists(dir_path)

    if not is_exists:
        logmng.logger.error("csv ファイルが見つかりません。")
        logmng.logger.error(f">> {dir_path}")
    else:
        with open(dir_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(record)


def format_tested_network_data(
    tested_network_data: tuple[datetime, float, float]
) -> tuple[str, str, str]:
    """ネットワーク速度計測データを整形する

    Args:
        tested_network_data (tuple[datetime, float, float]): ネットワーク速度計測データ

    Returns:
        tuple[str, str, str]: 整形後ネットワーク速度計測データ
    """

    tested_datetime: datetime = tested_network_data[0]
    download_speed: float = tested_network_data[1]
    upload_speed: float = tested_network_data[2]

    download_speed = utility.change_order(download_speed, utility.ValuePrefix.M)
    upload_speed = utility.change_order(upload_speed, utility.ValuePrefix.M)

    return (
        tested_datetime.strftime(utility.FORMAT_DATE_LONG),
        str(download_speed),
        str(upload_speed),
    )


def record_to_csv(
    file_path: str,
    tested_network_data: tuple[datetime, float, float],
    convert_byte: bool,
) -> None:
    """ネットワーク速度計測データを csv ファイルへ記録する

    Args:
        file_path (str): ネットワーク速度計測結果記録 csv ファイル
        tested_network_data (tuple[datetime, float, float]): ネットワーク速度計測データ
    """

    check_record_file(file_path, convert_byte)

    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        record: tuple[str, str, str] = format_tested_network_data(tested_network_data)

        writer.writerow(record)


if __name__ == "__main__":
    logmng.logger.info(f"{__file__} はモジュールをインポートして使ってください。")
