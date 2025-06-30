import unicodedata  # Unicodeデータベースへのアクセスを提供
import shutil
import os

from move_dirs import move_dir


# ナンバリング有りver
def add_begin_end_numbering(
    numbering: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    has_multi_dirs_filedir: bool | None = None,
) -> None:
    if rename_files is None:
        return

    for i, file in enumerate(rename_files, 1):
        # 文字列を正規化（NFKCで合成済み文字として扱う）
        normalized_path = unicodedata.normalize("NFKC", file)

        shutil.copy2(normalized_path, normalized_path + ".bak")

        dir_name = os.path.dirname(normalized_path)

        # os.path.splitext と os.path.basename で確実にファイル名と拡張子を取得する
        target_filename = os.path.basename(os.path.splitext(normalized_path)[0])
        extend = os.path.splitext(normalized_path)[1]

        new_name = os.path.join(
            dir_name,
            f"{i}-{replace_str}-{target_filename}{extend}"
            if numbering == "y"
            else f"{target_filename}-{replace_str}-{i}{extend}",
        )
        print(f"{normalized_path} -> {new_name}")
        os.rename(normalized_path, new_name)

        # フォルダ移動処理が有効の場合は以下の処理に進む
        if has_multi_dirs_filedir:
            move_dir(target_file_dir)


# ナンバリング無しver
def add_begin_end(
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    is_begin: bool | None = None,
    has_multi_dirs_filedir: bool | None = None,
) -> None:
    if rename_files is None:
        return

    for file in rename_files:
        normalized_path = unicodedata.normalize("NFKC", file)

        shutil.copy2(normalized_path, normalized_path + ".bak")

        dir_name = os.path.dirname(normalized_path)
        target_filename = os.path.basename(os.path.splitext(normalized_path)[0])
        extend = os.path.splitext(normalized_path)[1]

        new_name = os.path.join(
            dir_name,
            f"{replace_str}-{target_filename}{extend}"
            if is_begin
            else f"{target_filename}-{replace_str}{extend}",
        )
        print(f"{normalized_path} -> {new_name}")
        os.rename(normalized_path, new_name)

        # フォルダ移動処理が有効の場合は以下の処理に進む
        if has_multi_dirs_filedir:
            move_dir(target_file_dir)


if __name__ == "__main__":
    add_begin_end_numbering()
    add_begin_end()
