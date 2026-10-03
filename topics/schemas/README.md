# スキーマ（プリムの型）

`def Cube "Box"` の `Cube` の部分。そのプリムが何で、どんな属性を持てるかを決める。

## 形状（UsdGeom）

**基本形状**

| スキーマ | 主な属性 |
|---|---|
| `Cube` | `size` |
| `Sphere` | `radius` |
| `Cylinder` | `radius`, `height`, `axis` |
| `Cone` | `radius`, `height`, `axis` |
| `Capsule` | `radius`, `height`, `axis`（全高 = height + radius × 2） |
| `Plane` | `width`, `length`, `axis`（axis は面の **法線** 方向） |

**汎用ジオメトリ**

| スキーマ | 用途 |
|---|---|
| `Mesh` | ポリゴンメッシュ（→ [mesh](../mesh/README.md)） |
| `BasisCurves` | 髪の毛・ファーなどの曲線 |
| `NurbsCurves` / `NurbsPatch` | NURBS 曲線・曲面 |
| `Points` | パーティクル |
| `PointInstancer` | 同じモデルの大量配置 |

## 構造・グループ化

| スキーマ | 用途 |
|---|---|
| `Xform` | 変換を持つグループ（→ [xform](../xform/README.md)） |
| `Scope` | 変換を持たない整理用グループ |

## カメラ・ライト

| スキーマ | 用途 |
|---|---|
| `Camera` | カメラ |
| `DistantLight` | 平行光源（太陽） |
| `SphereLight` | 点光源 |
| `RectLight` / `DiskLight` | エリアライト |
| `CylinderLight` | 円柱ライト（蛍光灯） |
| `DomeLight` | 環境光（HDRI） |

## その他

| スキーマ | 用途 |
|---|---|
| `Material` / `Shader` | マテリアル（UsdShade） |
| `SkelRoot` / `Skeleton` | スケルタルアニメーション（UsdSkel） |
| `Volume` | 煙や雲（UsdVol） |

## メモ

- 型名をタイポ（`Capsul` など）しても読み込めてしまい、何も表示されないだけになる。`tools\check` は WARN で出す
- `Cylinder_1` / `Capsule_1` という新しい版もある（上下で半径を変えられる）
- 型ごとの属性一覧は Python で確認できる:
  ```bat
  tools\usd python -c "from pxr import Usd; print(Usd.SchemaRegistry().FindConcretePrimDefinition('Cylinder').GetPropertyNames())"
  ```

## サンプル

- [primitives.usda](primitives.usda): 基本形状 6 種を横に並べたもの

## 確認

```bat
tools\check topics\schemas
tools\render topics\schemas\primitives.usda
```

## 参考

- [UsdGeom](https://openusd.org/release/api/usd_geom_page_front.html)
- [UsdLux](https://openusd.org/release/api/usd_lux_page_front.html)
