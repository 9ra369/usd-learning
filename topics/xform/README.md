# Xform（移動・回転・スケール）

## 書き方

```usda
double3 xformOp:translate = (2, 0, 0)
float3 xformOp:rotateXYZ = (0, 45, 0)
float3 xformOp:scale = (1, 1, 1)
uniform token[] xformOpOrder = ["xformOp:translate", "xformOp:rotateXYZ", "xformOp:scale"]
```

- `xformOp:〜` の属性を書いて、使うものを `xformOpOrder` に並べる
- **`xformOpOrder` に入っていない op は無視される**（書いただけでは効かない）。`tools\check` は WARN で出す

## 主な op

| op | 型 | 意味 |
|---|---|---|
| `xformOp:translate` | `double3` | 移動 |
| `xformOp:rotateX` / `rotateY` / `rotateZ` | `float` | 1 軸回転（度） |
| `xformOp:rotateXYZ` など | `float3` | 3 軸回転（度）。名前の順に回転 |
| `xformOp:scale` | `float3` | スケール |
| `xformOp:orient` | `quatf` | クォータニオン回転 |
| `xformOp:transform` | `matrix4d` | 行列で直接指定 |

同じ種類を 2 つ使いたいときは `xformOp:translate:pivot` のように後ろに名前を付ける。

## 順番の意味

点には **リストの後ろの op から順に** 適用される。

`["xformOp:translate", "xformOp:rotateZ"]` → 回転してから移動（その場で回る）
`["xformOp:rotateZ", "xformOp:translate"]` → 移動してから回転（原点を中心に回り込む）

一般的な順番は `translate → rotate → scale`（= スケール → 回転 → 移動の順に適用）。

## 親子関係

子の変換は **親からの相対**。親 Xform を動かすと子もまとめて動く。

## サンプル

- [parent_translate.usda](parent_translate.usda): 親 World を x に 2 動かす。子の Ball はローカル (3,0,0) → ワールド (5,0,0)
- [op_order.usda](op_order.usda): 同じ translate + rotateZ を逆順にした 2 つの Cube

## 確認

```bat
tools\check topics\xform
tools\render topics\xform\op_order.usda
```

ワールド座標を数値で確認する:

```bat
tools\usd python -c "from pxr import Usd, UsdGeom; s=Usd.Stage.Open(r'topics\xform\parent_translate.usda'); print(UsdGeom.Xformable(s.GetPrimAtPath('/World/Ball')).ComputeLocalToWorldTransform(0).ExtractTranslation())"
```

## 参考

- [UsdGeomXformable](https://openusd.org/release/api/class_usd_geom_xformable.html)
