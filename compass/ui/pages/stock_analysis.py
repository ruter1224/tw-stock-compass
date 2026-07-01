"""
個股分析頁（核心）

元件：
- 股票代號/名稱/產業
- 五大維度雷達圖
- 維度詳情卡片
- 目標 PE 定價
- 追價安全圈（雙軌制）
- 股價位置指示器
- 操作按鈕
"""

import flet as ft
from typing import Callable, Optional

from compass.core.dimensions import FiveDimensions, DimensionScore
from compass.core.target_pe import TargetPEResult, TargetPECalculator
from compass.core.safety_zone import DualTrackSafetyZone, SafetyZoneCalculator


class StockAnalysisPage:
    """個股分析頁"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate
        self.stock_id: Optional[str] = None
        self.company_name: str = ""
        self.industry: str = ""
        self.current_price: float = 0.0
        self.dimensions: Optional[FiveDimensions] = None
        self.target_pe_result: Optional[TargetPEResult] = None
        self.safety_zone: Optional[DualTrackSafetyZone] = None

    def build(self) -> ft.Control:
        """建立個股分析頁 UI"""
        if self.stock_id is None:
            return self._build_empty_state()

        return ft.Column(
            [
                self._build_header(),
                self._build_dimensions_section(),
                self._build_target_pe_section(),
                self._build_safety_zone_section(),
                self._build_action_buttons(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_empty_state(self) -> ft.Control:
        """空狀態"""
        return ft.Column(
            [
                ft.Text("個股分析", size=24, weight=ft.FontWeight.BOLD),
                ft.Text("請輸入股票代號開始分析", color=ft.Colors.GREY_600),
                ft.TextField(
                    label="股票代號",
                    hint_text="例如：2330",
                    on_submit=self._on_stock_id_submit,
                    width=300,
                ),
            ],
            spacing=20,
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _build_header(self) -> ft.Control:
        """股票資訊標頭"""
        return ft.Card(
            content=ft.Container(
                content=ft.Row(
                    [
                        ft.Column(
                            [
                                ft.Text(self.stock_id, size=24, weight=ft.FontWeight.BOLD),
                                ft.Text(self.company_name, size=16),
                            ],
                            spacing=5,
                        ),
                        ft.VerticalDivider(),
                        ft.Column(
                            [
                                ft.Text(f"NT$ {self.current_price:.2f}", size=20, weight=ft.FontWeight.BOLD),
                                ft.Text(self.industry, size=14, color=ft.Colors.GREY_600),
                            ],
                            spacing=5,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                padding=20,
            )
        )

    def _build_dimensions_section(self) -> ft.Control:
        """五大維度區段"""
        if self.dimensions is None:
            return ft.Text("載入中...", color=ft.Colors.GREY_600)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("五大維度評分", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text(f"總分：{self.dimensions.total_score}/100", size=14),
                        ft.Row(
                            [
                                self._build_dimension_card("① 產業鏈地位", self.dimensions.supply_chain_position),
                                self._build_dimension_card("② 產業成長性", self.dimensions.industry_growth),
                                self._build_dimension_card("③ 企業護城河", self.dimensions.moat),
                                self._build_dimension_card("④ 財務模式", self.dimensions.financial_model),
                                self._build_dimension_card("⑤ 風險因子", self.dimensions.risk_discount),
                            ],
                            spacing=10,
                            wrap=True,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_dimension_card(self, title: str, score: DimensionScore) -> ft.Control:
        """維度卡片"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=12, weight=ft.FontWeight.BOLD),
                    ft.Text(f"{score.score}/20", size=20, weight=ft.FontWeight.BOLD),
                    ft.Text(score.level.value, size=10, color=ft.Colors.GREY_600),
                ],
                spacing=5,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=120,
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=5,
        )

    def _build_target_pe_section(self) -> ft.Control:
        """目標 PE 定價區段"""
        if self.target_pe_result is None:
            return ft.Text("載入中...", color=ft.Colors.GREY_600)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("目標本益比定價", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text("評級", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(self.target_pe_result.tier.value, size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=5,
                                ),
                                ft.Column(
                                    [
                                        ft.Text("目標 PE 區間", size=12, color=ft.Colors.GREY_600),
                                        ft.Text(self.target_pe_result.pe_range.range_str, size=16, weight=ft.FontWeight.BOLD),
                                    ],
                                    spacing=5,
                                ),
                            ],
                            spacing=30,
                        ),
                        ft.Text(self.target_pe_result.description, size=12, color=ft.Colors.GREY_600),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _build_safety_zone_section(self) -> ft.Control:
        """追價安全圈區段（雙軌制）"""
        if self.safety_zone is None:
            return ft.Text("載入中...", color=ft.Colors.GREY_600)

        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("追價安全圈（雙軌制）", size=18, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                self._build_safety_zone_card("安全邊際法", self.safety_zone.margin_of_safety),
                                self._build_safety_zone_card("DCF 折現法", self.safety_zone.dcf),
                            ],
                            spacing=20,
                        ),
                        ft.Divider(),
                        ft.Text("綜合建議區間", size=14, weight=ft.FontWeight.BOLD),
                        ft.Row(
                            [
                                ft.Text(f"便宜價：{self.safety_zone.combined_cheap_range}"),
                                ft.Text(f"合理價：{self.safety_zone.combined_fair_range}"),
                                ft.Text(f"昂貴價：{self.safety_zone.combined_expensive_range}"),
                            ],
                            spacing=20,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_safety_zone_card(self, title: str, zone) -> ft.Control:
        """安全圈卡片"""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(title, size=14, weight=ft.FontWeight.BOLD),
                    ft.Text(f"內在價值：NT$ {zone.intrinsic_value:.2f}", size=12),
                    ft.Text(f"便宜價：{zone.price_zones.cheap_range}", size=12),
                    ft.Text(f"合理價：{zone.price_zones.fair_range}", size=12),
                    ft.Text(f"昂貴價：{zone.price_zones.excessive_range}", size=12),
                ],
                spacing=5,
            ),
            padding=15,
            border=ft.border.all(1, ft.Colors.GREY_300),
            border_radius=5,
        )

    def _build_action_buttons(self) -> ft.Control:
        """操作按鈕"""
        return ft.Row(
            [
                ft.ElevatedButton(
                    "查看產業詳情",
                    icon=ft.Icons.BUSINESS,
                    on_click=lambda e: self.on_navigate(f"industry_analysis:{self.stock_id}"),
                ),
                ft.ElevatedButton(
                    "查看催化劑",
                    icon=ft.Icons.TRENDING_UP,
                    on_click=lambda e: self.on_navigate(f"catalyst:{self.stock_id}"),
                ),
                ft.OutlinedButton(
                    "匯出 HTML",
                    icon=ft.Icons.DOWNLOAD,
                    on_click=self._on_export_html,
                ),
            ],
            spacing=10,
        )

    def _on_stock_id_submit(self, e):
        """股票代號提交"""
        stock_id = e.control.value.strip()
        if stock_id:
            self.on_navigate(f"stock_analysis:{stock_id}")

    def _on_export_html(self, e):
        """匯出 HTML"""
        # TODO: 實作匯出功能
        pass

    def set_stock_data(
        self,
        stock_id: str,
        company_name: str,
        industry: str,
        current_price: float,
        dimensions: FiveDimensions,
    ):
        """設定股票資料"""
        self.stock_id = stock_id
        self.company_name = company_name
        self.industry = industry
        self.current_price = current_price
        self.dimensions = dimensions

        # 計算目標 PE
        self.target_pe_result = TargetPECalculator.calculate(dimensions)

        # 計算追價安全圈
        eps = 0.0  # TODO: 從財務資料取得
        self.safety_zone = SafetyZoneCalculator.calculate_dual_track(
            dimensions, eps, current_price
        )
