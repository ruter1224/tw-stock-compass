"""
產業分析頁

元件：
- 產業名稱
- 產業結構惡化評分
- 企業體質惡化評分
- 產業站隊評分
- 同業比較表
- 杜邦分析圖
"""

import flet as ft
from typing import Callable, Optional

from compass.ui.utils import border_all


class IndustryAnalysisPage:
    """產業分析頁"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate
        self.stock_id: Optional[str] = None
        self.industry_name: str = ""
        self.deterioration_score: float = 0.0
        self.business_deterioration_score: float = 0.0
        self.position_score: float = 0.0

    def build(self) -> ft.Control:
        """建立產業分析頁 UI"""
        if self.stock_id is None:
            return self._build_empty_state()

        return ft.Column(
            [
                self._build_header(),
                self._build_score_cards(),
                self._build_peer_comparison(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_empty_state(self) -> ft.Control:
        """空狀態"""
        return ft.Column(
            [
                ft.Text("產業分析", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("請先從個股分析頁進入", color=ft.Colors.GREY_600),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _build_header(self) -> ft.Control:
        """產業資訊標頭"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text(self.industry_name, size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"股票代號：{self.stock_id}", size=14, color=ft.Colors.GREY_600),
                    ],
                    spacing=5,
                ),
                padding=20,
            )
        )

    def _build_score_cards(self) -> ft.Control:
        """評分卡片"""
        return ft.Row(
            [
                self._build_score_card(
                    "產業結構惡化",
                    self.deterioration_score,
                    10,
                    self._get_deterioration_interpretation(),
                ),
                self._build_score_card(
                    "企業體質惡化",
                    self.business_deterioration_score,
                    10,
                    self._get_business_deterioration_interpretation(),
                ),
                self._build_score_card(
                    "產業站隊評分",
                    self.position_score,
                    10,
                    self._get_position_interpretation(),
                ),
            ],
            spacing=20,
        )

    def _build_score_card(self, title: str, score: float, max_score: float, interpretation: str) -> ft.Control:
        """評分卡片"""
        percentage = score / max_score
        color = ft.Colors.GREEN if percentage < 0.4 else ft.Colors.ORANGE if percentage < 0.7 else ft.Colors.RED

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{score:.1f}/{max_score:.0f}", size=24, weight=ft.FontWeight.BOLD, color=color),
                    ft.Text(interpretation, size=12, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=200,
            padding=20,
            border=border_all(1, ft.Colors.GREY_300),
            border_radius=10,
        )

    def _build_peer_comparison(self) -> ft.Control:
        """同業比較"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("同業比較", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("（載入中...）", color=ft.Colors.GREY_600),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _get_deterioration_interpretation(self) -> str:
        """產業結構惡化判讀"""
        if self.deterioration_score <= 3:
            return "典型景氣循環\n產業長期 OK"
        elif self.deterioration_score <= 6:
            return "灰色地帶\n需看公司層面"
        else:
            return "結構性惡化\n不適合長抱"

    def _get_business_deterioration_interpretation(self) -> str:
        """企業體質惡化判讀"""
        if self.business_deterioration_score <= 3:
            return "僅週期影響\n大家一起衰"
        elif self.business_deterioration_score <= 6:
            return "待觀察\n週期＋體質"
        else:
            return "體質已惡化\n全面落後"

    def _get_position_interpretation(self) -> str:
        """產業站隊判讀"""
        if self.position_score >= 8:
            return "核心配置\n急跌可加碼"
        elif self.position_score >= 6:
            return "中性觀察\n追蹤 CAPEX"
        else:
            return "結構性風險\n不建議投入"

    def set_industry_data(
        self,
        stock_id: str,
        industry_name: str,
        deterioration_score: float,
        business_deterioration_score: float,
        position_score: float,
    ):
        """設定產業資料"""
        self.stock_id = stock_id
        self.industry_name = industry_name
        self.deterioration_score = deterioration_score
        self.business_deterioration_score = business_deterioration_score
        self.position_score = position_score
