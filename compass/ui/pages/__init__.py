"""UI 頁面模組"""

from compass.ui.pages.allocation import AllocationPage
from compass.ui.pages.catalyst import CatalystPage
from compass.ui.pages.comparison import ComparisonPage
from compass.ui.pages.home import HomePage
from compass.ui.pages.industry_analysis import IndustryAnalysisPage
from compass.ui.pages.review import ReviewPage
from compass.ui.pages.settings import SettingsPage
from compass.ui.pages.stock_analysis import StockAnalysisPage

__all__ = [
    "HomePage",
    "StockAnalysisPage",
    "IndustryAnalysisPage",
    "CatalystPage",
    "ComparisonPage",
    "AllocationPage",
    "ReviewPage",
    "SettingsPage",
]
