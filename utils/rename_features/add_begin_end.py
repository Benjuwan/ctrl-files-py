import unicodedata  # Unicodeデータベースへのアクセスを提供
import shutil
import os

# インポートエラー状態だが utils.files_move と正してしまうと ModuleNotFoundError が発生する
from files_move import files_move

# インポートエラー状態だが rename_features.prefix_today_firstline と記述しないと ModuleNotFoundError が発生する
from rename_features.prefix_today_firstline import prefix_today_firstline


# ナンバリング有りver
def add_begin_end_numbering(
    numbering: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    is_begin: bool | None = None,
    run_move_dir: bool | None = None,
) -> None:
    try:
        if rename_files is None:
            return

        prefix_today: str | None = prefix_today_firstline()

        for i, file in enumerate(rename_files, 1):
            # 文字列を正規化（NFKCで合成済み文字として扱う）
            normalized_path = unicodedata.normalize("NFKC", file)

            shutil.copy2(normalized_path, normalized_path + ".bak")

            dir_name = os.path.dirname(normalized_path)

            # os.path.splitext と os.path.basename で確実にファイル名と拡張子を取得する
            target_filename = os.path.basename(os.path.splitext(normalized_path)[0])
            extend = os.path.splitext(normalized_path)[1]

            add_begin: str = (
                f"{prefix_today}{i}-{replace_str}-{target_filename}{extend}"
                if numbering == "y"
                else f"{prefix_today}{replace_str}-{i}-{target_filename}{extend}"
            )

            add_end: str = (
                f"{prefix_today}{target_filename}-{i}-{replace_str}{extend}"
                if numbering == "y"
                else f"{prefix_today}{target_filename}-{replace_str}-{i}{extend}"
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

    except Exception as e:
        print(
            f"ナンバリング + ファイル名前後への文字列を追加する処理時にエラーが発生  | `add_begin_end.py` ： {e}"
        )
        return


# ナンバリング無しver
def add_begin_end(
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    is_begin: bool | None = None,
    run_move_dir: bool | None = None,
) -> None:
    try:
        if rename_files is None:
            return

        prefix_today: str | None = prefix_today_firstline()

        for file in rename_files:
            normalized_path = unicodedata.normalize("NFKC", file)

            shutil.copy2(normalized_path, normalized_path + ".bak")

            dir_name = os.path.dirname(normalized_path)
            target_filename = os.path.basename(os.path.splitext(normalized_path)[0])
            extend = os.path.splitext(normalized_path)[1]

            new_name = os.path.join(
                dir_name,
                f"{prefix_today}{replace_str}-{target_filename}{extend}"
                if is_begin
                else f"{prefix_today}{target_filename}-{replace_str}{extend}",
            )
            print(f"{normalized_path} -> {new_name}")
            os.rename(normalized_path, new_name)

            if run_move_dir and target_file_dir is not None:
                move_dirname = target_file_dir[0]
                files_move(move_dirname)

    except Exception as e:
        print(
            f"ファイル名前後への文字列を追加する処理時にエラーが発生 | `add_begin_end.py` ： {e}"
        )
        return


if __name__ == "__main__":
    add_begin_end_numbering()
    add_begin_end()
