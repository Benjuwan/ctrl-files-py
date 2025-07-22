import sys
import os
import glob

from rename_file_act_regular import rename_file_act_regular
from rename_file_act_add import rename_file_act_add


# リネーム処理のコア機能部分
def rename_files_sys() -> None:
    try:
        # `../file/rename`というパス文字列として正しく認識してもらうために os.path.join で文字列結合
        file_dir = os.path.join("..", "file", "rename")
        target_files = glob.glob(file_dir)

        # `../file/rename`フォルダが存在しない場合
        if len(target_files) == 0 and os.path.exists(f"{file_dir}") is False:
            # ルートに file_dir フォルダが存在しない場合のみ作成
            print(f"{file_dir}が存在しないので作成します")
            # 再帰的にディレクトリを作成（※指定したフォルダ構成通りに作成してくれる）
            os.makedirs(f"{file_dir}")
            return

        # 以下のコマンドライン引数の場合、入力文字に応じた処理を実行する
        com_lists = ["all", "part", "add_begin", "add_end"]
        attention_com_lists = f"""処理実行可能なモードは{com_lists}です
- all：ファイル名の全置換
- part：ファイル名の部分置換（`ページ` -> `page`）
- add_begin：ファイル名の「先頭」に指定した文字列を追加
- add_end：ファイル名の「末尾」に指定した文字列を追加
"""

        # 入力したコマンドライン引数が1つ未満（※何も入力せずとも[0]にはファイル名が入る）または1つ以上の場合
        if len(sys.argv) != 2 or len(sys.argv) > 2:
            print(f"1つのコマンドライン引数を入力してください\n{attention_com_lists}")
            return

        # com_lists 内の文字列でない場合
        elif sys.argv[1] not in com_lists:
            print(f"「{sys.argv[1]}」はモードに含まれていません\n{attention_com_lists}")
            return

        # モード（実行可能コマンド：all, part, add_begin, add_end）
        mode = sys.argv[1]

        numbering = input(
            "（任意）ファイルをナンバリングする\n`n-`ファイル名：先頭に追加する場合は「y」と入力\nファイル名`-n`：末尾に追加する場合は「n」と入力\n不要の場合は何も入力せず enterキーを押下："
        )

        if mode == "all":
            replace_all_str = input("入力した文字列で全置換：")
            rename_file_act_regular(target_files, numbering, replace_all_str)

        elif mode == "part":
            replace_str = input("リネーム前の対象文字列を入力：")
            target_str = input("リネーム名を入力：")
            rename_file_act_regular(target_files, numbering, replace_str, target_str)

        elif mode == "add_begin":
            add_begin_str = input("ファイル名の先頭に追加したい文字列：")
            rename_file_act_add(target_files, numbering, add_begin_str)

        elif mode == "add_end":
            add_end_str = input("ファイル名の末尾に追加したい文字列：")
            rename_file_act_add(target_files, numbering, add_end_str, is_begin=False)

    except Exception as e:
        print(
            f"リネーム処理のコア機能部分での処理実行エラー | `rename_files_sys.py` ： {e}"
        )
        return


if __name__ == "__main__":
    rename_files_sys()
