import unicodedata  # Unicodeデータベースへのアクセスを提供
import shutil
import os

# インポートエラー状態だが utils.files_move と正してしまうと ModuleNotFoundError が発生する
from files_move import files_move


# ナンバリング有りver
def add_begin_end_numbering(
    numbering: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    is_begin: bool | None = None,
    run_move_dir: bool | None = None,
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

        add_begin: str = (
            f"{i}-{replace_str}-{target_filename}{extend}"
            if numbering == "y"
            else f"{replace_str}-{i}-{target_filename}{extend}"
        )

        add_end: str = (
            f"{target_filename}-{i}-{replace_str}{extend}"
            if numbering == "y"
            else f"{target_filename}-{replace_str}-{i}{extend}"
        )

        new_name = os.path.join(
            dir_name,
            add_begin if is_begin else add_end,
        )
        print(f"{normalized_path} -> {new_name}")
        os.rename(normalized_path, new_name)

        if run_move_dir and target_file_dir is not None:
            move_dirname = target_file_dir[0]
            files_move(move_dirname)


# ナンバリング無しver
def add_begin_end(
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    is_begin: bool | None = None,
    run_move_dir: bool | None = None,
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

        if run_move_dir and target_file_dir is not None:
            move_dirname = target_file_dir[0]
            files_move(move_dirname)


if __name__ == "__main__":
    add_begin_end_numbering()
    add_begin_end()
