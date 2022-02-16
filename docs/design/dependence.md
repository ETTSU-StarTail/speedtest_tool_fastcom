# 依存関係

Fast.com 版ネットワーク速度計測ツールの依存関係を下表に示す。

| 名称      | バージョン | 種別                                            |
| --------- | ---------- | ----------------------------------------------- |
| python    | 3.8.10     | プログラミング言語                              |
| bokeh     | 2.4.2      | データ可視化モジュール                          |
| pyppeteer | 1.0.2      | ブラウザ自動操作ツール puppeteer の python 実装 |

## 開発向け依存関係

Fast.com 版ネットワーク速度計測ツールの開発における依存関係を下表に示す。

| 名称                    | バージョン | 種別                              |
| ----------------------- | ---------- | --------------------------------- |
| black                   | 22.1.0     | python フォーマッタ               |
| flake8                  | 4.0.1      | python リンタ                     |
| flake8-black            | 0.2.4      | python リンタ（black 向け）       |
| flake8-bugbear          | 22.1.11    | python リンタ拡張                 |
| isort                   | 5.10.1     | インポートモジュールの整列ツール  |
| pre-commit              | 2.17.0     | git pre-commit hook ツール        |
| mypy                    | 0.931      | 型検査                            |
| pyinstaller             | 4.9        | 実行ファイル化ツール              |
| Sphinx                  | 4.4.0      | ドキュメント生成ツール            |
| pytest                  | 7.0.1      | テストフレームワーク              |
| myst-parser             | 0.17.0     | Sphinx の Markdown 利用拡張       |
| sphinx-markdown-tables  | 0.0.15     | Sphinx の Markdown 利用拡張       |
| sphinxcontrib-blockdiag | 3.0.0      | Sphinx のブロック図作図拡張       |
| sphinxcontrib-actdiag   | 3.0.0      | Sphinx のアクティビティ図作図拡張 |
| sphinx-material         | 0.0.35     | Sphinx テーマ                     |
