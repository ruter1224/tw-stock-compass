"""
風險儀表板

風險維度：
- 政治風險：兩岸關係、地緣政治、制裁/出口管制
- 總經風險：利率、匯率、通膨、景氣循環位置
- 產經風險：產業結構變化、技術顛覆、供應鏈移轉
- 公司風險：財務體質惡化

風險回饋閉環：
第四層的綜合風險評級 → 調整第二層維度⑤「風險折扣因子」的分數 →
影響安全邊際大小與目標本益比打折與否。
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskLevel(Enum):
    """風險等級"""
    LOW = "低風險"
    MEDIUM = "中度風險"
    HIGH = "高度風險"


class RiskCategory(Enum):
    """風險類別"""
    POLITICAL = "政治風險"
    MACRO = "總經風險"
    INDUSTRY = "產經風險"
    COMPANY = "公司風險"


@dataclass
class RiskScore:
    """單一風險評分"""
    category: RiskCategory
    score: float  # 0-10
    level: RiskLevel
    description: str


@dataclass
class RiskDashboardResult:
    """風險儀表板結果"""
    political_risk: RiskScore
    macro_risk: RiskScore
    industry_risk: RiskScore
    company_risk: RiskScore
    overall_risk: RiskLevel
    risk_discount_factor: float  # 回饋到 Layer 2 的風險折扣因子


class RiskDashboard:
    """風險儀表板"""

    @staticmethod
    def calculate_risk_level(score: float) -> RiskLevel:
        """計算風險等級"""
        if score <= 3:
            return RiskLevel.LOW
        elif score <= 6:
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.HIGH

    @staticmethod
    def analyze(
        political_score: float,
        macro_score: float,
        industry_score: float,
        company_score: float,
    ) -> RiskDashboardResult:
        """
        分析風險儀表板

        Args:
            political_score: 政治風險評分 (0-10)
            macro_score: 總經風險評分 (0-10)
            industry_score: 產經風險評分 (0-10)
            company_score: 公司風險評分 (0-10)

        Returns:
            RiskDashboardResult
        """
        # 計算各風險等級
        political_level = RiskDashboard.calculate_risk_level(political_score)
        macro_level = RiskDashboard.calculate_risk_level(macro_score)
        industry_level = RiskDashboard.calculate_risk_level(industry_score)
        company_level = RiskDashboard.calculate_risk_level(company_score)

        # 計算整體風險
        overall_score = (political_score + macro_score + industry_score + company_score) / 4
        overall_level = RiskDashboard.calculate_risk_level(overall_score)

        # 計算風險折扣因子（回饋到 Layer 2）
        # 風險越高，折扣因子越低
        risk_discount_factor = 1.0 - (overall_score / 20)

        return RiskDashboardResult(
            political_risk=RiskScore(
                category=RiskCategory.POLITICAL,
                score=political_score,
                level=political_level,
                description="兩岸關係、地緣政治、制裁/出口管制",
            ),
            macro_risk=RiskScore(
                category=RiskCategory.MACRO,
                score=macro_score,
                level=macro_level,
                description="利率、匯率、通膨、景氣循環位置",
            ),
            industry_risk=RiskScore(
                category=RiskCategory.INDUSTRY,
                score=industry_score,
                level=industry_level,
                description="產業結構變化、技術顛覆、供應鏈移轉",
            ),
            company_risk=RiskScore(
                category=RiskCategory.COMPANY,
                score=company_score,
                level=company_level,
                description="財務體質惡化",
            ),
            overall_risk=overall_level,
            risk_discount_factor=risk_discount_factor,
        )
