import glob
import os
import shutil


def move_dirs(dirname: str = "rename") -> None:
    # `../file/{dirname}`というパス文字列として正しく認識してもらうために os.path.join で文字列結合する
    file_dir = os.path.join("..", "file", dirname)

    target_files = glob.glob(file_dir, recursive=True)
    if len(target_files) == 0:
        print(f"`move_dirs` | 処理対象フォルダ「{dirname}」が存在しません")

        # ルートに file_dir フォルダが存在しない場合のみ作成
        if os.path.exists(f"{file_dir}") is False:
            # 再帰的にディレクトリを作成（※指定したフォルダ構成通りに作成してくれる）
            os.makedirs(f"{file_dir}")

        return
    
    """
    TODO
    ディレクトリ新規作成後に処理終了するので後続処理がうまくいかない（事項されない）
    main.py でディレクトリ作成処理を行う？
    """

    try:
        for target_file in target_files:
            # 完全なファイルコピー
            shutil.copy2(file_dir, target_file)

        # for target_file in target_files:
        #     # ファイルの移動
        #     shutil.move(file_dir, target_file)

    except Exception as e:
        print(f"フォルダ移動の処理実行エラー | {e}")
        return


if __name__ == "__main__":
    move_dirs()
