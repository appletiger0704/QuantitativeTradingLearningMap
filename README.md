# Quantitative Trading Learning Map（台股量化交易學習地圖）

目標：**從零建立可驗證、可追蹤、每日執行一次的台股量化研究系統**。每日產生買入／賣出／觀望訊號，**人工確認、人工下單**。以 Python 自行開發，FinLab 僅作可替換資料／研究工具，**不依賴任何特定供應商**。

> 教學研究用途，非投資建議；歷史回測不代表未來表現。

## 開始學習
1. [完整學習路線與階段驗收](docs/00-roadmap.md)
2. [核心基礎：價格、報酬與風險](docs/01-foundations.md)
3. [台股資料工程與防止資料洩漏](docs/02-data-engineering.md)
4. [回測、交易成本與驗證](docs/03-backtesting-validation.md)
5. [策略教材與統一規格](docs/04-strategies.md)
6. [每日訊號系統 MVP 架構](docs/05-daily-signal-mvp.md)
7. [練習任務、驗收與研究紀錄](docs/06-exercises-checklist.md)
8. [Lab 1：可執行的 SMA 日線回測](docs/07-first-running-lab.md)
9. [12 週引導式學習計畫](docs/08-guided-study-plan.md)
10. [台灣市場實際研究檢核表](docs/09-taiwan-market-research-checklist.md)

## 快速開始：執行練習

需要 Python 3.10+；此入門練習只使用標準函式庫。範例為**虛構行情**，並非可下單策略。

```bash
python examples/lesson01_ma_backtest.py
python -m unittest discover -s examples -p "test_*.py" -v
```


## 建議學習方式
每一章遵循 **概念 → 市場假設 → 明確規則 → 資料 → Python → 回測 → 偏誤檢查 → 結論**。每個階段要交付可重跑的實驗；不能只憑報酬率判定成功。先完成日線研究與紙上交易，再使用真實資金。

## 推薦專案結構（逐步建立）
```text
docs/                   # Markdown 教材
examples/               # 合成行情 Lab、測試與資料
notebooks/              # 探索性研究，不放正式排程邏輯
src/quant_trading/          # 下一階段待建立
  data/                 # Provider 介面與台股資料正規化
  indicators/           # 指標
  strategies/           # 交易訊號（純函式）
  portfolio/            # 部位／資金管理
  backtest/             # 撮合、成本、績效
  validation/           # 資料與策略驗證
  reporting/            # 每日研究報告
  pipeline/             # 排程與執行
tests/                  # 單元與整合測試
config/                 # 策略參數、Universe 與設定
artifacts/              # 本機輸出，視敏感度決定是否進版控
```

原始需求：[Issue #1](https://github.com/appletiger0704/QuantitativeTradingLearningMap/issues/1)。**路線圖與教材**在此 repo；未來可把實際程式建在獨立的 QuantitativeTrading repo。