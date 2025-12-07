# Greycraft Boss Daily Report  
老闆每日營收 LINE 報表（MVP）

> 每天自動幫你算好「今天收多少」，  
> 把重點整理成一段文字，固定時間傳給老闆的 LINE 或信箱。

Created by **Greycraft Automation（灰匠自動化）**.

---

## 1️⃣ 專案簡介（Project Overview）

**Greycraft Boss Daily Report** 是一個用 Python 寫的輕量級工具，示範如何：

1. 從 `sales_sample.csv` 讀取每日銷售資料  
2. 計算「今天」的營收總額與成交筆數  
3. 組合成一段「給老闆看的中文營收摘要訊息」

目前狀態：  

- ✅ 已可讀取示範銷售資料  
- ✅ 自動產生「今日營收快報」文字（可 demo 給老闆看）  
- ⏳ 未來將加入：LINE 通知、自動排程（Windows 排程器、cron 等）

---

## 2️⃣ 核心功能（What it does）

現階段工具主要負責：

- 讀取銷售 CSV 檔（例如：POS 匯出、Excel 匯出）  
- 根據「今天日期」過濾出當日交易  
- 計算：
  - 今日營收總額  
  - 今日交易筆數  
- 輸出一段類似下列格式的中文訊息：

> 2025-11-21 今日營收快報  
> 今日共 37 筆，總金額 NT$ 128,500  
> （可再依需求加入：各通路、各櫃檯、各店別摘要）

未來可擴充：

- 各通路 / 各櫃檯 / 各店別拆分統計  
- 異常偵測（某通路特別低、退款特別多時標記）  
- 自動發送至 LINE Notify / LINE Bot / Email 群組

---

## 3️⃣ 技術架構（Tech Stack）

- **Python 3**  
- 標準函式庫（`csv`、`datetime`…）處理：
  - 檔案讀取  
  - 日期判斷  
- 簡易函式封裝：
  - `read_today_total(csv_path)`：讀取今日營收與筆數  
  - `format_message(report_date, total_amount, count)`：產出文字訊息  

> LINE 通知與排程會在後續版本加入，並以獨立模組形式實作。

---

## 4️⃣ 檔案說明（Files）

> 依實際專案結構微調，以下為建議說明方式。

- `main.py`  
  - 專案進入點  
  - 呼叫讀取銷售資料與格式化訊息的主流程  

- `sales_sample.csv`  
  - 範例銷售資料  
  - 示範欄位（例如）：`date`, `item`, `amount`  
  - 用來測試「今日營收快報」輸出  

- `README.md`  
  - 本文件：專案技術說明與商業背景  

- （未來）`line_notifier.py`  
  - 專責發送 LINE 訊息的模組  

- （未來）`scheduler_config/`  
  - 各平台排程設定範例（Windows Task Scheduler、cron 等）

---

## 5️⃣ 如何執行（How to Run）

### 1. 準備環境

建議建立虛擬環境（可選）：

```bash
python -m venv .venv
source .venv/bin/activate  # Windows 則為 .venv\Scripts\activate
```

本專案目前只用到 Python 標準函式庫，不需要額外安裝套件。
（若未來加入 LINE / Email 功能，會再補充相依套件。）

### 2. 準備銷售資料 CSV

請確認你的 CSV 檔至少包含：

- `date`：交易日期（建議格式：`YYYY-MM-DD`）
- `amount`：金額（整數或可轉為整數的字串）

你可以先用提供的 `sales_sample.csv` 練習，
之後再改成自家 POS / 報表匯出的檔案。

### 3. 執行主程式

```bash
python main.py
```

預期行為：

- 讀取 `sales_sample.csv`
- 過濾出「今天日期」的交易
- 在終端機印出一段「今日營收快報」的中文訊息

---

## 6️⃣ 給老闆看的說明（Business Context）

各位老闆您好，我是 **Greycraft Automation（灰匠自動化）的 Jason**。 
我們不是賣 POS 機的，我主要做一件事： 

> **把您每天的營收，自動整理成一份一眼看得懂的「當日收款快報」，  
> 在固定時間送到您的 LINE 或信箱。**

不管您現在用的是 POS、Excel 還是手寫帳，
很多店家每天都在做類似的事情：

- 從機器或平台抄數字
- 打開 Excel 算今天收多少
- 數字對不起來又重算一次

我們做的這套小工具，是利用您「原本就有的帳務資料」，
每天自動幫您整理三件事：
1. 今天總共收多少？
2. 各通路／櫃檯／分店的表現如何？
3. 有沒有哪裡異常（某個通路特別低、退款特別多）？

老闆只要在固定時間打開 LINE 或信箱，就會看到：

- 一句話的營運重點結論
- 一張簡單、看得懂的數字摘要表

> Excel 函數是幫「填報的人」算數字，  
> 這套工具是幫「您」把每天的數字變成一句話的營運結論。  
> 兩個是互補，而不是互相取代。

---

## 7️⃣ 試點專案與收費範例（Pilot Project & Pricing）

我們目前已有真實旅館導入案例，可以用「匿名 Demo」給您看實際畫面。

合作方式通常會先從**一次性的試點專案**開始：

- 依照您實際的帳務方式調整工具
- 上線前與您一起驗證數字是否正確
- 提供簡單使用教學（給會計／櫃檯／行政）
- 上線後約 1 個月追蹤與微調

參考價位：

- 試點專案約 **NT$ 15,000 ～ 20,000**（做完是您自己的工具）
- 後續若不續約、不加功能，也不會再額外收費
- 若要再擴充（例如多分店、多通路、自動寄 LINE 通知），再另外估價

在討論價格之前，我會先問您一個問題：

>**現在旅館／餐廳／店裡，每天營收是怎麼看的？**

只要您願意分享目前做法，我會先幫您判斷：

- 這樣的自動化對您來說划不划算？
- 大概可以省下多少時間、人力或錯誤成本？
- 不適合的，我也會直接說實話，不會硬賣。

---

## 8️⃣ 實際 Demo 畫面（Real-world Demos）

以下為「真實台北旅館」的收支表與 Demo 畫面（日期為示意）：  

2024/12/01 Demo

<img width="3072" height="1728" alt="demo_2024-12-01" src="https://github.com/user-attachments/assets/16098796-77cb-4e1b-bedd-946199a4fe71" />

2024/12/05 Demo

<img width="3800" height="1838" alt="demo_2024-12-05" src="https://github.com/user-attachments/assets/402e6c5d-e600-45fc-88ca-b7c22e5eb59d" />

2024/12/31 Demo

<img width="4030" height="1853" alt="demo_2024-12-31" src="https://github.com/user-attachments/assets/2a3a4ac8-d1f1-4e27-a882-995103ae4f64" />

## 9️⃣ 關於 Greycraft Automation（About）

**Greycraft Automation（灰匠自動化）**

專注：企業流程自動化｜AI 整合｜資料擷取｜報表與 ETL Pipeline

- 負責人：Jason 劉昇劼
- 職稱：Automation Workflow Architect

如果你有一件工作，心裡覺得「每天做很浪費生命」，  
可以把流程跟我說說看，我會先幫你判斷值不值得自動化。  

**Contact｜聯絡方式**

- GitHub：https://github.com/greycraft-automation
- LINE 官方帳號：搜尋「灰匠自動化 Greycraft」或加入 ID：@177yaqsm
- Email：jasonaiflow.dev@gmail.com
