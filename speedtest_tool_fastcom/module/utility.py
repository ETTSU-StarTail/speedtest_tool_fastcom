from __future__ import annotations

import functools

from datetime import datetime, timedelta
from enum import Enum
import inspect
from typing import Any

from speedtest_tool_fastcom.module import log_manager


class ValuePrefix(Enum):
    """オーダー接頭辞

    Args:
        Enum (Enum): 列挙型
    """

    k = 3
    M = 6
    G = 9
    T = 12


def recording(f: Any) -> Any:
    """関数 (メソッド) の呼び出しを記録するデコレータです。

    受け取ったパラメータと返り値をログに出力します。

    https://blog.amedama.jp/entry/2016/10/31/225219

    Args:
        f (Any): 関数

    Returns:
        Any: 結果
    """

    @functools.wraps(f)
    def _recording(*args: Any, **kwargs: Any) -> Any:
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
        fmt = "{func_name}({func_args}) -> {result}"
        msg = fmt.format(func_name=func_name, func_args=func_args, result=result)
        log_manager.logger.info(msg)
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
    log_manager.logger.info(f"called {__name__}.")


if __name__ == "__main__":
    log_manager.logger.info(f"{__file__} はモジュールをインポートして使ってください。")
