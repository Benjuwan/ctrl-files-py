import shutil
import os

from move_dirs import move_dir


# part：ナンバリング有りver
def regular_part_numbering(
    numbering: str | None = None,
    target_str: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    has_multi_dirs_filedir: bool | None = None,
) -> None:
    if rename_files is None or replace_str is None or target_str is None:
        return

    for i, file in enumerate(rename_files, 1):
        # 置換対象文字を含んでいない場合はスキップ
        if file.count(replace_str) == 0:
            print(f"{i} --- {file}は置換対象外です")
            continue

        # バックアップを作成（.bak：バックアップファイルを意味する拡張子）
        shutil.copy2(file, file + ".bak")

        # 文字列置換
        target_replace_str = replace_str
        replace_result_str = target_str
        adjust_filename = file.replace(target_replace_str, replace_result_str)

        # ファイル名とディレクトリを分離
        dir_name = os.path.dirname(adjust_filename)
        base_name = os.path.basename(adjust_filename)
        name_without_ext = os.path.splitext(base_name)[0]
        # os.path.splitext で確実に拡張子を取得する
        extend = os.path.splitext(base_name)[1]

        # ファイル名の変更（`dir_name`と組み合わせてフルパス生成）
        new_name = os.path.join(
            dir_name,
            f"{i}-{name_without_ext}{extend}"
            if numbering == "y"
            else f"{name_without_ext}-{i}{extend}",
        )

        print(f"{file} -> {new_name}")
        os.rename(file, new_name)

        # フォルダ移動処理が有効の場合は以下の処理に進む
        if has_multi_dirs_filedir:
            move_dir(target_file_dir)


# part：ナンバリング無しver
def regular_part(
    target_str: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    has_multi_dirs_filedir: bool | None = None,
) -> None:
    if rename_files is None or replace_str is None:
        return

    if target_str is not None:
        for file in rename_files:
            if file.count(replace_str) == 0:
                continue

            shutil.copy2(file, file + ".bak")

            target_replace_str = replace_str
            replace_result_str = target_str
            adjust_filename = file.replace(target_replace_str, replace_result_str)

            print(f"{file} -> {adjust_filename}")
            os.rename(file, adjust_filename)

            # フォルダ移動処理が有効の場合は以下の処理に進む
            if has_multi_dirs_filedir:
                move_dir(target_file_dir)


if __name__ == "__main__":
    regular_part_numbering()
    regular_part()
