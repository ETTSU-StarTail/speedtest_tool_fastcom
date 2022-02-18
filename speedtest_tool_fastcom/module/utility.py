from __future__ import annotations

import functools
import inspect
from datetime import datetime, timedelta
from enum import Enum

from speedtest_tool_fastcom.module import logmng

FORMAT_DATE_LONG: str = "%Y-%m-%d %H:%M:%S"
FORMAT_DATE_SHORT: str = "%Y-%m-%d"


class ValuePrefix(Enum):
    """オーダー接頭辞

    Args:
        Enum (Enum): 列挙型
    """

    k = 3
    M = 6
    G = 9
    T = 12


def recording(f):
    """関数 (メソッド) の呼び出しを記録するデコレータです。

    受け取ったパラメータと返り値をログに出力します。

    https://blog.amedama.jp/entry/2016/10/31/225219

    Args:
        f (Any): 関数

    Returns:
        Any: 結果
    """

    @functools.wraps(f)
    def _recording(*args, **kwargs):
        # 表面上は元々の関数 (メソッド) がそのまま実行されたように振る舞う
        result = f(*args, **kwargs)
        # デコレーションする関数のシグネチャを取得する
        sig = inspect.signature(f)
        # 受け取ったパラメータをシグネチャにバインドする
        bound_args = sig.bind(*args, **kwargs)
        # 関数名やバインドしたパラメータの対応関係を取得する
        func_name = f.__name__
        func_args = ",".join(
            "{k}={v}".format(k=k, v=v) for k, v in bound_args.arguments.items()
        )
        # ログに残す
        fmt = "★ called {func_name}({func_args}) -> {result}"
        msg = fmt.format(func_name=func_name, func_args=func_args, result=result)
        logmng.logger.info(msg)
        # 結果を返す
        return result

    return _recording


@recording
def bits_to_byte(value_bits: float) -> float:
    """bit から byte に変換する

    Args:
        value_bits (float): bit の数値

    Returns:
        float: byte に変換した数値
    """

    return value_bits / 8


@recording
def change_order(value: float, value_prefix: ValuePrefix) -> float:
    """数値のオーダーを変換する

    Args:
        value (float): 数値
        value_prefix (ValuePrefix): オーダー接頭辞

    Returns:
        float: オーダー変換した数値
    """

    return value / 10**value_prefix.value


@recording
def clear_order(value: float, units: str) -> float:
    """値を指定の単位に合わせてオーダーを取り除く（kilo, mega とかを無くす）

    Args:
        value (float): 値
        units (str): 値のオーダー（K, M, G, T）

    Returns:
        float: オーダーを除去した値
    """

    exponent: int = 1

    if units.upper().startswith("K"):
        exponent = ValuePrefix.k.value
    elif units.upper().startswith("M"):
        exponent = ValuePrefix.M.value
    elif units.upper().startswith("G"):
        exponent = ValuePrefix.G.value
    elif units.upper().startswith("T"):
        exponent = ValuePrefix.T.value
    else:
        pass

    return value * 10**exponent


@recording
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


if __name__ == "__main__":
    logmng.logger.info(f"{__file__} はモジュールをインポートして使ってください。")
