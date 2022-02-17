from __future__ import annotations
import asyncio

import logging
from datetime import datetime
from typing import Any
from pyppeteer import launch
from pyppeteer.page import Request

from speedtest_tool_fastcom.module import log_manager, utility


async def handle_request(request: Request) -> Any:
    """pyppeteer で必要な情報だけ読み込む設定をする

    https://qiita.com/Nekomikado/items/3fa78568af48cfb11822

    Args:
        request (Request): pyppeteer でのリクエスト

    Returns:
        Any: pyppeteer での絞ったリクエスト
    """

    # リソースタイプがDocumentかScript以外はアクセスしない
    if request.resourceType in ["document", "script", "xhr"]:
        # continue_()なのはおそらく予約語と被るため
        return await request.continue_()
    else:
        return await request.abort()


@utility.recording
async def get_screenshot(url: str) -> None:
    browser = await launch(logLevel=logging.WARNING)
    page = await browser.newPage()

    # リソースタイプを指定するため割り込みを有効にする
    await page.setRequestInterception(True)
    await page.on(
        "request", lambda request: asyncio.ensure_future(handle_request(request))
    )

    await page.goto(url)
    await page.screenshot({"path": "example.png"})
    await browser.close()


@utility.recording
async def get_network_info_from_fastcom() -> dict[str, float | str]:
    """Fast.com でネットワーク速度結果を取得する

    Returns:
        dict[str, float | str]: "download_speed": ダウンロード速度
                                "download_unit": ダウンロード速度単位
                                "downloaded": ダウンロードサイズ
                                "upload_speed": アップロード速度
                                "upload_unit": アップロード速度単位
                                "uploaded": アップロードサイズ
                                "latency": 遅延
                                "buffer_bloat": バッファブロート？
                                "user_location": ユーザ地域
                                "user_ip": ユーザIP
    """

    target_url: str = "https://fast.com/"

    browser = await launch(logLevel=logging.WARNING)
    page = await browser.newPage()

    # リソースタイプを指定するため割り込みを有効にする
    await page.setRequestInterception(True)
    page.on("request", lambda request: asyncio.ensure_future(handle_request(request)))

    await page.goto(target_url)

    is_done: bool = False
    download_speed: float = 0
    download_units: str = ""
    downloaded: float = 0
    upload_speed: float = 0
    upload_units: str = ""
    uploaded: float = 0
    latency: float = 0
    buffer_bloat: float = 0
    user_location: str = ""
    user_ip: str = ""

    while not is_done:
        download_speed: float = await page.evaluate(
            "(elm) => Number(elm.textContent.trim())",
            await page.querySelector("#speed-value"),
        )

        download_units: str = await page.evaluate(
            "(elm) => elm.textContent.trim()", await page.querySelector("#speed-units")
        )

        downloaded: float = await page.evaluate(
            "(elm) => Number(elm.textContent.trim())",
            await page.querySelector("#down-mb-value"),
        )

        upload_speed: float = await page.evaluate(
            "(elm) => Number(elm.textContent.trim())",
            await page.querySelector("#upload-value"),
        )

        upload_units: str = await page.evaluate(
            "(elm) => elm.textContent.trim()", await page.querySelector("#upload-units")
        )

        uploaded: float = await page.evaluate(
            "(elm) => Number(elm.textContent.trim())",
            await page.querySelector("#up-mb-value"),
        )

        latency: float = await page.evaluate(
            "(elm) => Number(elm.textContent.trim())",
            await page.querySelector("#latency-value"),
        )

        buffer_bloat: float = await page.evaluate(
            "(elm) => Number(elm.textContent.trim())",
            await page.querySelector("#bufferbloat-value"),
        )

        user_location: str = await page.evaluate(
            "(elm) => elm.textContent.trim()",
            await page.querySelector("#user-location"),
        )

        user_ip: str = await page.evaluate(
            "(elm) => elm.textContent.trim()",
            await page.querySelector("#user-ip"),
        )

        is_done: bool = (
            await page.querySelector("#speed-value.succeeded") is not None
            and await page.querySelector("#upload-value.succeeded") is not None
        )

        log_manager.logger.info(
            {
                "download_speed": download_speed,
                "download_units": download_units,
                "downloaded": downloaded,
                "upload_speed": upload_speed,
                "upload_units": upload_units,
                "uploaded": uploaded,
                "latency": latency,
                "buffer_bloat": buffer_bloat,
                "user_location": user_location,
                "user_ip": user_ip,
                "is_done": is_done,
            }
        )

        await asyncio.sleep(5)

    await browser.close()

    return {
        "download_speed": download_speed,
        "download_units": download_units,
        "downloaded": downloaded,
        "upload_speed": upload_speed,
        "upload_units": upload_units,
        "uploaded": uploaded,
        "latency": latency,
        "buffer_bloat": buffer_bloat,
        "user_location": user_location,
        "user_ip": user_ip,
    }


@utility.recording
def run_speedtest() -> tuple[datetime, float, float]:
    """Fast.com によるネットワーク速度を計測し、計測結果を返す

    Returns:
        tuple[datetime, float, float]: 計測日時/ダウンロード速度[bit/s]/アップロード速度[bit/s]
    """

    test_datetime = datetime.now()

    # 計測
    result: dict[str, float | str] = asyncio.get_event_loop().run_until_complete(
        get_network_info_from_fastcom()
    )
    download_speed: float = float(result["download_speed"])
    upload_speed: float = float(result["upload_speed"])

    # 整形
    download_units = str(result["download_units"])
    upload_units = str(result["upload_units"])

    # bit に直す？
    if download_units.upper().startswith("K"):
        download_speed = download_speed * 10**utility.ValuePrefix.k.value
    elif download_units.upper().startswith("M"):
        download_speed = download_speed * 10**utility.ValuePrefix.M.value
    elif download_units.upper().startswith("G"):
        download_speed = download_speed * 10**utility.ValuePrefix.G.value
    elif download_units.upper().startswith("T"):
        download_speed = download_speed * 10**utility.ValuePrefix.T.value
    else:
        pass

    if upload_units.upper().startswith("K"):
        upload_speed = upload_speed * 10**utility.ValuePrefix.k.value
    elif upload_units.upper().startswith("M"):
        upload_speed = upload_speed * 10**utility.ValuePrefix.M.value
    elif upload_units.upper().startswith("G"):
        upload_speed = upload_speed * 10**utility.ValuePrefix.G.value
    elif upload_units.upper().startswith("T"):
        upload_speed = upload_speed * 10**utility.ValuePrefix.T.value
    else:
        pass

    return (test_datetime, download_speed, upload_speed)


def call_temp() -> None:
    log_manager.logger.info(f"called {__name__}.")


if __name__ == "__main__":
    log_manager.logger.info(f"{__file__} はモジュールをインポートして使ってください。")
