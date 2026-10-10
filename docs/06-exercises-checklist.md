# 06 — 實作練習、驗收與研究紀錄

## 由簡到難的練習
先從 [第一個可執行 Lab](07-first-running-lab.md) 開始，檢查環境、訊號時間、成交時間與成本；再依下列任務完成升級。
- [ ] E01 建立 Python 專案與 pytest，載入 CSV 日行情並檢查日期、型別、前導零。
- [ ] E02 計算簡單報酬、累積報酬、CAGR、波動度、Sharpe、MDD，手算小樣本核對。
- [ ] E03 計算 MA20／MA50／MA200、120D Momentum，測試資料不足的 warm-up。
- [ ] E04 注入重複日期、缺值、停牌與異常 OHLC，驗證 fail-closed。
- [ ] E05 做單一 ETF 趨勢策略，收盤計算、次交易日成交。
- [ ] E06 加入現金與持倉帳，測試股利、手續費、交易稅、滑價與最小交易單位。
- [ ] E07 比較策略與適當的含息 Benchmark；輸出 equity curve 與 metrics。
- [ ] E08 建立 Momentum 排名與月度再平衡，完整揭露歷史 Universe 侷限。
- [ ] E09 固定樣本外資料段並做 walk-forward、成本敏感度與參數穩健性測試。
- [ ] E10 完成每日訊號 JSON/CSV、資料快照、冪等執行及失敗報告。
- [ ] E11 執行紙上交易並記錄「訊號 vs 實際可交易價格」偏差。
- [ ] E12 撰寫完整策略研究報告；評估保留／淘汰理由。

## 每項練習的 Definition of Done
1. 提供可重現命令、依賴環境與輸入來源。
2. 有至少一個成功案例與一個反例的測試。
3. 說明資料可得時點與成交假設。
4. 說明風險與限制、不可用數據的處置。
5. 產出可追溯的圖／表／執行紀錄。

## 策略實驗紀錄模板
```markdown
# Experiment ID / Date
- Hypothesis:
- Strategy commit / version:
- Data provider / snapshot / as-of:
- Universe and benchmark:
- Parameters (pre-registered):
- Cost / fill model:
- In-sample range:
- Out-of-sample range:
- CAGR / Sharpe / MDD / turnover / trade count:
- Benchmark difference:
- Sensitivity / stress tests:
- Known biases and caveats:
- Decision: KEEP / REJECT / INVESTIGATE
- Next experiment:
```

## 學習完成的核心能力
**不只是產生 BUY / SELL**，還要能回答訊號是否使用了當時可取得資料、是否能成交、成本後是否勝過基準、是否只是過度擬合，以及系統出錯時是否會阻止錯誤建議。

## 未來延伸
在基礎成熟後可研究多因子、橫截面風險、資產配置、統計套利、ML；自動下單列為不同的風險與權限專案，不屬於此 MVP。
