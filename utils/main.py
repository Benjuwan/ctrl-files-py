import sys

from entry_validation import input_validation
from rename_files import rename_files


def run() -> None:
    try:
        part_mode = input("ファイル名の部分置換処理をスタート（y/n で入力）：")
        input_validation(part_mode)

        if part_mode == "n":
            sys.exit(
                """
ファイル名の全置換や部分置換、ファイル名の先頭または末尾へ特定文字列を追加したい場合
`utils/rename_files_sys.py`を実行してください。
実行コマンドは以下です。

```
# utils ディレクトリに移動（`cd utils`）して
python rename_files_sys.py <コマンド>

# mac の場合
# python3 rename_files_sys.py <コマンド>
```

※コマンドリストは以下です
- all：ファイル名の全置換
- part：ファイル名の部分置換（`ページ` -> `page`）
- add_begin：ファイル名の「先頭」に指定した文字列を追加
- add_end：ファイル名の「末尾」に指定した文字列を追加
"""
            )

        apply_dir_move = input("フォルダ移動を行いますか？（y/n で入力）：")
        input_validation(apply_dir_move)
        is_dir_move: bool = apply_dir_move == "y"

        apply_file_select = input(
            "ファイルを選択（※拡張子指定）しますか？（y/n で入力）："
        )
        input_validation(apply_file_select)
        is_file_select: bool = apply_file_select == "y"

        is_dirmove_fileselect: bool = is_dir_move and is_file_select

        if is_dirmove_fileselect:
            print("モード：フォルダ移動 + ファイル選択 + リネーム")
            rename_files("all")

        elif is_dir_move:
            print("モード：フォルダ移動 + リネーム")
            rename_files("dir_move")

        elif is_file_select:
            print("モード：ファイル選択 + リネーム")
            rename_files("files_select")
        else:
            print("モード：リネーム")
            rename_files()

    except Exception as e:
        print(f"コアモジュール main.py での処理実行エラー | {e}")
        return


run()

print("Done | すべての処理が完了しました.")
