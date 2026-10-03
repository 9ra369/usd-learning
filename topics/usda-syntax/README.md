# usda の基本構文

usda は USD のテキスト形式。1 ファイル = 1 **レイヤー**。

## ファイルの骨格

```usda
#usda 1.0                 ← 必須のヘッダー（1 行目）
(
    defaultPrim = "World" ← レイヤーメタデータ
    upAxis = "Y"
    metersPerUnit = 1
)

def Xform "World"         ← プリム
{
    double3 xformOp:translate = (0, 0, 0)   ← 属性
}
```

## レイヤーメタデータ

| 項目 | 意味 |
|---|---|
| `defaultPrim` | 参照されたときに使われるルートプリム。usdchecker は未指定を指摘する |
| `upAxis` | 上方向。`"Y"` か `"Z"` |
| `metersPerUnit` | 1 単位が何メートルか。`1` = メートル、`0.01` = センチ |
| `doc` | 説明文。`"""` で複数行書ける |
| `startTimeCode` / `endTimeCode` | アニメーションの範囲 |

## プリムの書き方

```
<specifier> <型名> "<名前>" ( <プリムメタデータ> )
{
    <属性・リレーションシップ・子プリム>
}
```

- **specifier**: `def`（定義する）、`over`（既存のものを上書きする）、`class`（継承元になるテンプレート）
- **型名**: `Xform`, `Cube`, `Mesh` など（→ [schemas](../schemas/README.md)）。省略すると型なしプリム
- 同じレイヤーに同じパスのプリムを 2 回 `def` するとエラー

## 属性とリレーションシップ

```usda
double radius = 1                        # 属性: 型 名前 = 値
uniform token purpose = "default"        # uniform: 時間で変化しない
custom string memo = "..."               # custom: スキーマに無い自分用の属性
double radius.timeSamples = { 0: 1, 24: 2 }   # アニメーション
rel proxyPrim = </World/Ball>            # リレーションシップ: 他プリムへのパス
```

- 属性は **値**、リレーションシップは **パス** を持つ
- パスは `</World/Ball>` のように `< >` で囲む
- `custom` を付けずにスキーマに無い名前を書いても読み込めてしまう（タイポに気づけない）。`tools\check` はこれを WARN で出す

## サンプル

- [layer_and_prims.usda](layer_and_prims.usda): 上記の要素をひととおり含む。timeSamples で Ball が 0〜24 フレームで動く

## 確認

```bat
tools\check topics\usda-syntax
tools\view topics\usda-syntax\layer_and_prims.usda   :: 再生ボタンで Ball が動く
tools\usd usdcat topics\usda-syntax\layer_and_prims.usda
```

## 参考

- [USD Glossary](https://openusd.org/release/glossary.html)
