import glob
import os
import shutil


def move_dirs(dirname: str = "rename", adjusted_files: list[str] | None = None) -> None:
    # `../file/{dirname}`というパス文字列として正しく認識してもらうために os.path.join で文字列結合する
    file_dir = os.path.join("..", "file", dirname)

    target_files_dir = glob.glob(file_dir, recursive=True)
    if len(target_files_dir) == 0:
        print(f"`rename_files` | 処理対象フォルダ「{dirname}」が存在しません")

        # ルートに file_dir フォルダが存在しない場合のみ作成
        if os.path.exists(f"{file_dir}") is False:
            # 再帰的にディレクトリを作成（※指定したフォルダ構成通りに作成してくれる）
            os.makedirs(f"{file_dir}")

        return

    try:
        if adjusted_files is None:
            return

        # アンパック（*）： JavaScriptのスプレッド構文（...）と同じようにリストやタプルの中身を展開して渡す仕組み
        adjusted_files_path = os.path.join(*adjusted_files)

        # 完全なファイルコピー
        shutil.copy2(file_dir, adjusted_files_path)

        # ファイルの移動
        # shutil.move(file_dir, adjusted_files_path)

    except Exception as e:
        print(f"フォルダ移動の処理実行エラー | {e}")
        return


if __name__ == "__main__":
    move_dirs()
