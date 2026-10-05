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

from typing import Callable

import flet as ft

from compass.auxiliary.allocation import AllocationResult, AssetAllocationAdvisor, RiskScenario


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
                                self._build_allocation_item(
                                    "台股", allocation.tw_stock_ratio, ft.Colors.BLUE
                                ),
                                self._build_allocation_item(
                                    "海外核心", allocation.overseas_core_ratio, ft.Colors.GREEN
                                ),
                                self._build_allocation_item(
                                    "海外避險", allocation.overseas_hedge_ratio, ft.Colors.ORANGE
                                ),
                            ],
                            spacing=20,
                        ),
                        ft.Divider(),
                        ft.Text(allocation.recommendation, size=14, color=ft.Colors.GREY_700),
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
            border=ft.border.Border(
                left=ft.border.BorderSide(1, color),
                right=ft.border.BorderSide(1, color),
                top=ft.border.BorderSide(1, color),
                bottom=ft.border.BorderSide(1, color),
            ),
            border_radius=10,
        )

    def _calculate_allocation(self) -> AllocationResult:
        """計算配置"""
        scenario_map = {
            "low": RiskScenario.LOW,
            "medium": RiskScenario.MEDIUM,
            "high": RiskScenario.HIGH,
        }
        scenario = scenario_map.get(self.risk_scenario, RiskScenario.LOW)
        return AssetAllocationAdvisor.calculate(self.age, scenario)

    def _on_age_change(self, e):
        """年齡變更"""
        self.age = int(e.control.value)

    def _on_risk_change(self, e):
        """風險情境變更"""
        self.risk_scenario = e.control.value
