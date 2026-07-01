"""
台股價值投資分析系統 — 主程式入口

基於阿勳 2025/2026 投資策略展望會方法論，以「追價安全圈」為核心的本機桌面分析工具。
"""

import flet as ft

from compass.ui.app import create_app


def main():
    """啟動 Flet 應用程式"""
    ft.run(main=create_app)


if __name__ == "__main__":
    main()
