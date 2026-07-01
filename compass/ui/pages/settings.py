"""
設定頁

元件：
- 帳號設定
- 資料更新設定
- 權重設定
- 備份設定
- 主題設定
- 關於
"""

import flet as ft
from typing import Callable, Optional


class SettingsPage:
    """設定頁"""

    def __init__(self, on_navigate: Callable[[str], None]):
        self.on_navigate = on_navigate

    def build(self) -> ft.Control:
        """建立設定頁 UI"""
        return ft.Column(
            [
                self._build_header(),
                self._build_account_settings(),
                self._build_data_settings(),
                self._build_backup_settings(),
                self._build_theme_settings(),
                self._build_about(),
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,
        )

    def _build_header(self) -> ft.Control:
        """標頭"""
        return ft.Text("設定", size=24, weight=ft.FontWeight.BOLD)

    def _build_account_settings(self) -> ft.Control:
        """帳號設定"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("帳號設定", size=18, weight=ft.FontWeight.BOLD),
                        ft.TextField(
                            label="使用者名稱",
                            hint_text="輸入使用者名稱",
                            value="User",
                        ),
                        ft.ElevatedButton(
                            "變更密碼",
                            on_click=self._on_change_password,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_data_settings(self) -> ft.Control:
        """資料更新設定"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("資料更新", size=18, weight=ft.FontWeight.BOLD),
                        ft.Switch(
                            label="自動更新資料",
                            value=True,
                        ),
                        ft.Dropdown(
                            label="更新頻率",
                            options=[
                                ft.dropdown.Option("daily", "每日"),
                                ft.dropdown.Option("weekly", "每週"),
                                ft.dropdown.Option("monthly", "每月"),
                            ],
                            value="daily",
                        ),
                        ft.ElevatedButton(
                            "立即更新",
                            icon=ft.Icons.REFRESH,
                            on_click=self._on_manual_update,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_backup_settings(self) -> ft.Control:
        """備份設定"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("備份設定", size=18, weight=ft.FontWeight.BOLD),
                        ft.TextField(
                            label="備份路徑",
                            hint_text="選擇備份資料夾",
                            read_only=True,
                        ),
                        ft.Row(
                            [
                                ft.ElevatedButton(
                                    "選擇路徑",
                                    on_click=self._on_select_backup_path,
                                ),
                                ft.Switch(
                                    label="自動備份",
                                    value=False,
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_theme_settings(self) -> ft.Control:
        """主題設定"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("外觀設定", size=18, weight=ft.FontWeight.BOLD),
                        ft.RadioGroup(
                            content=ft.Row(
                                [
                                    ft.Radio(value="light", label="淺色主題"),
                                    ft.Radio(value="dark", label="深色主題"),
                                ]
                            ),
                            value="light",
                            on_change=self._on_theme_change,
                        ),
                    ],
                    spacing=15,
                ),
                padding=20,
            )
        )

    def _build_about(self) -> ft.Control:
        """關於"""
        return ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Text("關於", size=18, weight=ft.FontWeight.BOLD),
                        ft.Text("台股價值投資分析系統", size=14),
                        ft.Text("版本：0.1.0", size=12, color=ft.Colors.GREY_600),
                        ft.ElevatedButton(
                            "檢查更新",
                            on_click=self._on_check_update,
                        ),
                    ],
                    spacing=10,
                ),
                padding=20,
            )
        )

    def _on_change_password(self, e):
        """變更密碼"""
        # TODO: 實作密碼變更
        pass

    def _on_manual_update(self, e):
        """手動更新"""
        # TODO: 實作手動更新
        pass

    def _on_select_backup_path(self, e):
        """選擇備份路徑"""
        # TODO: 實作路徑選擇
        pass

    def _on_theme_change(self, e):
        """主題變更"""
        # TODO: 實作主題切換
        pass

    def _on_check_update(self, e):
        """檢查更新"""
        # TODO: 實作更新檢查
        pass
