# 使用方法

main モジュールを実行して使用する。

```powershell
python -m speedtest_tool_fastcom.main -s <directory> -u <directory>
    必須オプション
        -s, --save_path: 計測データを記録するフォルダ・ディレクトリ（絶対パス）
        -u, --upload_path: 計測レポートをアップロードするフォルダ・ディレクトリ（絶対パス）
    任意オプション
        -c, --covert_byte: 指定すると byte/s でデータを記録
        -d, --date-select <date>: 指定した日付のレポートを出力
                                  日付は yyyy-MM-dd で指定、yyyy は西暦年、MM は月、dd は日
```

## プロキシ環境下で使う

下記を編集して、上述通りに使う。

`.\.venv\Lib\site-packages\pyppeteer\chromium_downloader.py` 78 行目をプロキシ対応をする

```python
# with urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) as http:

with urllib3.ProxyManager(proxy_url='http(s)://ip-address:port', cert_reqs='CERT_REQUIRED', ca_certs=certifi.where()) as http:
```
