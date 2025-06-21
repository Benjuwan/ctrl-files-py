import glob
import shutil
import os


# モード：all, part ルート時におけるリネーム処理
def rename_file_act_regular(
    target_file_dir: list[str] = [],
    numbering: str = "",
    replace_str: str = "",
    target_str: str | None = None,
) -> None:
    # 処理対象ディレクトリ内の全てのファイルリスト（イテラブル）
    rename_files = (
        target_file_dir
        if numbering == "no_sys_args"
        # アンパック（*）： JavaScriptのスプレッド構文（...）と同じようにリストやタプルの中身を展開して渡す仕組み
        else glob.glob(os.path.join(*target_file_dir, "*"))
        # f"{target_file_dir}/*"
    )

    if len(rename_files) == 0:
        print(f"{target_file_dir}内のファイルは現在「{len(rename_files)}」件です")
        return

    is_add_numbering = len(numbering) > 0 and (
        numbering.count("y") or numbering.count("n")
    )

    try:
        # all：ナンバリング有りver
        if is_add_numbering:
            for i, file in enumerate(rename_files, 1):
                # バックアップを作成（.bak：バックアップファイルを意味する拡張子）
                shutil.copy2(file, file + ".bak")
                # ファイル名の変更
                new_name = (
                    f"{i}-{replace_str}" if numbering == "y" else f"{replace_str}-{i}"
                )
                os.rename(file, new_name)
            return  # 無用な後続処理を避けるため明示的に処理終了

        # part：ナンバリング有りver
        if is_add_numbering and target_str is not None:
            for i, file in enumerate(rename_files, 1):
                shutil.copy2(file, file + ".bak")
                adjust_filename = file.replace(target_str, replace_str)
                new_name = (
                    f"{i}-{adjust_filename}"
                    if numbering == "y"
                    else f"{adjust_filename}-{i}"
                )
                os.rename(file, new_name)
            return

        # part：ナンバリング無しver
        if target_str is not None:
            for file in rename_files:
                shutil.copy2(file, file + ".bak")
                adjust_filename = file.replace(target_str, replace_str)
                os.rename(file, adjust_filename)
            return

        # all：ナンバリング無しver
        else:
            for file in rename_files:
                shutil.copy2(file, file + ".bak")
                os.rename(file, replace_str)
            return

    except Exception as e:
        print(f"ファイル名の置換処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_regular()
