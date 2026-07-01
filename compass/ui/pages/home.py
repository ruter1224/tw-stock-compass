"""
首頁儀表板

元件：
- 歡迎訊息
- 快速搜尋
- 最近查詢
- 市場概覽
- 關注股票
- 系統通知
"""

import flet as ft
from typing import Callable, Optional


class HomePage:
    """首頁儀表板"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate
        self.recent_stocks: list[str] = []
        self.watched_stocks: list[dict] = []

    def build(self) -> ft.Control:
        """建立首頁 UI"""
        return ft.Column(
            [
                self._build_welcome(),
                self._build_search(),
                self._build_market_overview(),
                self._build_recent_queries(),
                self._build_watched_stocks(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_welcome(self) -> ft.Control:
        """歡迎訊息"""
        return ft.Text(
            "歡迎使用台股價值投資分析系統",
            size=24,
            weight=ft.FontWeight.BOLD,
        )

    def _build_search(self) -> ft.Control:
        """快速搜尋"""
        return ft.TextField(
            label="搜尋股票",
            hint_text="輸入股票代號（例如：2330）",
            prefix_icon=ft.Icons.SEARCH,
            on_submit=self._on_search_submit,
            width=400,
        )

    def _build_market_overview(self) -> ft.Control:
        """市場概覽"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("市場概覽", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                self._build_stat_item("加權指數", "--"),
                                self._build_stat_item("成交量", "--"),
                                self._build_stat_item("漲跌家數", "--"),
                            ],
                            spacing=30,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _build_stat_item(self, label: str, value: str) -> ft.Control:
        """統計項目"""
        return ft.Column(
            [
                ft.Text(label, size=12, color=ft.Colors.GREY_600),
                ft.Text(value, size=16, weight=ft.FontWeight.BOLD),
            ],
            spacing=5,
        )

    def _build_recent_queries(self) -> ft.Control:
        """最近查詢"""
        items = []
        for stock_id in self.recent_stocks[:10]:
            items.append(
                ft.ListTile(
                    title=ft.Text(stock_id),
                    on_click=lambda e, sid=stock_id: self._on_stock_click(sid),
                )
            )

        if not items:
            items.append(ft.Text("尚無查詢紀錄", color=ft.Colors.GREY_600))

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("最近查詢", size=18, weight=ft.FontWeight.BOLD),
                        *items,
                    ],
                    spacing=5,
                ),
                padding=20,
            )
        )

    def _build_watched_stocks(self) -> ft.Control:
        """關注股票"""
        rows = []
        for stock in self.watched_stocks:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.TextButton(
                                stock["stock_id"],
                                on_click=lambda e, sid=stock["stock_id"]: self._on_stock_click(sid),
                            )
                        ),
                        ft.DataCell(ft.Text(stock.get("name", "--"))),
                        ft.DataCell(ft.Text(f"{stock.get('price', 0):.2f}")),
                        ft.DataCell(
                            ft.Text(
                                f"{stock.get('change', 0):+.2f}",
                                color=ft.Colors.GREEN if stock.get("change", 0) >= 0 else ft.Colors.RED,
                            )
                        ),
                    ]
                )
            )

        if not rows:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("尚無關注股票", color=ft.Colors.GREY_600)),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
                    ]
                )
            )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text("關注股票", size=18, weight=ft.FontWeight.BOLD),
                                ft.IconButton(
                                    icon=ft.Icons.ADD,
                                    on_click=self._on_add_watched,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("代號")),
                                ft.DataColumn(ft.Text("名稱")),
                                ft.DataColumn(ft.Text("股價"), numeric=True),
                                ft.DataColumn(ft.Text("漲跌"), numeric=True),
                            ],
                            rows=rows,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _on_search_submit(self, e):
        """搜尋提交"""
        stock_id = e.control.value.strip()
        if stock_id:
            self.recent_stocks.insert(0, stock_id)
            self.recent_stocks = self.recent_stocks[:10]
            self.on_navigate(f"stock_analysis:{stock_id}")

    def _on_stock_click(self, stock_id: str):
        """點擊股票"""
        self.on_navigate(f"stock_analysis:{stock_id}")

    def _on_add_watched(self, e):
        """新增關注股票"""
        # TODO: 開啟新增對話框
        pass

    def add_recent_stock(self, stock_id: str):
        """新增最近查詢"""
        if stock_id in self.recent_stocks:
            self.recent_stocks.remove(stock_id)
        self.recent_stocks.insert(0, stock_id)
        self.recent_stocks = self.recent_stocks[:10]

    def add_watched_stock(self, stock_id: str, name: str, price: float, change: float):
        """新增關注股票"""
        self.watched_stocks.append({
            "stock_id": stock_id,
            "name": name,
            "price": price,
            "change": change,
        })
