"""
復盤系統頁

元件：
- 交易紀錄表
- 新增交易按鈕
- 績效統計卡片
- 走勢對比圖
- 匯出按鈕
- 匯入按鈕
"""

import flet as ft
from typing import Callable, Optional


class ReviewPage:
    """復盤系統頁"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate
        self.trade_records: list[dict] = []

    def build(self) -> ft.Control:
        """建立復盤系統頁 UI"""
        return ft.Column(
            [
                self._build_header(),
                self._build_statistics(),
                self._build_trade_table(),
                self._build_action_buttons(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_header(self) -> ft.Control:
        """標頭"""
        return ft.Row(
            [
                ft.Text("復盤系統", size=24, weight=ft.FontWeight.BOLD),
                ft.ElevatedButton(
                    "新增交易",
                    icon=ft.Icons.ADD,
                    on_click=self._on_add_trade,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_statistics(self) -> ft.Control:
        """績效統計"""
        stats = self._calculate_statistics()

        return ft.Row(
            [
                self._build_stat_card("總交易次數", str(stats["total_trades"]), ft.Colors.BLUE),
                self._build_stat_card("勝率", f"{stats['win_rate']:.1f}%", ft.Colors.GREEN),
                self._build_stat_card("盈虧比", f"{stats['profit_loss_ratio']:.2f}", ft.Colors.ORANGE),
                self._build_stat_card("平均報酬", f"{stats['avg_return']:.2f}%", ft.Colors.PURPLE),
            ],
            spacing=20,
        )

    def _build_stat_card(self, label: str, value: str, color: str) -> ft.Control:
        """統計卡片"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(value, size=20, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=150,
            padding=15,
            border=ft.border.Border(
                left=ft.border.BorderSide(1, color),
                right=ft.border.BorderSide(1, color),
                top=ft.border.BorderSide(1, color),
                bottom=ft.border.BorderSide(1, color),
            ),
            border_radius=10,
        )

    def _build_trade_table(self) -> ft.Control:
        """交易紀錄表"""
        rows = []
        for record in self.trade_records:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(record.get("date", ""))),
                        ft.DataCell(
                            ft.TextButton(
                                record.get("stock_id", ""),
                                on_click=lambda e, sid=record.get("stock_id"): self.on_navigate(f"stock_analysis:{sid}"),
                            )
                        ),
                        ft.DataCell(ft.Text(record.get("type", ""))),
                        ft.DataCell(ft.Text(f"{record.get('price', 0):.2f}")),
                        ft.DataCell(ft.Text(str(record.get("quantity", 0)))),
                        ft.DataCell(ft.Text(record.get("reason", ""))),
                    ]
                )
            )

        if not rows:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("尚無交易紀錄", color=ft.Colors.GREY_600)),
                        ft.DataCell(ft.Text("")),
                        ft.DataCell(ft.Text("")),
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
                        ft.Text("交易紀錄", size=18, weight=ft.FontWeight.BOLD),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("日期")),
                                ft.DataColumn(ft.Text("代號")),
                                ft.DataColumn(ft.Text("類型")),
                                ft.DataColumn(ft.Text("價格"), numeric=True),
                                ft.DataColumn(ft.Text("數量"), numeric=True),
                                ft.DataColumn(ft.Text("理由")),
                            ],
                            rows=rows,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _build_action_buttons(self) -> ft.Control:
        """操作按鈕"""
        return ft.Row(
            [
                ft.OutlinedButton(
                    "匯出 CSV",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=self._on_export_csv,
                ),
                ft.OutlinedButton(
                    "匯出 JSON",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=self._on_export_json,
                ),
                ft.OutlinedButton(
                    "匯入備份",
                    icon=ft.Icons.UPLOAD,
                    on_click=self._on_import_backup,
                ),
            ],
            spacing=10,
        )

    def _calculate_statistics(self) -> dict:
        """計算統計數據"""
        if not self.trade_records:
            return {
                "total_trades": 0,
                "win_rate": 0.0,
                "profit_loss_ratio": 0.0,
                "avg_return": 0.0,
            }

        # TODO: 實作實際統計計算
        return {
            "total_trades": len(self.trade_records),
            "win_rate": 0.0,
            "profit_loss_ratio": 0.0,
            "avg_return": 0.0,
        }

    def _on_add_trade(self, e):
        """新增交易"""
        # TODO: 開啟新增交易對話框
        pass

    def _on_export_csv(self, e):
        """匯出 CSV"""
        # TODO: 實作匯出功能
        pass

    def _on_export_json(self, e):
        """匯出 JSON"""
        # TODO: 實作匯出功能
        pass

    def _on_import_backup(self, e):
        """匯入備份"""
        # TODO: 實作匯入功能
        pass

    def add_trade_record(self, record: dict):
        """新增交易紀錄"""
        self.trade_records.append(record)
