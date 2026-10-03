# CLAUDE.md

USD の学習用リポジトリ。ユーザーは日本語で USD を学んでいる。説明・メモは日本語で書く。

## 構成ルール

- `topics/<topic>/README.md` がメモ、同じフォルダの `*.usda` がそのメモで確認するサンプル
- 新しいトピックを作ったら `topics/README.md` の一覧に追加する
- 一時的な試しは `scratch/` に置く
- usda のヘッダーは `templates/sample.usda` に揃える（`doc`, `defaultPrim`, `upAxis = "Y"`, `metersPerUnit = 1`）
- usda 内のコメントは日本語で「何を確認するための行か」を書く
- `tools/*.cmd` は ASCII のみで書く（cmd.exe が UTF-8 の日本語を誤解釈するため）

## 検証

USD の exe は環境変数なしでは起動しないので、必ず `tools\usd.cmd` 経由で実行する。

- usda を書いたり変えたりしたら `tools\check <path>` を実行する（FAIL がゼロであること）
- 見た目が関係する変更は `tools\render <file>` で PNG を書き出し、画像を読んで確認する
  - usdrecord の既定では proxy purpose が描かれる。render purpose を見るときは `--purposes render`
- PowerShell からも `tools\check ...` のようにそのまま呼べる
