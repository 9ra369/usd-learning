# purpose と proxy

重いモデルに軽い代役を付けて、作業中は代役、最終レンダリングでは本物を表示する仕組み。

## purpose

`uniform token purpose = "..."` で、そのプリムを「どの用途で表示するか」を決める。

| 値 | 用途 |
|---|---|
| `"default"` | 常に表示（未指定時はこれ） |
| `"render"` | 最終レンダリング用。重いモデル |
| `"proxy"` | 作業中のビューポート用。軽い代役 |
| `"guide"` | ガイド表示。レンダリングには出ない |

purpose は子に継承される。親に `"proxy"` を付ければ中身全部が proxy になる。

## proxyPrim

```usda
def Cube "Box"
{
    uniform token purpose = "render"
    rel proxyPrim = </World/BoxProxy>
}
```

render 側から proxy 側を指すリレーションシップ。**描画には影響しない**。ツールが「Box の代役は BoxProxy」と辿るためのもの。

## サンプル

- [box_proxy.usda](box_proxy.usda): Box（render）に Capsule の代役（proxy）を付けたもの。Ball は default

## 確認

usdview: **Display → Display Purposes** で Proxy / Render を切り替える。

```bat
tools\view topics\purpose\box_proxy.usda
tools\render topics\purpose\box_proxy.usda                     :: usdrecord の既定は proxy → Capsule が写る
tools\render topics\purpose\box_proxy.usda --purposes render   :: Box が写る
```

## 参考

- [UsdGeomImageable（purpose）](https://openusd.org/release/api/class_usd_geom_imageable.html)
