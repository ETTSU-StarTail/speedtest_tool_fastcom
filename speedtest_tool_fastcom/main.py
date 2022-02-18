from __future__ import annotations

import os
from argparse import ArgumentParser, Namespace
from datetime import date, datetime, timedelta

from speedtest_tool_fastcom.module import logmng, recorder, reporter, speedtest, utility


def get_option() -> Namespace:
    """オプション引数

    :return: オプション引数の名前空間
    :rtype: Namespace
    """
    argparser = ArgumentParser()
    argparser.add_argument(
        "-u",
        "--upload_path",
        type=str,
        default="",
        help="collected data upload to path",
    )
    argparser.add_argument(
        "-s",
        "--save_path",
        type=str,
        default="",
        help="collecting data save to path",
    )
    argparser.add_argument(
        "-c",
        "--convert_byte",
        type=bool,
        default=False,
        help="convert MBit/s to MByte/s",
    )
    return argparser.parse_args()


def main() -> None:
    """
    プログラムの実行起点となり処理フローを制御する。
    """

    logmng.logger.info("Start Program")

    args: Namespace = get_option()

    # オプション設定
    record_dir_path: str = "{0}/dest".format(args.save_path)
    record_dir_path = os.path.abspath(record_dir_path)

    upload_dir_path: str = args.upload_path

    convert_byte: bool = args.convert_byte

    today: date = date.today()
    file_path: str = os.path.join(
        record_dir_path, f"{today.strftime(utility.FORMAT_DATE_SHORT)}_fastcom.csv"
    )
    yesterday: date = date.today() - timedelta(days=1)

    # ネットワーク速度計測
    tested_network_data: tuple[datetime, float, float] = speedtest.run_speedtest(
        convert_byte
    )

    # 保存
    recorder.record_to_csv(file_path, tested_network_data, convert_byte)

    # レポートアップロード
    reporter.upload_report(record_dir_path, upload_dir_path, yesterday)

    logmng.logger.info("End Program")


if __name__ == "__main__":
    main()
