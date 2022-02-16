from datetime import datetime, timedelta
from enum import Enum


class ValuePrefix(Enum):
    """オーダー接頭辞

    Args:
        Enum (Enum): 列挙型
    """

    k = 3
    M = 6
    G = 9
    T = 12


def bits_to_byte(value_bits: float) -> float:
    """bit から byte に変換する

    Args:
        value_bits (float): bit の数値

    Returns:
        float: byte に変換した数値
    """

    return value_bits / 8


def change_order(value: float, value_prefix: ValuePrefix) -> float:
    """数値のオーダーを変換する

    Args:
        value (float): 数値
        value_prefix (ValuePrefix): オーダー接頭辞

    Returns:
        float: オーダー変換した数値
    """

    return value / 10 ** value_prefix.value


def round_datetime(dt: datetime) -> datetime:
    """日時を丸める（15分単位）

    Args:
        dt (datetime): 日時

    Returns:
        datetime: 丸めた日時
    """

    minute: int = dt.minute
    tens_place: int = int(minute / 10)
    ones_place: int = minute - tens_place

    rounded_dt: datetime

    if ones_place < 5:
        rounded_dt = dt - timedelta(minutes=ones_place)
    else:
        rounded_dt = dt - timedelta(minutes=ones_place - 5)

    return rounded_dt


def call_temp() -> None:
    print(f"called {__name__}.")


if __name__ == "__main__":
    print(f"{__file__} はモジュールをインポートして使ってください。")
