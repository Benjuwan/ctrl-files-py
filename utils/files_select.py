import glob
import os
import sys

from entry_validation import check_entry_count
from rename_file_act_regular import rename_file_act_regular


def files_select(
    entry_replace_str: str | None = None,
    entry_target_str: str | None = None,
    mode: str = "files_select",
) -> None:
    if entry_replace_str is None:
        entry_replace_str = input("1. リネーム前の対象文字列を入力：")
        check_entry_count("リネーム前の対象文字列", entry_replace_str)

    if entry_target_str is None:
        entry_target_str = input("2. リネーム名を入力：")
        check_entry_count("リネーム名", entry_target_str)

    try:
        extends = input("処理対象ファイルの拡張子を入力：")
        check_entry_count("拡張子名", extends)

        file_dir_path = os.path.join(
            "..",
            "file",
            "rename",
            f"*.{extends}",
        )

        # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
        target_files = glob.glob(file_dir_path, recursive=True)

        if len(target_files) == 0:
            sys.exit(
                f"`files_select` | ../file/renameフォルダまたは当該フォルダ内に「{extends}」拡張子ファイルは存在しません"
            )

        is_exist_replace_file = any(
            [file.count(entry_replace_str) for file in target_files]
        )

        if is_exist_replace_file is False:
            sys.exit(
                f"`files_select` | ファイル名に「{entry_replace_str}」を含んだ「{extends}」拡張子ファイルは存在しません"
            )

        # target_files（拡張子ファイルでフィルター済み）を渡して、部分置換モードで処理を進める
        rename_file_act_regular(
            target_files, "", entry_replace_str, entry_target_str, mode
        )

    except Exception as e:
        print(f"処理対象ファイルを選択する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    files_select()
