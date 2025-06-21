import glob
import shutil
import os


# モード：add_ 系統ルート時におけるリネーム処理
def rename_file_act_add(
    target_file_dir: list[str] = [],
    numbering: str = "",
    replace_str: str = "",
    is_begin: bool = True,
) -> None:
    # 処理対象ディレクトリ内の全てのファイルリスト（イテラブル）
    rename_files = (
        target_file_dir
        if numbering == "no_sys_args"
        # アンパック（*）： JavaScriptのスプレッド構文（...）と同じようにリストやタプルの中身を展開して渡す仕組み
        else glob.glob(os.path.join(*target_file_dir, "*"))
    )

    if len(target_file_dir) == 0:
        print(f"{target_file_dir}内のファイルは現在「{len(rename_files)}」件です")
        return

    is_add_numbering = len(numbering) > 0 and (
        numbering.count("y") or numbering.count("n")
    )

    try:
        # ナンバリング有りver
        if is_add_numbering:
            for i, file in enumerate(rename_files, 1):
                shutil.copy2(file, file + ".bak")
                new_name = (
                    f"{i}-{replace_str}-{file}"
                    if numbering == "y"
                    else f"{file}-{replace_str}-{i}"
                )
                os.rename(file, new_name)
            return  # 無用な後続処理を避けるため明示的に処理終了

        for file in rename_files:
            shutil.copy2(file, file + ".bak")
            adjust_filename = (
                f"{replace_str}-{file}" if is_begin else f"{file}-{replace_str}"
            )
            os.rename(file, adjust_filename)
        return

    except Exception as e:
        print(f"ファイル名の前後に文字列を追加する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_add()
