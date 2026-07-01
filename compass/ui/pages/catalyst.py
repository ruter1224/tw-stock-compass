"""
催化劑儀表板

元件：
- 股票代號
- 基本面訊號
- 技術面訊號
- 籌碼面訊號
- 訊號強度指示器
- 歷史訊號紀錄
"""

import flet as ft
from typing import Callable, Optional


class CatalystPage:
    """催化劑儀表板"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate
        self.stock_id: Optional[str] = None
        self.fundamental_signals: list[dict] = []
        self.technical_signals: list[dict] = []
        self.chips_signals: list[dict] = []

    def build(self) -> ft.Control:
        """建立催化劑頁 UI"""
        if self.stock_id is None:
            return self._build_empty_state()

        return ft.Column(
            [
                self._build_header(),
                self._build_signal_sections(),
                self._build_signal_history(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_empty_state(self) -> ft.Control:
        """空狀態"""
        return ft.Column(
            [
                ft.Text("催化劑儀表板", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("請先從個股分析頁進入", color=ft.Colors.GREY_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _build_header(self) -> ft.Control:
        """股票資訊標頭"""
        return ft.Card(
            content=ft.Container(
                content=ft.Text(f"催化劑分析：{self.stock_id}", size=20, weight=ft.FontWeight.BOLD),
                padding=20,
            )
        )

    def _build_signal_sections(self) -> ft.Control:
        """訊號區段"""
        return ft.Row(
            [
                self._build_signal_section("基本面訊號", self.fundamental_signals, ft.Colors.BLUE),
                self._build_signal_section("技術面訊號", self.technical_signals, ft.Colors.GREEN),
                self._build_signal_section("籌碼面訊號", self.chips_signals, ft.Colors.ORANGE),
            ],
            spacing=20,
        )

    def _build_signal_section(self, title: str, signals: list[dict], color: str) -> ft.Control:
        """訊號區段"""
        items = []
        for signal in signals:
            items.append(
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.CHECK_CIRCLE if signal.get("positive", True) else ft.Icons.CANCEL,
                        color=color,
                    ),
                    title=ft.Text(signal.get("name", ""), size=14),
                    subtitle=ft.Text(signal.get("description", ""), size=12),
                )
            )

        if not items:
            items.append(ft.Text("暫無訊號", color=ft.Colors.GREY_600, size=12))

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color=color),
                    *items,
                ],
                spacing=5,
            ),
            width=300,
            padding=15,
            border=ft.border.all(1, color),
            border_radius=10,
        )

    def _build_signal_history(self) -> ft.Control:
        """歷史訊號紀錄"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("歷史訊號紀錄", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("（過去 6 個月的訊號紀錄）", color=ft.Colors.GREY_600),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def set_signals(
        self,
        stock_id: str,
        fundamental_signals: list[dict],
        technical_signals: list[dict],
        chips_signals: list[dict],
    ):
        """設定訊號資料"""
        self.stock_id = stock_id
        self.fundamental_signals = fundamental_signals
        self.technical_signals = technical_signals
        self.chips_signals = chips_signals
