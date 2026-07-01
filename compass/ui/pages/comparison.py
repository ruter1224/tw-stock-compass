"""
多股比較頁

元件：
- 股票選擇器
- 比較維度選擇
- 比較表格
- 雷達圖疊加
- 安全圈比較
- 進度條
"""

import flet as ft
from typing import Callable, Optional


class ComparisonPage:
    """多股比較頁"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate
        self.selected_stocks: list[str] = []

    def build(self) -> ft.Control:
        """建立多股比較頁 UI"""
        return ft.Column(
            [
                self._build_header(),
                self._build_stock_selector(),
                self._build_comparison_table(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_header(self) -> ft.Control:
        """標頭"""
        return ft.Text("多股比較", size=24, weight=ft.FontWeight.BOLD)

    def _build_stock_selector(self) -> ft.Control:
        """股票選擇器"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("選擇股票（2-10 檔）", size=16, weight=ft.FontWeight.BOLD),
                        ft.TextField(
                            label="股票代號",
                            hint_text="輸入代號後按 Enter（例如：2330）",
                            on_submit=self._on_add_stock,
                            width=300,
                        ),
                        ft.Wrap(
                            [self._build_stock_chip(s) for s in self.selected_stocks],
                            spacing=10,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_stock_chip(self, stock_id: str) -> ft.Control:
        """股票標籤"""
        return ft.Chip(
            label=ft.Text(stock_id),
            on_click=lambda e, sid=stock_id: self._on_remove_stock(sid),
        )

    def _build_comparison_table(self) -> ft.Control:
        """比較表格"""
        if len(self.selected_stocks) < 2:
            return ft.Text("請選擇至少 2 檔股票進行比較", color=ft.Colors.GREY_600)

        rows = []
        for stock_id in self.selected_stocks:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.TextButton(
                                stock_id,
                                on_click=lambda e, sid=stock_id: self.on_navigate(f"stock_analysis:{sid}"),
                            )
                        ),
                        ft.DataCell(ft.Text("--")),  # 產業鏈地位
                        ft.DataCell(ft.Text("--")),  # 產業成長性
                        ft.DataCell(ft.Text("--")),  # 企業護城河
                        ft.DataCell(ft.Text("--")),  # 財務模式
                        ft.DataCell(ft.Text("--")),  # 風險因子
                        ft.DataCell(ft.Text("--")),  # 總分
                    ]
                )
            )

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("比較結果", size=18, weight=ft.FontWeight.BOLD),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("代號")),
                                ft.DataColumn(ft.Text("產業鏈地位")),
                                ft.DataColumn(ft.Text("產業成長性")),
                                ft.DataColumn(ft.Text("企業護城河")),
                                ft.DataColumn(ft.Text("財務模式")),
                                ft.DataColumn(ft.Text("風險因子")),
                                ft.DataColumn(ft.Text("總分")),
                            ],
                            rows=rows,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _on_add_stock(self, e):
        """新增股票"""
        stock_id = e.control.value.strip()
        if stock_id and stock_id not in self.selected_stocks and len(self.selected_stocks) < 10:
            self.selected_stocks.append(stock_id)
            e.control.value = ""

    def _on_remove_stock(self, stock_id: str):
        """移除股票"""
        if stock_id in self.selected_stocks:
            self.selected_stocks.remove(stock_id)
