"""
SQLite 資料快取

所有資料擷取後快取至本地 SQLite，避免重複 fetch，並支援離線查看最近已查資料。
"""

import sqlite3
from datetime import date, datetime
from pathlib import Path
from typing import Optional, Any
import json


class DataCache:
    """資料快取管理器"""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = str(Path.home() / ".tw-stock-compass" / "cache.db")

        self.db_path = db_path
        self._ensure_db_dir()
        self._init_db()

    def _ensure_db_dir(self):
        """確保資料庫目錄存在"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    def _init_db(self):
        """初始化資料庫"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS cache (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    created_at TEXT,
                    expires_at TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS stock_prices (
                    stock_id TEXT,
                    date TEXT,
                    open REAL,
                    high REAL,
                    low REAL,
                    close REAL,
                    volume INTEGER,
                    PRIMARY KEY (stock_id, date)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS financial_data (
                    stock_id TEXT,
                    year INTEGER,
                    quarter INTEGER,
                    roe REAL,
                    eps REAL,
                    net_worth_per_share REAL,
                    gross_margin REAL,
                    operating_margin REAL,
                    debt_ratio REAL,
                    free_cash_flow REAL,
                    PRIMARY KEY (stock_id, year, quarter)
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS analysis_cache (
                    stock_id TEXT PRIMARY KEY,
                    dimensions_score TEXT,
                    target_pe TEXT,
                    safety_zone TEXT,
                    updated_at TEXT
                )
            """)

            conn.execute("""
                CREATE TABLE IF NOT EXISTS trade_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    stock_id TEXT,
                    trade_type TEXT,
                    price REAL,
                    quantity INTEGER,
                    trade_date TEXT,
                    reason TEXT,
                    dimensions_snapshot TEXT,
                    created_at TEXT
                )
            """)

    def get(self, key: str) -> Optional[Any]:
        """取得快取值"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT value, expires_at FROM cache WHERE key = ?",
                (key,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            value_json, expires_at = row

            # 檢查是否過期
            if expires_at:
                expires = datetime.fromisoformat(expires_at)
                if datetime.now() > expires:
                    conn.execute("DELETE FROM cache WHERE key = ?", (key,))
                    return None

            return json.loads(value_json)

    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None):
        """設定快取值"""
        expires_at = None
        if ttl_seconds:
            expires_at = datetime.now() + __import__("datetime").timedelta(seconds=ttl_seconds)
            expires_at = expires_at.isoformat()

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO cache (key, value, created_at, expires_at)
                VALUES (?, ?, ?, ?)
                """,
                (key, json.dumps(value), datetime.now().isoformat(), expires_at),
            )

    def delete(self, key: str):
        """刪除快取"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("DELETE FROM cache WHERE key = ?", (key,))

    def clear_expired(self):
        """清除過期快取"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "DELETE FROM cache WHERE expires_at IS NOT NULL AND expires_at < ?",
                (datetime.now().isoformat(),),
            )

    def save_stock_price(self, stock_id: str, date: date, open: float, high: float, low: float, close: float, volume: int):
        """儲存股價資料"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO stock_prices
                (stock_id, date, open, high, low, close, volume)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (stock_id, date.isoformat(), open, high, low, close, volume),
            )

    def get_stock_prices(self, stock_id: str, limit: int = 365) -> list[dict]:
        """取得股價資料"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT date, open, high, low, close, volume
                FROM stock_prices
                WHERE stock_id = ?
                ORDER BY date DESC
                LIMIT ?
                """,
                (stock_id, limit),
            )
            return [
                {
                    "date": row[0],
                    "open": row[1],
                    "high": row[2],
                    "low": row[3],
                    "close": row[4],
                    "volume": row[5],
                }
                for row in cursor.fetchall()
            ]

    def save_analysis(self, stock_id: str, dimensions_score: dict, target_pe: dict, safety_zone: dict):
        """儲存分析結果"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO analysis_cache
                (stock_id, dimensions_score, target_pe, safety_zone, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    stock_id,
                    json.dumps(dimensions_score),
                    json.dumps(target_pe),
                    json.dumps(safety_zone),
                    datetime.now().isoformat(),
                ),
            )

    def get_analysis(self, stock_id: str) -> Optional[dict]:
        """取得分析結果"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                """
                SELECT dimensions_score, target_pe, safety_zone, updated_at
                FROM analysis_cache
                WHERE stock_id = ?
                """,
                (stock_id,),
            )
            row = cursor.fetchone()

            if row is None:
                return None

            return {
                "dimensions_score": json.loads(row[0]),
                "target_pe": json.loads(row[1]),
                "safety_zone": json.loads(row[2]),
                "updated_at": row[3],
            }
