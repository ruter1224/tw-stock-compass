"""
資產配置頁

元件：
- 年齡輸入
- 風險屬性選擇
- 配置建議圖
- 兩岸風險情境
- 配置調整表
- 情境說明
"""

import flet as ft
from typing import Callable, Optional


class AllocationPage:
    """資產配置頁"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate
        self.age: int = 30
        self.risk_scenario: str = "low"

    def build(self) -> ft.Control:
        """建立資產配置頁 UI"""
        return ft.Column(
            [
                self._build_header(),
                self._build_age_input(),
                self._build_risk_scenario(),
                self._build_allocation_result(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_header(self) -> ft.Control:
        """標頭"""
        return ft.Text("資產配置建議", size=24, weight=ft.FontWeight.BOLD)

    def _build_age_input(self) -> ft.Control:
        """年齡輸入"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("您的年齡", size=16, weight=ft.FontWeight.BOLD),
                        ft.Slider(
                            min=20,
                            max=70,
                            divisions=50,
                            value=self.age,
                            label="{value} 歲",
                            on_change=self._on_age_change,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _build_risk_scenario(self) -> ft.Control:
        """兩岸風險情境"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("兩岸風險情境", size=16, weight=ft.FontWeight.BOLD),
                        ft.RadioGroup(
                            content=ft.Row(
                                [
                                    ft.Radio(value="low", label="平時（低風險）"),
                                    ft.Radio(value="medium", label="風險升溫（中度）"),
                                    ft.Radio(value="high", label="高度緊張"),
                                ]
                            ),
                            value=self.risk_scenario,
                            on_change=self._on_risk_change,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _build_allocation_result(self) -> ft.Control:
        """配置建議結果"""
        # 根據年齡和風險情境計算配置
        allocation = self._calculate_allocation()

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("配置建議", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                self._build_allocation_item("台股", allocation["tw_stock"], ft.Colors.BLUE),
                                self._build_allocation_item("海外核心", allocation["overseas_core"], ft.Colors.GREEN),
                                self._build_allocation_item("海外避險", allocation["overseas_hedge"], ft.Colors.ORANGE),
                            ],
                            spacing=20,
                        ),
                        ft.Divider(),
                        ft.Text(self._get_recommendation(), size=14, color=ft.Colors.GREY_700),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_allocation_item(self, label: str, percentage: float, color: str) -> ft.Control:
        """配置項目"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(label, size=12, color=ft.Colors.GREY_600),
                    ft.Text(f"{percentage:.0f}%", size=24, weight=ft.FontWeight.BOLD, color=color),
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=150,
            padding=15,
            border=ft.border.all(1, color),
            border_radius=10,
        )

    def _calculate_allocation(self) -> dict:
        """計算配置"""
        # 根據年齡決定風險屬性
        if self.age < 30:
            risk_profile = "aggressive"
        elif self.age < 40:
            risk_profile = "adventurous"
        elif self.age < 50:
            risk_profile = "balanced"
        elif self.age < 60:
            risk_profile = "conservative"
        else:
            risk_profile = "very_conservative"

        # 根據風險情境調整
        if self.risk_scenario == "low":
            return {"tw_stock": 25, "overseas_core": 65, "overseas_hedge": 10}
        elif self.risk_scenario == "medium":
            return {"tw_stock": 15, "overseas_core": 55, "overseas_hedge": 30}
        else:
            return {"tw_stock": 5, "overseas_core": 45, "overseas_hedge": 50}

    def _get_recommendation(self) -> str:
        """取得建議"""
        if self.risk_scenario == "low":
            return "維持正常成長型配置，定期檢視投資組合。"
        elif self.risk_scenario == "medium":
            return "建議減碼台股，增加海外避險資產，降低風險曝險。"
        else:
            return "建議集中美元現金、T-Bill、黃金，大幅降低台股曝險。"

    def _on_age_change(self, e):
        """年齡變更"""
        self.age = int(e.control.value)

    def _on_risk_change(self, e):
        """風險情境變更"""
        self.risk_scenario = e.control.value
