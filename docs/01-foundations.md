# 01 — 市場、報酬與風險基礎

## 必懂區別
- **Strategy**：交易假設與完整規則。
- **Indicator**：以過去資料計算的特徵（例如 MA）。
- **Signal**：某一時點的 BUY / SELL / HOLD 意圖。
- **Order / Fill**：委託與實際成交，可能與訊號不同。
- **Position**：目前持有數量；**Portfolio**：全部資產與現金。

## 市場資料
OHLCV = Open、High、Low、Close、Volume。必須明確標示成交量單位、交易日與時區 `Asia/Taipei`；不可混用未調整、前／後復權價格。台股還需研究除權息、停止交易、漲跌幅、零股／整股、流動性，以及 ETF 的標的與配息特性。

## 基本公式
- 單期簡單報酬：`r_t = P_t / P_(t-1) - 1`（若有配息，需正確納入總報酬）。
- 對數報酬：`ln(P_t / P_(t-1))`；不可直接以對數報酬表示帳戶損益。
- CAGR：`(V_end/V_start)^(1/years) - 1`，年數應依實際期間。
- 年化波動率（常見日資料近似）：`std(daily_returns) * sqrt(252)`；應註明年化慣例與樣本。
- Sharpe（概念）：`mean(excess_daily_returns)/std(excess_daily_returns)*sqrt(252)`；無風險利率頻率須一致。
- Max Drawdown：`min(V_t/running_max(V_t)-1)`；數值越負，回撤越大。

## 評估不能只看 CAGR
同時看 MDD、波動率、Sharpe、年勝率、交易次數、換手率、平均獲利／虧損、最大單筆損失、曝險比例與相對 Benchmark 的績效；沒有充分交易次數或時間跨度時不要過度解讀統計值。

## 自我測驗
1. 為什麼 +10% 再 -10% 不等於零報酬？
2. 若收盤後才算完訊號，可以用當日收盤價成交嗎？
3. 高 CAGR、深 MDD 與低換手的策略，各自可能有哪些代價？
4. 為何個股的價格報酬不一定等於含息總報酬？
