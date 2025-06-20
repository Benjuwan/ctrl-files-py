import sys
import os
import glob
import shutil


# --- モード：all, part ルート時におけるリネーム処理のプライベートメソッド
def _rename_file_act(
    rename_files: list[str],
    numbering: str,
    replace_str: str,
    target_str: str | None = None,
) -> None:
    is_add_numbering = len(numbering) > 0 and (
        numbering.count("y") or numbering.count("n")
    )

    try:
        # all：ナンバリング有りver
        if is_add_numbering:
            for i, file in enumerate(rename_files, 1):
                # バックアップを作成（.bak：バックアップファイルを意味する拡張子）
                shutil.copy2(file, file + ".bak")
                # ファイル名の変更
                new_name = (
                    f"{i}-{replace_str}" if numbering == "y" else f"{replace_str}-{i}"
                )
                os.rename(file, new_name)
            return  # 無用な後続処理を避けるため明示的に処理終了

        # part：ナンバリング有りver
        if is_add_numbering and target_str is not None:
            for i, file in enumerate(rename_files, 1):
                shutil.copy2(file, file + ".bak")
                adjust_filename = file.replace(target_str, replace_str)
                new_name = (
                    f"{i}-{adjust_filename}"
                    if numbering == "y"
                    else f"{adjust_filename}-{i}"
                )
                os.rename(file, new_name)
            return

        # part：ナンバリング無しver
        if target_str is not None:
            for file in rename_files:
                shutil.copy2(file, file + ".bak")
                adjust_filename = file.replace(target_str, replace_str)
                os.rename(file, adjust_filename)
            return

        # all：ナンバリング無しver
        else:
            for file in rename_files:
                shutil.copy2(file, file + ".bak")
                os.rename(file, replace_str)
            return

    except Exception as e:
        print(f"ファイル名の置換処理実行エラー | {e}")
        return


# --- モード：add_ 系統ルート時におけるリネーム処理のプライベートメソッド
def _rename_file_act_mode_add(
    rename_files: list[str], numbering: str, replace_str: str, is_begin: bool = True
) -> None:
    is_add_numbering = len(numbering) > 0 and (
        numbering.count("y") or numbering.count("n")
    )

    try:
        # ナンバリング有りver
        if is_add_numbering:
            for i, file in enumerate(rename_files, 1):
                shutil.copy2(file, file + ".bak")
                new_name = (
                    f"{i}-{replace_str}-{file}"
                    if numbering == "y"
                    else f"{file}-{replace_str}-{i}"
                )
                os.rename(file, new_name)
            return  # 無用な後続処理を避けるため明示的に処理終了

        for file in rename_files:
            shutil.copy2(file, file + ".bak")
            adjust_filename = (
                f"{replace_str}-{file}" if is_begin else f"{file}-{replace_str}"
            )
            os.rename(file, adjust_filename)
        return

    except Exception as e:
        print(f"ファイル名の前後に文字列を追加する処理実行エラー | {e}")
        return


# リネーム処理のコア機能部分
def rename_files_sys(rename_files_dir: list[str] | None = None) -> None:
    """
    # 指定した位置（インデックス）の値を取得
    # sys.argv[0]  # プログラム名
    # sys.argv[1]  # 第一引数：モード（ all, part, add_begin, add_end ）
    """

    # ----- main.py 経由の処理ルート
    if rename_files_dir is not None:
        if len(rename_files_dir) == 0:
            sys.exit("処理対象フォルダまたはファイルが存在しないようです")

        replace_str = input(
            f"{rename_files_dir}フォルダ内の全ファイル名を入力文字で置換："
        )
        target_str = input(
            f"{rename_files_dir}フォルダ内の全ファイル名の置換対象となる文字列を入力："
        )

        _rename_file_act(rename_files_dir, "", replace_str, target_str)
        return

    # ----- rename_files_sys.py 単体実行の処理ルート
    try:
        # 処理対象ディレクトリパス
        # ※`../file/rename`というパス文字列として正しく認識してもらうために os.path.join で文字列結合
        file_dir = os.path.join("..", "file", "rename")
        # 処理対象ディレクトリ内の全てのファイルリスト（イテラブル）
        rename_files = glob.glob(os.path.join(file_dir, "*"))

        # `../file/rename`フォルダまたは当該フォルダ内にファイルが一切ない場合
        if len(rename_files) == 0:
            if os.path.exists(f"{file_dir}") is False:
                # ルートに file_dir フォルダが存在しない場合のみ作成
                print(f"{file_dir}が存在しないので作成します")
                # 再帰的にディレクトリを作成（※指定したフォルダ構成通りに作成してくれる）
                os.makedirs(f"{file_dir}")
                return

            print(f"{file_dir}内のファイルは現在「{len(rename_files)}」件です")
            return

        # 以下のコマンドライン引数の場合、入力文字に応じた処理を実行する
        com_lists = ["all", "part", "add_begin", "add_end"]
        attention_com_lists = f"""処理実行可能なモードは{com_lists}です
- all：ファイル名の全置換
- part：ファイル名の部分置換（`ページ` -> `page`）
- add_begin：ファイル名の「先頭」に指定した文字列を追加
- add_end：ファイル名の「末尾」に指定した文字列を追加
"""
        print(sys.argv)

        # 入力したコマンドライン引数が1つ未満（※何も入力せずとも[0]にはファイル名が入る）または1つ以上の場合
        if len(sys.argv) != 2 or len(sys.argv) > 2:
            print(f"1つのコマンドライン引数を入力してください\n{attention_com_lists}")
            return

        # com_lists 内の文字列でない場合
        elif sys.argv[1] not in com_lists:
            print(f"「{sys.argv[1]}」はモードに含まれていません\n{attention_com_lists}")
            return

        mode = sys.argv[1]  # モード

        numbering = input(
            "（任意）ファイルをナンバリングする\n`n-`ファイル名：先頭に追加する場合は「y」と入力\nファイル名`-n`：末尾に追加する場合は「n」と入力\n不要の場合は何も入力せず enterキーを押下："
        )

        if mode == "all":
            replace_all_str = input("入力した文字列で全置換：")
            _rename_file_act(rename_files, numbering, replace_all_str)

        elif mode == "part":
            replace_str = input("置換結果となる文字列：")
            target_str = input("置換したいファイル名の文字列：")
            _rename_file_act(rename_files, numbering, replace_str, target_str)

        elif mode == "add_begin":
            add_begin_str = input("ファイル名の先頭に追加したい文字列：")
            _rename_file_act_mode_add(rename_files, numbering, add_begin_str)

        elif mode == "add_end":
            add_end_str = input("ファイル名の末尾に追加したい文字列：")
            _rename_file_act_mode_add(
                rename_files, numbering, add_end_str, is_begin=False
            )

    except Exception as e:
        print(f"リネーム処理のコア機能部分`rename_files_sys`での処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_files_sys()
