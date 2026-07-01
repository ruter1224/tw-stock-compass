"""
Flet App 主體

UI 架構：
- 左側導航欄（功能選單 + 最近查詢）
- 右側主內容區（各功能頁面）
- 底部狀態列（資料更新時間、快取狀態）
"""

import flet as ft
from typing import Optional, Any

from compass.ui.pages import (
    HomePage,
    StockAnalysisPage,
    IndustryAnalysisPage,
    CatalystPage,
    ComparisonPage,
    AllocationPage,
    ReviewPage,
    SettingsPage,
)


class State:
    """Simple state holder — replaces ft.State (removed in Flet 0.85.x)."""
    def __init__(self, default: Any = None):
        self._value = default

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, val: Any) -> None:
        self._value = val


def create_app(page: ft.Page):
    """建立 Flet 應用程式"""
    page.title = "台股價值投資分析系統"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1280
    page.window_height = 800

    # 狀態
    current_page = State("home")
    current_stock_id = State(None)

    # 建立頁面實例
    home_page = HomePage(on_navigate=lambda route: navigate(route))
    stock_analysis_page = StockAnalysisPage(on_navigate=lambda route: navigate(route))
    industry_analysis_page = IndustryAnalysisPage(on_navigate=lambda route: navigate(route))
    catalyst_page = CatalystPage(on_navigate=lambda route: navigate(route))
    comparison_page = ComparisonPage(on_navigate=lambda route: navigate(route))
    allocation_page = AllocationPage(on_navigate=lambda route: navigate(route))
    review_page = ReviewPage(on_navigate=lambda route: navigate(route))
    settings_page = SettingsPage(on_navigate=lambda route: navigate(route))

    # 內容區域
    content_area = ft.Container(
        content=ft.Column([home_page.build()]),
        expand=True,
        padding=20,
    )

    def navigate(route: str):
        """導航至指定頁面"""
        parts = route.split(":")
        page_name = parts[0]
        param = parts[1] if len(parts) > 1 else None

        current_page.value = page_name

        if param:
            current_stock_id.value = param

        # 更新內容區域
        if page_name == "home":
            content_area.content = ft.Column([home_page.build()])
        elif page_name == "stock_analysis":
            if param:
                # TODO: 載入股票資料
                stock_analysis_page.stock_id = param
            content_area.content = ft.Column([stock_analysis_page.build()])
        elif page_name == "industry_analysis":
            if param:
                industry_analysis_page.stock_id = param
            content_area.content = ft.Column([industry_analysis_page.build()])
        elif page_name == "catalyst":
            if param:
                catalyst_page.stock_id = param
            content_area.content = ft.Column([catalyst_page.build()])
        elif page_name == "comparison":
            content_area.content = ft.Column([comparison_page.build()])
        elif page_name == "allocation":
            content_area.content = ft.Column([allocation_page.build()])
        elif page_name == "review":
            content_area.content = ft.Column([review_page.build()])
        elif page_name == "settings":
            content_area.content = ft.Column([settings_page.build()])

        page.update()

    # 導航項目
    nav_items = [
        ft.ListTile(
            leading=ft.Icon(ft.Icons.HOME),
            title=ft.Text("首頁"),
            selected=current_page.value == "home",
            on_click=lambda e: navigate("home"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.ANALYTICS),
            title=ft.Text("個股分析"),
            selected=current_page.value == "stock_analysis",
            on_click=lambda e: navigate("stock_analysis"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.BUSINESS),
            title=ft.Text("產業分析"),
            selected=current_page.value == "industry_analysis",
            on_click=lambda e: navigate("industry_analysis"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.TRENDING_UP),
            title=ft.Text("催化劑"),
            selected=current_page.value == "catalyst",
            on_click=lambda e: navigate("catalyst"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.COMPARE),
            title=ft.Text("多股比較"),
            selected=current_page.value == "comparison",
            on_click=lambda e: navigate("comparison"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.PIE_CHART),
            title=ft.Text("資產配置"),
            selected=current_page.value == "allocation",
            on_click=lambda e: navigate("allocation"),
        ),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.HISTORY),
            title=ft.Text("復盤系統"),
            selected=current_page.value == "review",
            on_click=lambda e: navigate("review"),
        ),
        ft.Divider(),
        ft.ListTile(
            leading=ft.Icon(ft.Icons.SETTINGS),
            title=ft.Text("設定"),
            selected=current_page.value == "settings",
            on_click=lambda e: navigate("settings"),
        ),
    ]

    # 最近查詢區域
    recent_queries = ft.Column(
        [
            ft.Text("最近查詢", size=14, weight=ft.FontWeight.BOLD),
            ft.Text("（尚無紀錄）", size=12, color=ft.Colors.GREY_600),
        ],
        spacing=5,
    )

    # 左側導航欄
    nav_rail = ft.Container(
        content=ft.Column(
            [
                ft.Text("台股價值投資分析", size=16, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                *nav_items,
                ft.Divider(),
                recent_queries,
            ],
            spacing=0,
        ),
        width=220,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
        padding=10,
    )

    # 底部狀態列
    status_bar = ft.Container(
        content=ft.Row(
            [
                ft.Text("資料更新時間：--", size=12),
                ft.Text("快取狀態：正常", size=12),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        padding=10,
        bgcolor=ft.Colors.SURFACE_CONTAINER,
    )

    # 主版面
    page.add(
        ft.Row(
            [
                nav_rail,
                ft.VerticalDivider(),
                content_area,
            ],
            expand=True,
        ),
        status_bar,
    )
