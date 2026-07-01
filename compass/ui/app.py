"""
Flet App 主體

UI 架構：
- 左側導航欄（功能選單 + 最近查詢）
- 右側主內容區（各功能頁面）
- 底部狀態列（資料更新時間、快取狀態）
"""

import flet as ft
from typing import Optional


def create_app(page: ft.Page):
    """建立 Flet 應用程式"""
    page.title = "台股價值投資分析系統"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1280
    page.window_height = 800

    # 狀態變數
    current_page = ft.State("home")
    recent_stocks = ft.State([])

    # 建立 UI
    page.add(
        ft.Row(
            [
                # 左側導航欄
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("台股價值投資分析", size=20, weight=ft.FontWeight.BOLD),
                            ft.Divider(),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.HOME),
                                title=ft.Text("首頁"),
                                on_click=lambda e: navigate("home"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.ANALYTICS),
                                title=ft.Text("個股分析"),
                                on_click=lambda e: navigate("stock_analysis"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.BUSINESS),
                                title=ft.Text("產業分析"),
                                on_click=lambda e: navigate("industry_analysis"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.TRENDING_UP),
                                title=ft.Text("催化劑儀表板"),
                                on_click=lambda e: navigate("catalyst"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.COMPARE),
                                title=ft.Text("多股比較"),
                                on_click=lambda e: navigate("comparison"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.PIE_CHART),
                                title=ft.Text("資產配置"),
                                on_click=lambda e: navigate("allocation"),
                            ),
                            ft.ListTile(
                                leading=ft.Icon(ft.Icons.HISTORY),
                                title=ft.Text("復盤系統"),
                                on_click=lambda e: navigate("review"),
                            ),
                            ft.Divider(),
                            ft.Text("最近查詢", size=14, weight=ft.FontWeight.BOLD),
                            # 最近查詢列表會動態更新
                        ],
                        spacing=0,
                    ),
                    width=250,
                    bgcolor=ft.Colors.SURFACE_VARIANT,
                    padding=10,
                ),
                # 右側主內容區
                ft.Container(
                    content=ft.Column(
                        [
                            # 頁面內容會根據 current_page 動態切換
                            ft.Text("歡迎使用台股價值投資分析系統", size=24),
                            ft.Text("請從左側選單選擇功能"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    expand=True,
                    padding=20,
                ),
            ],
            expand=True,
        ),
        # 底部狀態列
        ft.Container(
            content=ft.Row(
                [
                    ft.Text("資料更新時間：--"),
                    ft.Text("快取狀態：正常"),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=10,
            bgcolor=ft.Colors.SURFACE_VARIANT,
        ),
    )

    def navigate(page_name: str):
        """導航至指定頁面"""
        current_page.value = page_name
        page.update()


def home_page():
    """首頁儀表板"""
    return ft.Column(
        [
            ft.Text("首頁儀表板", size=24, weight=ft.FontWeight.BOLD),
            ft.TextField(
                label="搜尋股票代號",
                hint_text="輸入股號或公司名稱",
                prefix_icon=ft.Icons.SEARCH,
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("市場概覽", size=18, weight=ft.FontWeight.BOLD),
                            ft.Text("加權指數：--"),
                            ft.Text("成交量：--"),
                        ]
                    ),
                    padding=20,
                )
            ),
        ]
    )


def stock_analysis_page():
    """個股分析頁"""
    return ft.Column(
        [
            ft.Text("個股分析", size=24, weight=ft.FontWeight.BOLD),
            ft.TextField(
                label="股票代號",
                hint_text="例如：2330",
            ),
            ft.ElevatedButton("分析", icon=ft.Icons.SEARCH),
            # 分析結果會顯示在這裡
        ]
    )


def industry_analysis_page():
    """產業分析頁"""
    return ft.Column(
        [
            ft.Text("產業分析", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("選擇產業進行分析"),
        ]
    )


def catalyst_page():
    """催化劑儀表板頁"""
    return ft.Column(
        [
            ft.Text("催化劑儀表板", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("基本面 / 技術面 / 籌碼面訊號"),
        ]
    )


def comparison_page():
    """多股比較頁"""
    return ft.Column(
        [
            ft.Text("多股比較", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("選擇 2-10 檔股票進行比較"),
        ]
    )


def allocation_page():
    """資產配置頁"""
    return ft.Column(
        [
            ft.Text("資產配置", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("核心 / 衛星 / 避險配置建議"),
        ]
    )


def review_page():
    """復盤系統頁"""
    return ft.Column(
        [
            ft.Text("復盤系統", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("交易紀錄與績效分析"),
        ]
    )


def settings_page():
    """設定頁"""
    return ft.Column(
        [
            ft.Text("設定", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("帳號 / 資料更新 / 權重 / 備份 / 主題"),
        ]
    )
