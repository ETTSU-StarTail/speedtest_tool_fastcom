from __future__ import annotations

from datetime import date, datetime

from speedtest_tool_fastcom.module import log_manager, utility


@utility.recording
def make_network_speed_graph(
    save_path: str,
    measure_date: date,
    network_speed_data: list[tuple[datetime, float, float]],
) -> None:
    """ネットワーク速度計測結果からグラフを html で出力する

    Args:
        save_path (str): 計測データ記録パス
        measure_date (date): 計測日付
        network_speed_data (list[tuple[datetime, float, float]]): ネットワーク速度計測データ
    """
    pass


def call_temp() -> None:
    log_manager.logger.info(f"called {__name__}.")


if __name__ == "__main__":
    log_manager.logger.info(f"{__file__} はモジュールをインポートして使ってください。")
