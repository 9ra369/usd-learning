# usd_workspace

USD の勉強用リポジトリ。メモを書きながら usda を手書きして、チェック・表示で確かめる。

## フォルダ構成

```
usd_workspace/
├── topics/              トピックごとに「メモ + 確認用 usda」をまとめる
│   ├── README.md        トピック一覧（目次）
│   └── <topic>/
│       ├── README.md    メモ
│       └── *.usda       そのメモで確認するサンプル
├── scratch/             試し書き用（気軽に壊してよい）
├── templates/           新しいトピックのひな形
├── tools/               チェック・表示・レンダリング用スクリプト
├── renders/             tools\render の出力先（自動生成）
└── .vscode/tasks.json   VS Code から tools を呼ぶタスク
```

トピック一覧 → [topics/README.md](topics/README.md)

## ツール

USD 本体は `D:\Dev\usd_root`（NVIDIA 配布版 OpenUSD 25.08）。
`usd_root\bin` の exe は DLL のパスを通さないと起動しないので、すべて `tools\usd.cmd` 経由で環境を読み込んでから実行する。

| コマンド | 内容 |
|---|---|
| `tools\check [パス...]` | usda のチェック。引数なしで topics と scratch すべて |
| `tools\view <file>` | usdview で開く |
| `tools\render <file> [usdrecord のオプション]` | `renders\<名前>.png` に書き出す |
| `tools\new <topic> [sample名]` | templates から新しいトピックを作る |
| `tools\usd <command>` | USD 環境で任意のコマンドを実行（`usdcat`, `usdtree`, `python` など） |

PowerShell からも `tools\check` のようにそのまま実行できる。

### tools\check の判定

`usdchecker` に加えて、usdchecker が見逃す書き間違いも検出する。

| 判定 | 内容 |
|---|---|
| FAIL | 構文エラー、合成エラー、存在しない値型（`doubel` など） |
| WARN | スキーマに無い属性名（`sizee` など）、存在しないプリム型（`Capsul` など）、xformOpOrder に入っていない xformOp、参照先の無いリレーションシップ、usdchecker の指摘 |
| OK | 問題なし |

### よく使う USD コマンド

```bat
tools\usd usdcat file.usda              :: 読み込んだ結果を usda で出力
tools\usd usdcat --flatten file.usda    :: composition を解決して 1 枚にした結果
tools\usd usdtree file.usda             :: プリム階層をツリー表示
tools\usd usddiff a.usda b.usda         :: 2 ファイルの差分
tools\usd usdchecker file.usda          :: 公式のチェッカー単体
tools\usd python                        :: pxr が使える Python
```

## VS Code

`Ctrl+Shift+P` → **Tasks: Run Task** から実行できる（開いているファイルが対象）。

- USD: Check current file
- USD: Check all
- USD: View current file (usdview)
- USD: Render current file
- USD: Flatten current file (usdcat)

## 進め方

1. `tools\new <topic>` でフォルダを作る（または scratch で試す）
2. usda を書く → `tools\check` → `tools\view` / `tools\render` で確認
3. 分かったことを README.md にメモする
4. [topics/README.md](topics/README.md) の一覧に追加する
