# 04 — 策略教材與研究模板

## Strategy Specification（每個策略必填）
```markdown
# Strategy Name
## Hypothesis：為何可能有效、何時可能失效
## Universe：交易標的、進出股票池規則
## Required Data：欄位、調整方式、發布時間
## Indicator / Signal：精確計算及觀測時點
## Entry / Exit：買入與賣出觸發條件
## Rebalance：訊號頻率與可執行時段
## Position Sizing：資金、最大曝險、整／零股
## Execution / Cost：成交假設、手續費、稅、滑價
## Risk Control：停損、集中度與資料缺失處置
## Benchmark：含息或不含息、選用理由
## Metrics：CAGR、MDD、Sharpe、Turnover、交易次數
## Bias Check：前視、存活者、過擬合與資料修訂
## Experiments：樣本內／外及 walk-forward 實驗連結
## Decision：保留、淘汰或待觀察（附證據）
```

## A. Trend Following（適合第一個每日訊號原型）
- 假設：較長期方向有延續性；盤整市可能頻繁假突破。
- 範例規則：收盤價在 MA200 之上且 MA50 > MA200，允許持有；跌破任一預先定義門檻則調整或退出。
- **注意**：必須事先固定「首次建立部位」、「再次進場」、「初始無部位」、「變動訊號」的定義，不能把條件為真每天當作新 BUY。
- 練習：比較 MA 參數附近範圍，記錄換手及成本後結果。

## B. Momentum（完整研究案例）
- 假設：過去中期相對強勢股票可能延續，但反轉風險高。
- Universe：歷史可交易且具流動性之台股；需明訂停牌／下市處理。
- Signal：以截至 T 的 120 個交易日報酬排序，Top 10、等權重，每月調整。
- Execution：T 收盤生成名單，下一個可交易時段依規則成交。
- 比較：20／60／120／252 日視窗；比較 0050 含息版本，非只報最優參數。

## C. Mean Reversion
- 假設：短期偏離可能回復；單邊下跌時可能持續失效。
- 範例：`close / MA20 - 1 < -0.08` 候選進場；價格回到 MA20 或持有超過預設 N 日退出。
- 練習：加入市場環境過濾與尾端風險，檢查停止交易與缺量情境。

## D. Factor Investing
- Value：PE、PB；Quality：ROE、獲利率；Growth：營收及 EPS 成長；Momentum：6／12 個月報酬；Risk：波動率。
- 流程：Point-in-time 財報 → 缺值與極端值處理 → 標準化 → 分數 → 排名 → 資金配置 → 成本回測。
- 注意：負 EPS、產業間差異、發佈日延遲及財報修訂，需明確規範。

## 初學者研究順序
**單資產 MA 策略 → 多資產 Momentum → Mean Reversion → 多因子**。先掌握透明規則，再比較複雜模型。
