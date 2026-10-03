# Mesh

頂点の座標と「どの頂点で面を作るか」のリストでポリゴンを表す。

## 最低限必要な属性

| 属性 | 型 | 意味 |
|---|---|---|
| `points` | `point3f[]` | 頂点座標の一覧。順番が頂点番号（0 始まり） |
| `faceVertexCounts` | `int[]` | 面ごとの頂点数。`[4, 3]` = 四角形 1 枚 + 三角形 1 枚 |
| `faceVertexIndices` | `int[]` | 各面が使う頂点番号を、面の順に並べたもの |

`faceVertexIndices` の長さ = `faceVertexCounts` の合計。

## あると良い属性

| 属性 | 意味 |
|---|---|
| `extent` | バウンディングボックス `[(最小), (最大)]`。無いと表示時に毎回計算される |
| `subdivisionScheme` | 既定は `"catmullClark"`（滑らかに表示される）。カクカクのままにするなら `"none"` |
| `normals` | 法線。無いと自動計算 |
| `primvars:displayColor` | 表示色 |

## 面の向き

既定（`orientation = "rightHanded"`）では、**外側から見て反時計回り** に頂点を並べた面が表になる。

## サンプル

- [pyramid.usda](pyramid.usda): 頂点 5 個・面 5 枚の四角錐

## 確認

```bat
tools\check topics\mesh
tools\render topics\mesh\pyramid.usda
```

## 参考

- [UsdGeomMesh](https://openusd.org/release/api/class_usd_geom_mesh.html)
