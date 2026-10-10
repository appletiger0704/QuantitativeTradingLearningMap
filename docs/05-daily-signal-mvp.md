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
`run_id, business_key, revision_key, input_fingerprint, strategy_id, strategy_version, config_hash, symbol, as_of_trade_date, generated_at, action, reason_code, target_weight, reference_close, execution_earliest, risk_checks`。

訊號 `action` 統一列舉：**BUY / SELL / HOLD / NO_DATA / BLOCKED**。
- **HOLD**：通過資料與風控檢查，維持目前目標部位。
- **NO_DATA**：資料缺漏、過期、尚未完整發布或資料品質檢查失敗；不得推導交易意圖。
- **BLOCKED**：資料有效且可算出意圖，但因持倉上限、人工停止、交易限制或其他風控規則禁止執行。
- **BUY / SELL**：有效訊號且通過風控；仍非已成交訂單。

每筆輸出保留 `reason_code` 和可讀原因；優先判定資料有效性，再判定交易風控。沒有既有持倉輸入時，須區分「目標部位」與「相對目前持倉需要的實際委託」，不得直接把目標權重當成已可下單指令。

## 可靠性與安全
- Idempotency 分兩層：`business_key = hash(strategy_id, strategy_version, as_of_trade_date, symbol, config_hash)` 對應同一研究問題；`revision_key = hash(business_key, input_fingerprint)` 識別當次輸入版本。`input_fingerprint` 至少包括市場資料快照、持倉快照與風控設定版本。相同 revision 重試不重複產出；遲到／修正資料改變 fingerprint 時新增 **immutable revision**，保留原先 NO_DATA／BLOCKED／交易訊號結果，不得覆寫。`run_id` 另記錄每一次執行嘗試，最新結果需註明修訂次序。
- Data cut-off：收盤數據是否已正式發布需檢查；遲到、停市與假日自動跳過或告警。
- Fail closed：缺資料、重複資料、異常價格或未準時發布 → **NO_DATA**；資料有效但交易風控禁止 → **BLOCKED**；兩者皆不可產生 BUY / SELL。
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