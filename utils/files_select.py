import glob
import os
import sys

from rename_files_sys import rename_files_sys


def files_select(extends: str = "*", entry_replace_str: str | None = None) -> None:
    if entry_replace_str is None:
        return

    file_dir_path = os.path.join(
        "..",
        "file",
        "rename",
        f"{extends if len(extends) == 1 else f'*.{extends}'}",
    )

    # サブディレクトリも処理対象（＝指定したディレクトリ全体が処理対象）
    target_files = glob.glob(file_dir_path, recursive=True)

    if len(target_files) == 0:
        # sys.exit で全体の処理中断
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

    try:
        pass
        # 拡張子ファイルでフィルター済みの target_files を渡して処理を進める
        # rename_files_sys(target_files, entry_replace_str, entry_target_str)

    except Exception as e:
        print(f"処理対象ファイルを選択する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    files_select()
