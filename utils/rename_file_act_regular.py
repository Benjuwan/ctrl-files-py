import glob
import shutil
import os


# 同一拡張子のファイルが無いかチェックするプライベートメソッド
def _check_duplicated_extends(filelist: list[str]) -> bool:
    extends = []
    duplicated_extends_count = 0

    for file in filelist:
        # os.path.splitext で確実に拡張子を取得する
        extend = os.path.splitext(file)[1]
        extends.append(extend)

        for ext in extends:
            if file.count(ext):
                duplicated_extends_count += 1

    if duplicated_extends_count > 0:
        return True

    return False


# モード：all, part ルート時におけるリネーム処理
def rename_file_act_regular(
    target_file_dir: list[str] | None = None,
    numbering: str = "",
    replace_str: str = "",
    target_str: str | None = None,
) -> None:
    if target_file_dir is None:
        return

    # 処理対象ディレクトリ内の全てのファイルリスト（以下の内包表記からうまれるイテラブル）
    rename_files = [
        f  # 式：ループ変数fをそのまま取得
        for f  # ループ変数：glob結果の各要素（target_file_dirフォルダ内の全データ）を順次取得
        # アンパック（*イテラブル）： JavaScriptのスプレッド構文（...）と同じようにリストやタプルの中身を展開して渡す仕組み
        in glob.glob(os.path.join(*target_file_dir, "*"))
        # isfile：対象がファイルかどうかを判定（ディレクトリを除外してファイルのみを抽出）
        if os.path.isfile(f)
    ]

    if len(rename_files) == 0:
        print(f"{target_file_dir}内のファイルは現在「{len(rename_files)}」件です")
        return

    is_add_numbering = len(numbering) > 0 and (
        numbering.count("y") or numbering.count("n")
    )

    try:
        # part：ナンバリング有りver
        if is_add_numbering and target_str is not None:
            for i, file in enumerate(rename_files, 1):
                # 置換対象文字を含んでいない場合はスキップ
                if file.count(replace_str) == 0:
                    print(f"{i} --- {file}は置換対象外です")
                    continue

                # バックアップを作成（.bak：バックアップファイルを意味する拡張子）
                shutil.copy2(file, file + ".bak")

                # 文字列置換
                target_replace_str = replace_str
                replace_result_str = target_str
                adjust_filename = file.replace(target_replace_str, replace_result_str)

                # ファイル名とディレクトリを分離
                dir_name = os.path.dirname(adjust_filename)
                base_name = os.path.basename(adjust_filename)
                name_without_ext = os.path.splitext(base_name)[0]
                # os.path.splitext で確実に拡張子を取得する
                extend = os.path.splitext(base_name)[1]

                # ファイル名の変更（`dir_name`と組み合わせてフルパス生成）
                new_name = os.path.join(
                    dir_name,
                    f"{i}-{name_without_ext}{extend}"
                    if numbering == "y"
                    else f"{name_without_ext}-{i}{extend}",
                )
                print(file, new_name)
                os.rename(file, new_name)
            return

        # part：ナンバリング無しver
        if target_str is not None:
            for file in rename_files:
                if file.count(replace_str) == 0:
                    continue

                shutil.copy2(file, file + ".bak")
                target_replace_str = replace_str
                replace_result_str = target_str
                adjust_filename = file.replace(target_replace_str, replace_result_str)
                os.rename(file, adjust_filename)
            return

        # all：ナンバリング有りver
        if is_add_numbering:
            for i, file in enumerate(rename_files, 1):
                shutil.copy2(file, file + ".bak")

                dir_name = os.path.dirname(file)
                extend = os.path.splitext(file)[1]

                new_name = os.path.join(
                    dir_name,
                    f"{i}-{replace_str}{extend}"
                    if numbering == "y"
                    else f"{replace_str}-{i}{extend}",
                )
                print(file, new_name)
                os.rename(file, new_name)
            return

        # all：ナンバリング無しver
        else:
            for file in rename_files:
                # 同一拡張子のファイルが無いかチェック
                is_check_duplicated_extends = _check_duplicated_extends(rename_files)
                if is_check_duplicated_extends:
                    print("同じ拡張子のファイルがあります。重複ファイルは作成不可")
                    return

                shutil.copy2(file, file + ".bak")

                dir_name = os.path.dirname(file)
                extend = os.path.splitext(file)[1]

                new_name = os.path.join(dir_name, f"{replace_str}{extend}")
                os.rename(file, new_name)
            return

    except Exception as e:
        print(f"ファイル名の置換処理実行エラー | {e}")
        return


if __name__ == "__main__":
    rename_file_act_regular()
