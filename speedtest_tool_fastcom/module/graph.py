from __future__ import annotations

from datetime import date, datetime


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
    print(f"called {__name__}.")


if __name__ == "__main__":
    print(f"{__file__} はモジュールをインポートして使ってください。")
