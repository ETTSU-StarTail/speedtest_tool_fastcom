from __future__ import annotations

import csv
import os
import shutil
from datetime import date, datetime

import bokeh.models
import bokeh.plotting

from speedtest_tool_fastcom.module import logmng, utility


@utility.recording
def get_result_csv(file_path: str) -> dict[str, list[tuple[datetime, float]]]:
    """ネットワーク速度計測結果 csv ファイルを開いて中身をタプルのリストとして取得する。

    Args:
        file_path (str): ネットワーク速度計測結果 csv ファイルパス

    Returns:
        dict[str, list[tuple[datetime, float]]]: 日時に対するダウンロード速度（key: download_speed）
                                                 日時に対するアップロード速度（key: upload_speed）
    """

    with open(file_path, mode="r", newline="", encoding="utf-8") as f:
        reader = csv.reader(f)

        reader.__next__()

        download_speed_list: list[tuple[datetime, float]] = []
        upload_speed_list: list[tuple[datetime, float]] = []

        for row in reader:
            download_speed: tuple[datetime, float] = (
                datetime.strptime(row[0], utility.FORMAT_DATE_LONG),
                float(row[1]),
            )
            upload_speed: tuple[datetime, float] = (
                datetime.strptime(row[0], utility.FORMAT_DATE_LONG),
                float(row[2]),
            )

            download_speed_list.append(download_speed)
            upload_speed_list.append(upload_speed)

    return {"download_speed": download_speed_list, "upload_speed": upload_speed_list}


@utility.recording
def make_network_speed_graph(
    csv_file_path: str,
    dest_path: str,
) -> None:
    """ネットワーク速度計測結果からグラフを html で出力する

    Args:
        csv_file_path (str): ネットワーク速度計測結果ファイルパス
        dest_path (str): 出力レポートファイルパス
    """

    tested_data: dict[str, list[tuple[datetime, float]]] = get_result_csv(csv_file_path)

    download_speed_list: list[tuple[datetime, float]] = tested_data["download_speed"]
    upload_speed_list: list[tuple[datetime, float]] = tested_data["upload_speed"]

    bokeh.plotting.reset_output()

    title: str = "Network Speed at {0}".format(os.path.basename(csv_file_path))

    bokeh.plotting.output_file(
        dest_path, os.path.basename(csv_file_path).split(".")[0] + "_fastcom"
    )

    hover_tool = bokeh.models.HoverTool(
        tooltips=[("Datetime", "@x{%T}"), ("Network Speed", "@{top} [MByte/s]")],
        formatters={"@x": "datetime"},
        mode="vline",
    )

    p = bokeh.plotting.figure(
        tools=[hover_tool, "save", "pan", "zoom_in", "zoom_out", "reset"],
        title=title,
        x_axis_label="Datetime",
        x_axis_type="datetime",
        y_axis_label="Network speed [MByte/s]",
        plot_width=1600,
        plot_height=800,
    )
    x_format = "%H:%M:%S"
    p.xaxis.formatter = bokeh.models.DatetimeTickFormatter(
        seconds=[x_format],
        minutes=[x_format],
        hours=[x_format],
        days=[x_format],
        months=[x_format],
        years=[x_format],
    )

    p.vbar(
        x=[x_value[0] for x_value in download_speed_list],
        top=[y_value[1] for y_value in download_speed_list],
        width=20000,
        fill_color="#8682F5",
        legend_label="Download speed [MByte/s]",
    )

    p.vbar(
        x=[x_value[0] for x_value in upload_speed_list],
        top=[y_value[1] for y_value in upload_speed_list],
        width=20000,
        fill_color="#F57E76",
        legend_label="Upload speed [MByte/s]",
    )

    p.legend.click_policy = "hide"

    bokeh.plotting.save(p, filename=dest_path)


@utility.recording
def upload_report(
    record_dir_path: str,
    upload_dir_path: str,
    target_date: date,
    is_force: bool = False,
) -> None:
    """指定日付のネットワーク速度計測結果とグラフをアップロードする

    Args:
        data_path (str): ネットワーク速度計測結果ディレクトリパス
        upload_path (str): レポートをアップロード先ディレクトリパス
        target_date (date): ネットワーク速度計測結果日付
    """

    file_name: str = target_date.strftime(utility.FORMAT_DATE_SHORT)
    file_path: str = os.path.join(record_dir_path, file_name + "_fastcom.csv")
    report_path: str = os.path.join(record_dir_path, file_name + "_fastcom.html")

    # アップロード先確認
    is_upload_dir_exists: bool = os.path.exists(
        upload_dir_path
    ) or upload_dir_path.__contains__(r"\\")
    if is_upload_dir_exists:
        os.makedirs(upload_dir_path, exist_ok=True)
        logmng.logger.info("アップロード先ディレクトリが見つからない為作成しました。")
        logmng.logger.info(f">> {upload_dir_path}")

    # レポート作成
    is_file_exists: bool = os.path.exists(file_path)
    is_report_exists: bool = os.path.exists(report_path)

    if not is_file_exists:
        logmng.logger.warn("指定日付のネットワーク速度計測結果ファイルが無い為グラフは作成していません。")
        logmng.logger.warn(f">> {file_path}")
    elif not is_report_exists or is_force:
        make_network_speed_graph(file_path, report_path)
        logmng.logger.info(f"{file_path} のグラフを {report_path} に作成しました。")

        shutil.copy(file_path, upload_dir_path)
        shutil.copy(report_path, upload_dir_path)
        logmng.logger.info(
            f"{file_path} 及び {report_path} を {upload_dir_path} にアップロードしました。"
        )
    else:
        logmng.logger.warn("既にグラフが有り、強制作成フラグが False の為グラフは作成していません。")
        logmng.logger.warn(f">> {file_path}")


if __name__ == "__main__":
    logmng.logger.info(f"{__file__} はモジュールをインポートして使ってください。")
