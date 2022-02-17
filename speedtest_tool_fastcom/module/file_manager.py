from __future__ import annotations

import os
import shutil

from speedtest_tool_fastcom.module import log_manager


def upload_file(file_path: str, upload_path: str) -> None:
    """指定パスのファイルを指定パスにアップロードする

    Args:
        file_path (str): アップロードしたいファイルのパス
        upload_path (str): アップロード先のパス
    """

    log_manager.logger.info("ファイルアップロード呼出")

    if not os.path.exists(upload_path):
        log_manager.logger.info(f"{upload_path} が見つかりませんでした。アップロード先パスを作成します。")
        os.makedirs(upload_path, exist_ok=True)

    if os.path.exists(file_path):
        log_manager.logger.info(f"{file_path} を {upload_path} へアップロードします。")
        shutil.copy(file_path, upload_path)
    else:
        log_manager.logger.info("アップロードしたいファイルが存在しない為、アップロードできませんでした。")
        log_manager.logger.info(f">> {file_path}")


def get_csvdata(file_path: str) -> list[tuple[str, ...]]:
    """csv ファイルを開いて中身をタプルのリストとして取得する。

    Args:
        file_path (str): csv ファイルパス

    Returns:
        list[tuple[str, ...]]: csv ファイルの中身
    """

    log_manager.logger.info("csv ファイル読込呼出")

    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        log_manager.logger.info(f)
        pass

    return [("test", "test", "test")]


def call_temp() -> None:
    log_manager.logger.info(f"called {__name__}.")


if __name__ == "__main__":
    log_manager.logger.info(f"{__file__} はモジュールをインポートして使ってください。")
