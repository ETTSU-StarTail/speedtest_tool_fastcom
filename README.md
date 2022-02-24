# speedtest_tool-fastcom

speedtest_tool の fast.com 版

pyppeteer を使用して Fast.com を利用することでネットワーク速度計測をする。

sphinx ビルドはリポジトリ直下から下記で。

```powershell
.\make.bat html
```

パッケージ管理は `poetry` を使用

## Usage

```powershell
python -m speedtest_tool_fastcom.main -s <記録ディレクトリ絶対パス> -u <レポート出力ディレクトリ絶対パス>
```

記録ディレクトリ絶対パスに下記ディレクトリ・ファイルが生成される。

- `/path/to/<記録ディレクトリ絶対パス>/dest/yyyy-MM-dd.csv`: ネットワーク速度計測結果記録ファイル
- `/path/to/<記録ディレクトリ絶対パス>/dest/yyyy-MM-dd.html`: ネットワーク速度計測結果グラフファイル
- `/path/to/<記録ディレクトリ絶対パス>/log/speedtest_fastcom.log`: ネットワーク速度計測処理ログファイル
- `/path/to/<記録ディレクトリ絶対パス>/log/speedtest_fastcom.log.yyyy-MM-dd`: 古いネットワーク速度計測処理ログファイル
