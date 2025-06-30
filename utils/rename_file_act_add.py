import glob
import os
import sys

from rename_features.add_begin_end import add_begin_end_numbering
from rename_features.add_begin_end import add_begin_end


# モード：add_ 系統ルート時におけるリネーム処理
def rename_file_act_add(
    target_file_dir: list[str] | None = None,
    numbering: str = "",
    replace_str: str = "",
    is_begin: bool = True,
) -> None:
    if target_file_dir is None:
        print(
            "処理対象フォルダが指定されていないようです\n処理する場合は rename_files_sys.py を通じて実行してください "
        )
        return

    # file ディレクトリ配下に複数のフォルダがあるかどうか判定するフラグ
    has_multi_dirs_filedir = len(target_file_dir) > 1

    # file ディレクトリ配下のフォルダから rename（処理対象ディレクトリ）を取得
    target_rename_dir = list(filter(lambda dir: dir.count("rename"), target_file_dir))

    # 処理対象ディレクトリ内の全てのファイルリスト（以下の内包表記からうまれるイテラブル）
    rename_files = [
        f for f in glob.glob(os.path.join(*target_rename_dir, "*")) if os.path.isfile(f)
    ]

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

    try:
        if is_add_numbering:
            # ナンバリング有りver
            add_begin_end_numbering(
                numbering,
                target_file_dir,
                rename_files,
                replace_str,
                has_multi_dirs_filedir,
            )
            return

        # ナンバリング無しver
        add_begin_end(
            target_file_dir,
            rename_files,
            replace_str,
            is_begin,
            has_multi_dirs_filedir,
        )

    except Exception as e:
        print(f"ファイル名の前後に文字列を追加する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_add()
