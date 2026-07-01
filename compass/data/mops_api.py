"""
MOPS API 串接（使用 FinMind 作為資料來源）

資料來源：FinMind API
- 財務報表（損益表）
- 資產負債表
- 現金流量表

FinMind 提供結構化的財務數據，比直接爬取 MOPS 更穩定。
"""

from dataclasses import dataclass
from datetime import date
from typing import Optional
import pandas as pd
from FinMind.data import DataLoader


@dataclass
class FinancialData:
    """財務資料"""
    stock_id: str
    year: int
    quarter: int
    roe: float  # 股東權益報酬率 (%)
    eps: float  # 每股盈餘
    net_worth_per_share: float  # 每股淨值
    gross_margin: float  # 毛利率 (%)
    operating_margin: float  # 營業利益率 (%)
    debt_ratio: float  # 負債比 (%)
    free_cash_flow: float  # 自由現金流 (億元)


@dataclass
class BalanceSheetData:
    """資產負債表資料"""
    stock_id: str
    date: date
    total_assets: float  # 總資產 (千元)
    total_liabilities: float  # 總負債 (千元)
    total_equity: float  # 總權益 (千元)
    cash_and_equivalents: float  # 現金及約當現金 (千元)


@dataclass
class CashFlowData:
    """現金流量表資料"""
    stock_id: str
    date: date
    operating_cash_flow: float  # 營業活動現金流量 (千元)
    investing_cash_flow: float  # 投資活動現金流量 (千元)
    financing_cash_flow: float  # 籌資活動現金流量 (千元)
    free_cash_flow: float  # 自由現金流 (千元)


