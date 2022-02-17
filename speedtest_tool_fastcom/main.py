from __future__ import annotations

from speedtest_tool_fastcom.module import (
    file_manager,
    graph,
    log_manager,
    speedtest,
    utility,
)


def main() -> None:
    """
    プログラムの実行起点となり処理フローを制御する。
    """

    log_manager.logger.info("Start Program")

    log_manager.logger.info(speedtest.run_speedtest())
    graph.call_temp()
    file_manager.call_temp()
    log_manager.call_temp()
    utility.call_temp()

    log_manager.logger.info("End Program")


if __name__ == "__main__":
    main()
