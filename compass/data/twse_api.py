"""
TWSE API 串接

資料來源：臺灣證券交易所
- 股價日線
- 公司基本資料
- 產業分類

API 端點：
- STOCK_DAY: 個股日線資料
- MI_INDEX: 全市場行情
"""

import re
from dataclasses import dataclass
from datetime import date, timedelta
from typing import Optional
import requests


@dataclass
class StockPrice:
    """股價資料"""
    stock_id: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int  # 股
    value: float  # 元
    change: float  # 漲跌
    turnover: int  # 成交筆數


@dataclass
class CompanyInfo:
    """公司基本資料"""
    stock_id: str
    name: str
    industry: Optional[str] = None


class TWSEAPI:
    """TWSE API 客戶端"""

    BASE_URL = "https://www.twse.com.tw/exchangeReport"

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        })

    def get_stock_price(
        self,
        stock_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> list[StockPrice]:
        """
        取得個股日線資料

        Args:
            stock_id: 股票代號 (例如: "2330")
            start_date: 開始日期
            end_date: 結束日期

        Returns:
            list of StockPrice
        """
        if end_date is None:
            end_date = date.today()
        if start_date is None:
            start_date = end_date - timedelta(days=365)

        url = f"{self.BASE_URL}/STOCK_DAY"
        params = {
            "response": "json",
            "stockNo": stock_id,
            "date": start_date.strftime("%Y%m%d"),
        }

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            if data.get("stat") != "OK":
                return []

            prices = []
            for item in data.get("data", []):
                item_date = self._parse_roc_date(item[0])
                if item_date and start_date <= item_date <= end_date:
                    prices.append(
                        StockPrice(
                            stock_id=stock_id,
                            date=item_date,
                            open=self._parse_float(item[3]),
                            high=self._parse_float(item[4]),
                            low=self._parse_float(item[5]),
                            close=self._parse_float(item[6]),
                            volume=self._parse_int(item[1]),
                            value=self._parse_float(item[2]),
                            change=self._parse_float(item[7]),
                            turnover=self._parse_int(item[8]),
                        )
                    )

            return prices

        except Exception as e:
            print(f"Error fetching stock price for {stock_id}: {e}")
            return []

    def get_company_info(self, stock_id: str) -> Optional[CompanyInfo]:
        """
        取得公司基本資料

        從 STOCK_DAY 的 title 欄位解析公司名稱
        Title 格式: "114年06月 2330 台積電           各日成交資訊"

        Args:
            stock_id: 股票代號

        Returns:
            CompanyInfo or None
        """
        # Try multiple dates to find one with data
        for days_ago in range(7):
            target_date = date.today() - timedelta(days=days_ago)
            url = f"{self.BASE_URL}/STOCK_DAY"
            params = {
                "response": "json",
                "stockNo": stock_id,
                "date": target_date.strftime("%Y%m%d"),
            }

            try:
                response = self.session.get(url, params=params, timeout=self.timeout)
                response.raise_for_status()
                data = response.json()

                title = data.get("title", "")
                if not title:
                    continue

                # Title format: "114年06月 2330 台積電           各日成交資訊"
                match = re.search(r"(\d{3})年(\d{2})月\s+(\d{4})\s+(.+?)\s{2,}", title)
                if match:
                    name = match.group(4).strip()
                    return CompanyInfo(
                        stock_id=stock_id,
                        name=name,
                    )

            except Exception as e:
                print(f"Error fetching company info for {stock_id}: {e}")
                continue

        return None

    def get_all_stock_ids(self) -> list[str]:
        """
        取得所有上市股票代號

        Returns:
            list of stock_id
        """
        url = f"{self.BASE_URL}/MI_INDEX"
        params = {
            "response": "json",
            "date": date.today().strftime("%Y%m%d"),
            "type": "ALLBUT0999",
        }

        try:
            response = self.session.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()

            stock_ids = []
            for table in data.get("tables", []):
                for row in table.get("data", []):
                    if row and len(row) > 0:
                        # First column is usually stock_id
                        match = re.match(r"^(\d{4})", row[0])
                        if match:
                            stock_ids.append(match.group(1))

            return sorted(set(stock_ids))

        except Exception as e:
            print(f"Error fetching stock list: {e}")
            return []

    def _parse_roc_date(self, date_str: str) -> Optional[date]:
        """解析民國日期字串 (例如: "114/01/02")"""
        try:
            parts = date_str.split("/")
            if len(parts) != 3:
                return None
            year = int(parts[0]) + 1911  # 民國轉西元
            month = int(parts[1])
            day = int(parts[2])
            return date(year, month, day)
        except (ValueError, IndexError):
            return None

    def _parse_float(self, value: str) -> float:
        """解析浮點數 (處理逗號格式)"""
        try:
            if isinstance(value, (int, float)):
                return float(value)
            return float(value.replace(",", "").replace("+", ""))
        except (ValueError, AttributeError):
            return 0.0

    def _parse_int(self, value: str) -> int:
        """解析整數 (處理逗號格式)"""
        try:
            if isinstance(value, int):
                return value
            return int(value.replace(",", ""))
        except (ValueError, AttributeError):
            return 0
