# 値の型

属性は `型 名前 = 値` の形で書く。型名は `基本型 + 要素数 + 精度` の組み合わせが多い。

## 基本の型

| 型 | 中身 | 例 |
|---|---|---|
| `bool` | 真偽値 | `true` |
| `int` | 32bit 整数 | `3` |
| `half` / `float` / `double` | 16 / 32 / 64bit 浮動小数点 | `1.5` |
| `string` | 任意の文字列 | `"hello"` |
| `token` | 決まった選択肢の文字列（列挙値など） | `"Y"`, `"render"` |
| `asset` | ファイルパス | `@./tex.png@` |

`string` と `token` の違い: token は内部で共有される識別子。`axis` や `purpose` のように「値の候補が決まっているもの」は token。

## ベクトル

`double3` = double × 3、`float2` = float × 2 … のように **型 + 要素数**。

| 型 | 精度 | よく使う場所 |
|---|---|---|
| `double3` | 64bit | `xformOp:translate`（原点から遠くても誤差が出にくい） |
| `float3` | 32bit | `xformOp:rotateXYZ`, `xformOp:scale` |
| `half3` | 16bit | 精度より容量を優先するとき |

## ロール（役割）付きの型

中身は `float3` と同じだが「何を表すか」の意味が付いている。変換をかけたときの扱いが変わる。

| 型 | 意味 | 使われる場所 |
|---|---|---|
| `color3f` | 色 | `primvars:displayColor` |
| `point3f` | 位置 | Mesh の `points` |
| `vector3f` | 方向 | |
| `normal3f` | 法線 | Mesh の `normals` |
| `texCoord2f` | UV 座標 | `primvars:st` |

末尾の `f` / `d` / `h` が精度（float / double / half）。

## 行列・回転

| 型 | 例 |
|---|---|
| `matrix4d` | `((1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1))` |
| `quatf` / `quatd` | `(1, 0, 0, 0)`（実部が先頭） |

## 配列

型名の後ろに `[]`。値は `[ ]` で囲む。

```usda
int[] faceVertexCounts = [4, 3, 3]
point3f[] points = [(0, 0, 0), (1, 0, 0)]
```

## 注意: 型名のタイポ

`doubel size = 2` のように存在しない型名を書いても、usda は **エラーにせず読み込んでしまう**（値は解釈されない）。usdchecker も検出しないが、`tools\check` は FAIL で出す。

## サンプル

- [types.usda](types.usda): 上の型を `custom` 属性としてすべて書いたもの（表示されるものはない）

## 確認

```bat
tools\check topics\data-types
tools\usd python -c "from pxr import Usd; s=Usd.Stage.Open(r'topics\data-types\types.usda'); [print(a.GetName(), a.GetTypeName(), a.Get()) for a in s.GetPrimAtPath('/Types').GetAttributes()]"
```

## 参考

- [Basic Datatypes for Scene Description](https://openusd.org/release/api/_usd__page__datatypes.html)
