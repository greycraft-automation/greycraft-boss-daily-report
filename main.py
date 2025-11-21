# Greycraft 老闆每日營收 LINE 報表 - MVP v0.1
# 目標：讀一個 CSV，把「今日營收總額」算出來，並產生一段給老闆看的文字訊息

import csv
from datetime import date


def read_today_total(csv_path: str):
    """讀取銷售資料，計算「今天」的總營收與筆數"""
    today_str = date.today().isoformat()  # 例如：2025-11-21
    total_amount = 0
    count = 0

    with open(csv_path, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 假設欄位名稱是 date, amount
            if row["date"] == today_str:
                # 這裡先假設 amount 是整數字串
                total_amount += int(row["amount"])
                count += 1

    return today_str, total_amount, count


def format_message(report_date: str, total_amount: int, count: int) -> str:
    """把數字組成一段老闆看得懂的中文訊息"""
    if count == 0:
        return f"{report_date} 營收快報：今日尚無交易紀錄。"

    return f"{report_date} 營收快報：今日 {total_amount:,} 元，共 {count} 筆交易。"



if __name__ == "__main__":
    print("Greycraft 老闆每日營收 LINE 報表 - 開發中")

    # 先用一個暫時的檔名，等一下你會建立這個檔案
    csv_path = "sales_sample.csv"

    report_date, total_amount, count = read_today_total(csv_path)
    message = format_message(report_date, total_amount, count)

    print("=== 測試輸出 ===")
    print(message)
