import unicodedata  # Unicodeデータベースへのアクセスを提供
import shutil
import os

# インポートエラー状態だが utils.files_move と正してしまうと ModuleNotFoundError が発生する
from files_move import files_move


# 同一拡張子のファイルが無いかチェックするプライベートメソッド
def _check_duplicated_extends(filelist: list[str]) -> bool:
    extends = []
    duplicated_extends_count = 0

    for file in filelist:
        # 文字列を正規化（NFKCで合成済み文字として扱う）
        normalized_path = unicodedata.normalize("NFKC", file)

        # os.path.splitext で確実に拡張子を取得する
        extend = os.path.splitext(normalized_path)[1]
        extends.append(extend)

        for ext in extends:
            if normalized_path.count(ext):
                duplicated_extends_count += 1

    if duplicated_extends_count > 0:
        return True

    return False


# all：ナンバリング有りver
def regular_all_numbering(
    numbering: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    run_move_dir: bool | None = None,
) -> None:
    if rename_files is None:
        return

    for i, file in enumerate(rename_files, 1):
        normalized_path = unicodedata.normalize("NFKC", file)

        shutil.copy2(normalized_path, normalized_path + ".bak")

        dir_name = os.path.dirname(normalized_path)
        extend = os.path.splitext(normalized_path)[1]

        new_name = os.path.join(
            dir_name,
            f"{i}-{replace_str}{extend}"
            if numbering == "y"
            else f"{replace_str}-{i}{extend}",
        )

        print(f"{normalized_path} -> {new_name}")
        os.rename(normalized_path, new_name)

        if run_move_dir and target_file_dir is not None:
            move_dirname = target_file_dir[0]
            files_move(move_dirname)


# all：ナンバリング無しver
def regular_all(
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    run_move_dir: bool | None = None,
) -> None:
    if rename_files is None:
        return

    for file in rename_files:
        normalized_path = unicodedata.normalize("NFKC", file)

        # 同一拡張子のファイルが無いかチェック
        is_check_duplicated_extends = _check_duplicated_extends(rename_files)
        if is_check_duplicated_extends:
            print("同じ拡張子のファイルがあります。重複ファイルは作成不可")
            return

        shutil.copy2(normalized_path, normalized_path + ".bak")

        dir_name = os.path.dirname(normalized_path)
        extend = os.path.splitext(normalized_path)[1]

        new_name = os.path.join(dir_name, f"{replace_str}{extend}")

        print(f"{normalized_path} -> {new_name}")
        os.rename(normalized_path, new_name)

        if run_move_dir and target_file_dir is not None:
            move_dirname = target_file_dir[0]
            files_move(move_dirname)


if __name__ == "__main__":
    regular_all_numbering()
    regular_all()
