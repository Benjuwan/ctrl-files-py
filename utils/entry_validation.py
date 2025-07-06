import sys


# 適正コマンド（y/n）かどうかを確認するメソッド
def input_validation(input_entry: str | None = None) -> str | None:
    entry_result = input_entry if input_entry == "y" or input_entry == "n" else None

    if entry_result is None:
        sys.exit(f"入力された「{input_entry}」は無効です。y または n で入力ください")

    return entry_result


# 必要項目が入力されているか確認するメソッド
def check_entry_count(title: str = "", entry: str | None = None) -> None:
    if entry is not None and len(entry) == 0:
        sys.exit(f"{title} | 入力文字数が「{len(entry)}」なので処理できませんでした")


if __name__ == "__main__":
    input_validation()
    check_entry_count()
