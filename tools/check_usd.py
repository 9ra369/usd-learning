"""USD ファイルを読み込んで、エラーやありがちなミスを報告する。

使い方:
    tools\\check                      # topics/ と scratch/ 以下をすべて
    tools\\check path\\to\\file.usda    # ファイルやフォルダを指定
    tools\\check --no-usdchecker      # usdchecker を省略して速く回す

判定:
    FAIL  正しく読み込めない（構文エラー・合成エラー・存在しない値型）
    WARN  読み込めるが怪しい（タイポっぽい属性名、未知のプリム型、usdchecker の指摘など）
    OK    問題なし
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

from pxr import Sdf, Tf, Usd, UsdGeom

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TARGETS = [ROOT / "topics", ROOT / "scratch"]
USD_EXTS = {".usda", ".usd", ".usdc", ".usdz"}

# スキーマで定義されていなくても普通に使う名前空間
FREE_NAMESPACES = ("primvars:", "xformOp:", "inputs:", "outputs:", "userProperties:")


def collect_files(targets):
    files = []
    for target in targets:
        if target.is_dir():
            files += sorted(p for p in target.rglob("*") if p.suffix in USD_EXTS)
        elif target.suffix in USD_EXTS:
            files.append(target)
        else:
            print(f"skip: {target}（USD ファイルではありません）", file=sys.stderr)
    return files


def check_prim(prim, errors, warnings):
    path = prim.GetPath()
    type_name = prim.GetTypeName()

    if type_name and not Usd.SchemaRegistry().FindConcretePrimDefinition(type_name):
        warnings.append(f"{path}: 型 '{type_name}' はスキーマに存在しません（タイポ？）")

    # usda は未知の値型名（doubel など）も読み込めてしまうので自前で検出する
    # （Usd 側の型はスキーマで補われてしまうので、レイヤーに書かれた型名を直接見る）
    for attr in prim.GetAuthoredAttributes():
        for spec in attr.GetPropertyStack():
            raw = spec.GetInfo("typeName")
            if raw and not Sdf.ValueTypeNames.Find(raw):
                errors.append(f"{path}: {attr.GetName()} の値型 '{raw}' は存在しません")

    prim_def = prim.GetPrimDefinition()
    for prop in prim.GetAuthoredProperties():
        name = prop.GetName()
        if prop.IsCustom() or name.startswith(FREE_NAMESPACES):
            continue
        # 見つからないときは None ではなく無効な（False になる）オブジェクトが返る
        if not prim_def.GetPropertyDefinition(name):
            warnings.append(
                f"{path}: '{name}' は {type_name or '型なしプリム'} のスキーマにない属性です"
                "（タイポ？ 意図的なら custom を付ける）"
            )

    for rel in prim.GetRelationships():
        for target in rel.GetTargets():
            if not prim.GetStage().GetObjectAtPath(target):
                warnings.append(f"{path}: {rel.GetName()} の参照先 {target} が存在しません")

    xformable = UsdGeom.Xformable(prim)
    if xformable:
        ordered = {op.GetOpName() for op in xformable.GetOrderedXformOps()}
        for attr in prim.GetAuthoredAttributes():
            name = attr.GetName()
            if name.startswith("xformOp:") and name not in ordered:
                warnings.append(f"{path}: {name} が xformOpOrder に入っていないため無視されます")


def run_usdchecker(file):
    try:
        result = subprocess.run(
            ["usdchecker", str(file)], capture_output=True, text=True, errors="replace"
        )
    except FileNotFoundError:
        return ["usdchecker が見つかりません（tools\\check から実行してください）"]
    if result.returncode == 0:
        return []
    lines = [line.strip() for line in (result.stdout + result.stderr).splitlines()]
    return ["usdchecker: " + line for line in lines if line and line != "Failed!"]


def check_file(file, use_usdchecker):
    errors, warnings = [], []

    try:
        layer = Sdf.Layer.FindOrOpen(str(file))
    except Tf.ErrorException as e:
        # "...textParserHelpers.h : 'file.usda:6:1: Expected } ...'" から後半だけ取り出す
        match = re.search(r"'([^']*:\d+:\d+: .*)'", str(e), re.DOTALL)
        return [f"構文エラー: {match.group(1).strip() if match else str(e).strip()}"], []
    if layer is None:
        return ["ファイルを開けませんでした"], []

    stage = Usd.Stage.Open(layer)
    errors += [f"合成エラー: {e}" for e in stage.GetCompositionErrors()]

    for prim in stage.TraverseAll():
        check_prim(prim, errors, warnings)

    if use_usdchecker:
        # upAxis や metersPerUnit の未指定なども拾うが、読み込み自体はできるので WARN 扱い
        warnings += run_usdchecker(file)
    elif not stage.GetDefaultPrim():
        warnings.append("defaultPrim が設定されていません")
    return errors, warnings


def main():
    sys.stdout.reconfigure(errors="replace")
    parser = argparse.ArgumentParser(description="USD ファイルのチェック")
    parser.add_argument("paths", nargs="*", type=Path, help="ファイルまたはフォルダ")
    parser.add_argument("--no-usdchecker", action="store_true", help="usdchecker を実行しない")
    args = parser.parse_args()

    files = collect_files(args.paths or DEFAULT_TARGETS)
    if not files:
        print("チェック対象の USD ファイルがありません")
        return 0

    counts = {"OK": 0, "WARN": 0, "FAIL": 0}
    for file in files:
        errors, warnings = check_file(file.resolve(), not args.no_usdchecker)
        status = "FAIL" if errors else "WARN" if warnings else "OK"
        counts[status] += 1
        try:
            shown = file.resolve().relative_to(ROOT)
        except ValueError:
            shown = file
        print(f"{status:<5} {shown}")
        for msg in errors + warnings:
            print(f"      - {msg}")

    print(f"\n{len(files)} files: {counts['OK']} OK, {counts['WARN']} WARN, {counts['FAIL']} FAIL")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
