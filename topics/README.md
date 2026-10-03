# トピック一覧

各フォルダに、メモ（`README.md`）と確認用の usda を一緒に置いています。

| トピック | 内容 | サンプル |
|---|---|---|
| [usda-syntax](usda-syntax/README.md) | ファイルの骨格、プリム、属性、リレーションシップ、timeSamples | layer_and_prims |
| [data-types](data-types/README.md) | `double3` などの値型、ロール付きの型、配列 | types |
| [schemas](schemas/README.md) | Cube / Sphere などプリムの型の一覧 | primitives |
| [mesh](mesh/README.md) | 頂点と面のリストで作るポリゴン | pyramid |
| [xform](xform/README.md) | 移動・回転・スケール、xformOpOrder、親子関係 | parent_translate, op_order |
| [purpose](purpose/README.md) | render / proxy / guide の使い分け、proxyPrim | box_proxy |

## これから書きたいもの

- composition（sublayer / reference / payload / inherits / variantSet）
- マテリアル（UsdShade, UsdPreviewSurface）
- ライトとカメラ
- primvars と interpolation
- kind とモデル階層
