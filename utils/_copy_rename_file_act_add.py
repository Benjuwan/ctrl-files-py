import glob
import shutil
import os

from move_dirs import move_dir


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
        f  # 式：ループ変数fをそのまま取得
        for f  # ループ変数：glob結果の各要素（target_file_dirフォルダ内の全データ）を順次取得
        # アンパック（*イテラブル）： JavaScriptのスプレッド構文（...）と同じようにリストやタプルの中身を展開して渡す仕組み
        in glob.glob(os.path.join(*target_rename_dir, "*"))
        # isfile：対象がファイルかどうかを判定（ディレクトリを除外してファイルのみを抽出）
        if os.path.isfile(f)
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
        print(
            f"\n処理受付可能なコードは「y」または「n」のみです\n入力されたコードは「{numbering}」なので無視されます\n"
        )

    try:
        # ナンバリング有りver
        if is_add_numbering:
            for i, file in enumerate(rename_files, 1):
                shutil.copy2(file, file + ".bak")

                dir_name = os.path.dirname(file)

                # os.path.splitext と os.path.basename で確実にファイル名と拡張子を取得する
                target_filename = os.path.basename(os.path.splitext(file)[0])
                extend = os.path.splitext(file)[1]

                new_name = os.path.join(
                    dir_name,
                    f"{i}-{replace_str}-{target_filename}{extend}"
                    if numbering == "y"
                    else f"{target_filename}-{replace_str}-{i}{extend}",
                )
                print(f"{file} -> {new_name}")
                os.rename(file, new_name)

                # フォルダ移動処理が有効の場合は以下の処理に進む
                if has_multi_dirs_filedir:
                    move_dir(target_file_dir)

            return  # 無用な後続処理を避けるため明示的に処理終了

        # ナンバリング無しver
        for file in rename_files:
            shutil.copy2(file, file + ".bak")

            dir_name = os.path.dirname(file)
            target_filename = os.path.basename(os.path.splitext(file)[0])
            extend = os.path.splitext(file)[1]

            new_name = os.path.join(
                dir_name,
                f"{replace_str}-{target_filename}{extend}"
                if is_begin
                else f"{target_filename}-{replace_str}{extend}",
            )
            print(f"{file} -> {new_name}")
            os.rename(file, new_name)

            # フォルダ移動処理が有効の場合は以下の処理に進む
            if has_multi_dirs_filedir:
                move_dir(target_file_dir)

        return

    except Exception as e:
        print(f"ファイル名の前後に文字列を追加する処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_add()
