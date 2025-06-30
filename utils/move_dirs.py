import os
import glob
import sys
import shutil


def check_and_create_move_dir(dirname: str = "rename") -> None:
    try:
        # `../file/{dirname}`というパス文字列として正しく認識してもらうために os.path.join で文字列結合する
        file_dir = os.path.join("..", "file", dirname)

        target_files = glob.glob(file_dir, recursive=True)
        if len(target_files) == 0:
            print(
                f"`check_and_create_move_dir` | 処理対象フォルダ「{dirname}」が存在しません"
            )

            # ルートに file_dir フォルダが存在しない場合のみ作成
            if os.path.exists(f"{file_dir}") is False:
                # 再帰的にディレクトリを作成（※指定したフォルダ構成通りに作成してくれる）
                os.makedirs(f"{file_dir}")

            # sys.exit で全体の処理中断
            sys.exit(f"「{dirname}」を作成したので再実行してください")

    except Exception as e:
        print(f"移動先フォルダのチェック及び作成処理における実行エラー | {e}")
        return


def move_dir(
    target_file_dir: list[str] | None = None, replace_result_str: str | None = None
):
    if target_file_dir is None:
        return

    try:
        # 移動先フォルダパス（rename以外の各フォルダリスト）
        move_target_dir = list(
            filter(lambda dir: dir.count("rename") == 0, target_file_dir)
        )

        # Notice： （React でいう props バケツリレー的な感じで）main.py からここまで entry_move_dir を渡してくればフィルター処理で入力フォルダを処理対象にできるが、保守性と可読性が低下するので以下のエラーハンドリングで対処
        if len(move_target_dir) > 2:
            print(f"""
fileフォルダ内に現在、処理対象候補フォルダが「 {len(move_target_dir)}つ」あります
fileフォルダ内は、2つ（rename + 任意のフォルダ）までにしてください
今回は先頭フォルダ「{move_target_dir[0]}」に対象ファイルをコピーします
""")

        # 移動元フォルダパス（file/rename）を抽出
        target_rename_dir = list(
            filter(lambda dir: dir.count("rename"), target_file_dir)
        )

        # 移動元フォルダパス（file/rename）から各ファイルデータパス（イテラブル）を取得
        src_file = glob.glob(os.path.join(*target_rename_dir, "*"))

        for file in src_file:
            # ※部分置換処理の場合のみ
            # 置換対象文字が存在して、それを含んでいない場合はスキップ
            if replace_result_str is not None and file.count(replace_result_str) == 0:
                continue

            # ファイルの移動（メタデータを含む完全コピー）
            shutil.copy2(file, move_target_dir[0])

    except Exception as e:
        print(f"フォルダ移動の処理実行エラー | {e}")
        return


if __name__ == "__main__":
    check_and_create_move_dir()
    move_dir()
