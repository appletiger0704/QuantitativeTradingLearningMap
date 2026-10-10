# 05 — 每日交易訊號系統 MVP（人工下單）

## 範圍
- 僅日線、每日批次、台股研究用途。
- 產生買賣／觀望建議及可核對報告；**不直接連接券商下單 API**。
- 正式資料取得與訊號生成必須獨立於 Notebook，且可在排程環境重跑。

## 模組與資料流
```text
Scheduler（台北時間、交易日曆）
  → Provider Adapter（官方／付費／FinLab 可替換）
  → Raw Snapshot + Metadata（保留來源與取得時間）
  → Validation（缺漏／重複／價格異常／日期）
  → Feature Engine（MA／Momentum）
  → Strategy（策略版本與設定）
  → Portfolio + Risk Rules（部位、曝險、禁買）
  → Signal Store（冪等鍵）
  → Human-Readable Report（明確標註僅供人工確認）
  → 人工查核 → 人工下單 → 執行結果回填（選做）
```

## 日訊號輸出建議欄位
`run_id, strategy_id, strategy_version, config_hash, symbol, as_of_trade_date, generated_at, action, target_weight, reference_close, execution_earliest, reason, risk_checks, data_status`。

重要：**HOLD** 表示保持現有配置；**NO_DATA / BLOCKED** 表示資料或風控不合格，不能以 HOLD 偷渡。沒有既有持倉輸入時，區分「目標持倉」與「相對目前持倉需要的實際訂單」。

## 可靠性與安全
- Idempotency：`strategy_id + strategy_version + as_of_trade_date + symbol + config_hash`；重跑不重複產生行動建議。
- Data cut-off：收盤數據是否已正式發布需檢查；遲到、停市與假日自動跳過或告警。
- Fail closed：缺資料、重複資料、異常價格、風控失敗時標示 BLOCKED。
- 可追溯：輸入快照／校驗碼、版本、參數、交易日、產生時間、結果都保存。
- 秘密資訊放環境變數或秘密管理器；不提交 token、帳戶及個人持倉到 Git。
- 定期驗證官方交易日曆、資料使用條款與交易成本假設，不把示範值視為現行法規。

## 推薦最小模組介面
```python
def load_bars(provider, symbols, start, end): ...
def validate_bars(bars): ...
def calculate_features(bars, params): ...
def generate_target_positions(features, strategy): ...
def apply_risk_limits(target_positions, holdings, rules): ...
def build_signal_report(targets, holdings, context): ...
```

## MVP 交付序列
1. **M0**：一檔 ETF 的歷史行情 → MA 訊號 → CSV 報表。
2. **M1**：正確 T+1 回測 + 成本 + benchmark，含測試。
3. **M2**：多股票／持倉部位與風控 + 策略版本管理。
4. **M3**：交易日排程、缺漏檢核、可追溯資料快照與報告。
5. **M4**：紙上交易及人工確認紀錄、異常告警。

最終驗收：同一批資料重跑相同結果；空資料與停市不會產生錯誤交易訊號；報告可回答「為什麼、用哪天數據、下個何時可交易、風險是什麼」。