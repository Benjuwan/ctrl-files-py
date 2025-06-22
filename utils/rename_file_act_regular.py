import glob
import shutil
import os


# モード：all, part ルート時におけるリネーム処理
def rename_file_act_regular(
    target_file_dir: list[str] | None = None,
    numbering: str = "",
    replace_str: str = "",
    target_str: str | None = None,
) -> None:
    if target_file_dir is None:
        return

    # 処理対象ディレクトリ内の全てのファイルリスト（以下の内包表記からうまれるイテラブル）
    rename_files = [
        f  # 式：ループ変数fをそのまま取得
        for f  # ループ変数：glob結果の各要素（target_file_dirフォルダ内の全データ）を順次取得
        # アンパック（*イテラブル）： JavaScriptのスプレッド構文（...）と同じようにリストやタプルの中身を展開して渡す仕組み
        in glob.glob(os.path.join(*target_file_dir, "*"))
        # isfile：対象がファイルかどうかを判定（ディレクトリを除外してファイルのみを抽出）
        if os.path.isfile(f)
    ]

    print(rename_files, target_file_dir, target_file_dir[0])

    if len(rename_files) == 0:
        print(f"{target_file_dir}内のファイルは現在「{len(rename_files)}」件です")
        return

    is_add_numbering = len(numbering) > 0 and (
        numbering.count("y") or numbering.count("n")
    )

    try:
        # part：ナンバリング有りver
        if is_add_numbering and target_str is not None:
            for i, file in enumerate(rename_files, 1):
                # バックアップを作成（.bak：バックアップファイルを意味する拡張子）
                shutil.copy2(file, file + ".bak")

                # 文字列置換
                adjust_filename = file.replace(target_str, replace_str)

                # ファイル名とディレクトリを分離
                dir_name = os.path.dirname(adjust_filename)
                base_name = os.path.basename(adjust_filename)
                name_without_ext = os.path.splitext(base_name)[0]
                extends = file.split(".")[-1]

                # ファイル名の変更（`dir_name`と組み合わせてフルパス生成）
                new_name = os.path.join(
                    dir_name,
                    f"{i}-{name_without_ext}.{extends}"
                    if numbering == "y"
                    else f"{name_without_ext}-{i}.{extends}",
                )
                print(file, new_name)
                os.rename(file, new_name)
            return

        # part：ナンバリング無しver
        if target_str is not None:
            for file in rename_files:
                shutil.copy2(file, file + ".bak")
                adjust_filename = file.replace(target_str, replace_str)
                os.rename(file, adjust_filename)
            return

        # all：ナンバリング有りver
        if is_add_numbering:
            for i, file in enumerate(rename_files, 1):
                shutil.copy2(file, file + ".bak")

                dir_name = os.path.dirname(file)
                extends = file.split(".")[-1]

                new_name = os.path.join(
                    dir_name,
                    f"{i}-{replace_str}.{extends}"
                    if numbering == "y"
                    else f"{replace_str}-{i}.{extends}",
                )
                print(file, new_name)
                os.rename(file, new_name)
            return

        # all：ナンバリング無しver
        else:
            for file in rename_files:
                shutil.copy2(file, file + ".bak")

                dir_name = os.path.dirname(file)
                extends = file.split(".")[-1]

                new_name = os.path.join(dir_name, f"{replace_str}.{extends}")
                os.rename(file, new_name)
            return

    except Exception as e:
        print(f"ファイル名の置換処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_regular()
