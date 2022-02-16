from __future__ import annotations

from datetime import datetime


def speedtest() -> tuple[datetime, float, float]:
    """Fast.com によるネットワーク速度を計測し、計測結果を返す

    Returns:
        tuple[datetime, float, float]: 計測日時/ダウンロード速度[bit/s]/アップロード速度[bit/s]
    """

    return (datetime.now(), 1.1, 1.1)


def call_temp() -> None:
    print(f"called {__name__}.")


if __name__ == "__main__":
    print(f"{__file__} はモジュールをインポートして使ってください。")