class MOPSAPI:
    """MOPS API 客戶端（使用 FinMind）"""

    # FinMind 欄位名稱對應表
    FINANCIAL_FIELD_MAP = {
        "營業收入": ["營業收入"],
        "營業成本": ["營業成本"],
        "營業毛利": ["營業毛利", "營業毛損"],
        "營業費用": ["營業費用"],
        "營業利益": ["營業利益", "營業損失"],
        "本期淨利": ["本期淨利", "本期淨損"],
        "基本EPS": ["基本每股盈餘", "基本每股虧損"],
    }

    BALANCE_FIELD_MAP = {
        "總資產": ["資產總計"],
        "總負債": ["負債總計"],
        "權益總額": ["權益總額", "歸屬於母公司業主之權益合計", "權益總計"],
        "現金": ["現金及約當現金"],
    }

    CASHFLOW_FIELD_MAP = {
        "營業CF": ["營業活動之淨現金流入", "營業活動之淨現金流出"],
        "投資CF": ["投資活動之淨現金流入", "投資活動之淨現金流出"],
        "籌資CF": ["籌資活動之淨現金流入", "籌資活動之淨現金流出"],
    }

    def __init__(self):
        self.dl = DataLoader()

    def get_financial_data(
        self,
        stock_id: str,
        year: Optional[int] = None,
        quarter: Optional[int] = None,
    ) -> list[FinancialData]:
        """
        取得財務資料

        Args:
            stock_id: 股票代號
            year: 年度
            quarter: 季度

        Returns:
            list of FinancialData
        """
        if year is None:
            year = date.today().year - 1
        if quarter is None:
            quarter = 4

        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"

        try:
            # 取得損益表
            income_df = self.dl.taiwan_stock_financial_statement(
                stock_id=stock_id,
                start_date=start_date,
                end_date=end_date,
            )

            # 取得資產負債表
            balance_df = self.dl.taiwan_stock_balance_sheet(
                stock_id=stock_id,
                start_date=start_date,
                end_date=end_date,
            )

            # 取得現金流量表
            cashflow_df = self.dl.taiwan_stock_cash_flows_statement(
                stock_id=stock_id,
                start_date=start_date,
                end_date=end_date,
            )

            # 解析資料
            results = []
            for q in range(1, 5):
                q_date = f"{year}-{q*3:02d}-{15 if q == 1 else 28 if q == 2 else 30}"

                # 提取關鍵指標
                revenue = self._extract_value(income_df, q_date, "營業收入")
                gross_profit = self._extract_value(income_df, q_date, "營業毛利")
                operating_income = self._extract_value(income_df, q_date, "營業利益")
                net_income = self._extract_value(income_df, q_date, "本期淨利")
                eps = self._extract_value(income_df, q_date, "基本EPS")

                # 計算毛利率和營業利益率
                gross_margin = (gross_profit / revenue * 100) if revenue > 0 else 0
                operating_margin = (operating_income / revenue * 100) if revenue > 0 else 0

                # ROE 需要權益數據，從資產負債表取得
                # 注意：資產負債表可能只有 Q3 和 Q4 的數據
                total_equity = self._extract_value(balance_df, q_date, "權益總額", field_map="balance")
                if total_equity > 0:
                    roe = (net_income / total_equity * 100 * 4)  # 年化
                else:
                    roe = 0.0

                # 從資產負債表計算負債比
                total_assets = self._extract_value(balance_df, q_date, "總資產", field_map="balance")
                total_liabilities = self._extract_value(balance_df, q_date, "總負債", field_map="balance")
                debt_ratio = (total_liabilities / total_assets * 100) if total_assets > 0 else 0.0

                # 從現金流量表計算自由現金流
                operating_cf = self._extract_value(cashflow_df, q_date, "營業CF", field_map="cashflow")
                investing_cf = self._extract_value(cashflow_df, q_date, "投資CF", field_map="cashflow")
                # 注意：FinMind 的現金流量數據單位是元，轉換為億元需除以 1e8
                free_cash_flow = (operating_cf + investing_cf) / 1e8  # 元轉億元

                results.append(
                    FinancialData(
                        stock_id=stock_id,
                        year=year,
                        quarter=q,
                        roe=roe,
                        eps=eps,
                        net_worth_per_share=0,  # 需要額外計算
                        gross_margin=gross_margin,
                        operating_margin=operating_margin,
                        debt_ratio=debt_ratio,
                        free_cash_flow=free_cash_flow,
                    )
                )

            return results

        except Exception as e:
            print(f"Error fetching financial data for {stock_id}: {e}")
            return []

    def get_balance_sheet(
        self,
        stock_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[BalanceSheetData]:
        """
        取得資產負債表

        Args:
            stock_id: 股票代號
            start_date: 開始日期
            end_date: 結束日期

        Returns:
            list of BalanceSheetData
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = date(end_date.year - 1, 1, 1)

        try:
            df = self.dl.taiwan_stock_balance_sheet(
                stock_id=stock_id,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )

            results = []
            # 按日期分組
            for dt, group in df.groupby("date"):
                total_assets = self._extract_value_from_group(group, "總資產")
                total_liabilities = self._extract_value_from_group(group, "總負債")
                total_equity = self._extract_value_from_group(group, "權益總額")
                cash = self._extract_value_from_group(group, "現金及約當現金")

                results.append(
                    BalanceSheetData(
                        stock_id=stock_id,
                        date=dt if isinstance(dt, date) else pd.to_datetime(dt).date(),
                        total_assets=total_assets,
                        total_liabilities=total_liabilities,
                        total_equity=total_equity,
                        cash_and_equivalents=cash,
                    )
                )

            return results

        except Exception as e:
            print(f"Error fetching balance sheet for {stock_id}: {e}")
            return []

    def get_cash_flow(
        self,
        stock_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[CashFlowData]:
        """
        取得現金流量表

        Args:
            stock_id: 股票代號
            start_date: 開始日期
            end_date: 結束日期

        Returns:
            list of CashFlowData
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = date(end_date.year - 1, 1, 1)

        try:
            df = self.dl.taiwan_stock_cash_flows_statement(
                stock_id=stock_id,
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
            )

            results = []
            # 按日期分組
            for dt, group in df.groupby("date"):
                operating_cf = self._extract_value_from_group(
                    group, "營業活動之淨現金流入（流出）"
                )
                investing_cf = self._extract_value_from_group(
                    group, "投資活動之淨現金流入（流出）"
                )
                financing_cf = self._extract_value_from_group(
                    group, "籌資活動之淨現金流入（流出）"
                )
                free_cf = operating_cf + investing_cf

                results.append(
                    CashFlowData(
                        stock_id=stock_id,
                        date=dt if isinstance(dt, date) else pd.to_datetime(dt).date(),
                        operating_cash_flow=operating_cf,
                        investing_cash_flow=investing_cf,
                        financing_cash_flow=financing_cf,
                        free_cash_flow=free_cf,
                    )
                )

            return results

        except Exception as e:
            print(f"Error fetching cash flow for {stock_id}: {e}")
            return []

    def _extract_value(self, df: pd.DataFrame, date_str: str, metric_key: str, field_map: str = "financial") -> float:
        """從 DataFrame 中提取特定日期的特定指標值"""
        try:
            # 取得對應的欄位名稱
            if field_map == "balance":
                field_names = self.BALANCE_FIELD_MAP.get(metric_key, [metric_key])
            elif field_map == "cashflow":
                field_names = self.CASHFLOW_FIELD_MAP.get(metric_key, [metric_key])
            else:
                field_names = self.FINANCIAL_FIELD_MAP.get(metric_key, [metric_key])

            # 嘗試匹配日期
            mask = df["date"].astype(str).str.contains(date_str[:7])  # 匹配年月
            filtered = df[mask]

            # 嘗試匹配 origin_name 包含關鍵字
            for _, row in filtered.iterrows():
                origin_name = str(row.get("origin_name", ""))
                for field_name in field_names:
                    if field_name in origin_name:
                        return float(row.get("value", 0))

            return 0.0
        except Exception:
            return 0.0

    def _extract_value_from_group(self, group: pd.DataFrame, metric_key: str) -> float:
        """從分組的 DataFrame 中提取特定指標值"""
        try:
            # 根據 metric_key 選擇對應的欄位映射
            if metric_key in self.BALANCE_FIELD_MAP:
                field_names = self.BALANCE_FIELD_MAP[metric_key]
            elif metric_key in self.CASHFLOW_FIELD_MAP:
                field_names = self.CASHFLOW_FIELD_MAP[metric_key]
            elif metric_key in self.FINANCIAL_FIELD_MAP:
                field_names = self.FINANCIAL_FIELD_MAP[metric_key]
            else:
                field_names = [metric_key]

            for _, row in group.iterrows():
                origin_name = str(row.get("origin_name", ""))
                for field_name in field_names:
                    if field_name in origin_name:
                        return float(row.get("value", 0))
            return 0.0
        except Exception:
            return 0.0
