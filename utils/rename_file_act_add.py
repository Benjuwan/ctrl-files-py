import glob
import os
import sys

# rename_features. からの相対パスでないと ModuleNotFoundError が発生する
from rename_features.add_begin_end import add_begin_end_numbering
from rename_features.add_begin_end import add_begin_end


# モード：add_ 系統ルート時におけるリネーム処理
def rename_file_act_add(
    target_file_dir: list[str] | None = None,
    numbering: str = "",
    replace_str: str = "",
    is_begin: bool = True,
    mode: str = "",
) -> None:
    if target_file_dir is None:
        print(
            "処理対象フォルダが指定されていないようです\n処理する場合は rename_files_sys.py を通じて実行してください "
        )
        return

    try:
        is_mode_all: bool = mode == "all"
        is_files_select: bool = mode == "files_select"
        is_mode_dir_move: bool = mode == "dir_move"

        # file ディレクトリ配下のフォルダから rename（処理対象ディレクトリ）という文字列を含んだフォルダまたはファイルリストを取得
        target_rename_dir = list(
            filter(lambda dir: dir.count("rename"), target_file_dir)
        )

        # 処理対象ディレクトリ内の全てのファイルリスト（以下の内包表記からうまれるイテラブル）
        rename_files = [
            f
            for f in glob.glob(os.path.join(*target_rename_dir, "*"))
            if os.path.isfile(f)
        ]

        # ファイル選択処理の場合はそのまま target_rename_dir（拡張子でのフィルター済みイテラブル）を処理対象にする
        if is_files_select:
            rename_files = target_rename_dir

        if len(rename_files) == 0:
            print(f"{target_rename_dir}内のファイルは現在「{len(rename_files)}」件です")
            return

        is_replace_str = len(replace_str) == 0
        if is_replace_str:
            print("リネーム対象文字列が未入力なようです")
            return

        is_check_correct_numbering_code = numbering == "y" or numbering == "n"
        is_add_numbering = len(numbering) > 0 and is_check_correct_numbering_code

        if len(numbering) > 0 and is_check_correct_numbering_code is False:
            sys.exit(
                f"\n処理受付可能なコードは「y」または「n」のみです\n入力されたコードは「{numbering}」なので処理を中断します\n"
            )

        run_move_dir: bool = is_mode_all or is_mode_dir_move

        if is_add_numbering:
            # ナンバリング有りver
            add_begin_end_numbering(
                numbering,
                target_file_dir,
                rename_files,
                replace_str,
                is_begin,
                run_move_dir,
            )
            return

        # ナンバリング無しver
        add_begin_end(
            target_file_dir,
            rename_files,
            replace_str,
            is_begin,
            run_move_dir,
        )

    except Exception as e:
        print(f"ファイル名の前後に文字列を追加する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_add()
