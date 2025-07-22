import unicodedata  # Unicodeデータベースへのアクセスを提供
import shutil
import os

# インポートエラー状態だが utils.files_move と正してしまうと ModuleNotFoundError が発生する
from files_move import files_move


# part：ナンバリング有りver
def regular_part_numbering(
    numbering: str | None = None,
    target_str: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    run_move_dir: bool | None = None,
) -> None:
    try:
        if rename_files is None or replace_str is None or target_str is None:
            return

        # 処理対象ファイルの連番用カウンター
        target_file_counter = 0

        for i, file in enumerate(rename_files, 1):
            # 文字列を正規化（NFKCで合成済み文字として扱う）
            normalized_path = unicodedata.normalize("NFKC", file)

            # 置換対象文字を含んでいない場合はスキップ
            if normalized_path.count(replace_str) == 0:
                print(f"{i} --- {normalized_path}は置換対象外です")
                continue

            # 連番用カウンターに加算
            target_file_counter = target_file_counter + 1

            # バックアップを作成（.bak：バックアップファイルを意味する拡張子）
            shutil.copy2(normalized_path, normalized_path + ".bak")

            # 文字列置換
            target_replace_str = replace_str
            replace_result_str = target_str
            adjust_filename = normalized_path.replace(
                target_replace_str, replace_result_str
            )

            # ファイル名とディレクトリを分離
            dir_name = os.path.dirname(adjust_filename)
            base_name = os.path.basename(adjust_filename)
            name_without_ext = os.path.splitext(base_name)[0]
            # os.path.splitext で確実に拡張子を取得する
            extend = os.path.splitext(base_name)[1]

            # ファイル名の変更（`dir_name`と組み合わせてフルパス生成）
            new_name = os.path.join(
                dir_name,
                f"{target_file_counter}-{name_without_ext}{extend}"
                if numbering == "y"
                else f"{name_without_ext}-{target_file_counter}{extend}",
            )

            print(f"{normalized_path} -> {new_name}")
            os.rename(normalized_path, new_name)

            if run_move_dir and target_file_dir is not None:
                move_dirname = target_file_dir[0]
                files_move(move_dirname, replace_result_str)

    except Exception as e:
        print(f"ナンバリング + 部分置換処理時にエラーが発生 | `regular_part.py` ： {e}")
        return


# part：ナンバリング無しver
def regular_part(
    target_str: str | None = None,
    target_file_dir: list[str] | None = None,
    rename_files: list[str] | None = None,
    replace_str: str | None = None,
    run_move_dir: bool | None = None,
) -> None:
    try:
        if rename_files is None or replace_str is None:
            return

        if target_str is not None:
            for file in rename_files:
                normalized_path = unicodedata.normalize("NFKC", file)

                if normalized_path.count(replace_str) == 0:
                    continue

                shutil.copy2(normalized_path, normalized_path + ".bak")

                target_replace_str = replace_str
                replace_result_str = target_str
                adjust_filename = normalized_path.replace(
                    target_replace_str, replace_result_str
                )

                print(f"{normalized_path} -> {adjust_filename}")
                os.rename(normalized_path, adjust_filename)

                if run_move_dir and target_file_dir is not None:
                    move_dirname = target_file_dir[0]
                    files_move(move_dirname, replace_result_str)

    except Exception as e:
        print(f"部分置換処理時にエラーが発生 | `regular_part.py` ： {e}")
        return


if __name__ == "__main__":
    regular_part_numbering()
    regular_part()
