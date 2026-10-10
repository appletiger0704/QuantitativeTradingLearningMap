# 02 — 台股資料工程與資料時間正確性

## 資料需求
| 資料集 | 基本欄位 | 用途 |
|---|---|---|
| 日行情 | symbol、trade_date、OHLCV、來源 | 指標與策略 |
| 公司行動 | event_date、現金股利／拆併股／調整因子 | 總報酬與價格一致性 |
| 證券主檔 | symbol、上市／下市日、交易狀態、類別 | 歷史 Universe |
| 基本面（進階） | fiscal_period、published_at、value | 因子研究 |
| 基準 | trade_date、價格／含息總報酬 | 比較基準 |
| 執行紀錄 | as_of、observed_at、source、版本／hash | 可追溯性 |

可先評估 TWSE、TPEx、MOPS 等官方資料；亦可透過有授權的供應商。實際可用 API、授權、下載限制、更新頻率與資料涵蓋度需在接入時驗證。FinLab 只實作為其中一個 adapter，不能讓策略直接依賴 FinLab 的專屬欄位。

## 建議抽象介面
```python
from typing import Protocol
import pandas as pd

class MarketDataProvider(Protocol):
    def get_daily_bars(self, symbols: list[str], start: str, end: str) -> pd.DataFrame: ...
```
統一輸出 schema 後再讓策略使用；Provider 的套件、憑證、限流與重試放在資料層處理。

## 避免未來函數
- 區分 `trade_date`、`published_at`（外部何時正式發布）與 `ingested_at`（本系統何時收到）。
- 決策時只能使用 **當時已公開且可取得** 的資訊；晚發布財報不可回填到更早決策日。
- 股票池要以當時的上市、下市與停牌狀態重建；只用今天還存在的股票會造成 **survivorship bias**。
- 所有移動均線／動能特徵只能依當時及之前資料產生；同日收盤生成的訊號，最早只能假設次一可執行交易時段成交。
- 除權息處理須分清訊號用價格、成交用原始行情、績效用含息資產變動，避免重複計入股利。
- 若採用最新修訂後的歷史資料，需要標示 point-in-time 限制，不可宣稱已消除前視偏誤。

## 最低品質門檻
(symbol, trade_date) 不重複；OHLC 邏輯一致；交易量與價格範圍合理；缺失交易日、停牌與無資料要明確區分；股票代號不丟前導零；日期、時區與單位一致。保留原始快照及校驗碼，來源失敗不可靜默沿用舊資料。

## 最小測試
- 人工注入重複列，檢查是否拒絕。
- 移除某股票一日行情，確認系統標記缺漏而非補出假價格。
- 將財報發布日改到決策日之後，確認因子不使用該值。
- 使用下市標的測試歷史 Universe 的涵蓋。
