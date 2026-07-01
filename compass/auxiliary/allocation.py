"""
資產配置建議

核心／衛星／避險三層架構，依年齡提供建議配比。

配置類型：
- 積極型 (20-30 歲): 核心 40%, 衛星 60%, 避險 0%
- 進取型 (30-40 歲): 核心 50%, 衛星 40%, 避險 10%
- 混合型 (40-50 歲): 核心 60%, 衛星 25%, 避險 15%
- 穩健型 (50-60 歲): 核心 60%, 衛星 20%, 避險 20%
- 保守型 (60 歲以上): 核心 50%, 衛星 10%, 避險 40%

兩岸風險情境：
- 平時（低風險）: 台股 20-30%, 海外核心 60-70%, 海外避險 10-15%
- 風險升溫（中度）: 台股 10-20%, 海外核心 50-60%, 海外避險 30-35%
- 高度緊張: 台股 0-10%, 海外核心 40-50%, 海外避險 50-55%
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class RiskProfile(Enum):
    """風險屬性"""
    AGGRESSIVE = "積極型"
    ADVENTUROUS = "進取型"
    BALANCED = "混合型"
    CONSERVATIVE = "穩健型"
    VERY_CONSERVATIVE = "保守型"


class RiskScenario(Enum):
    """風險情境"""
    LOW = "平時（低風險）"
    MEDIUM = "風險升溫（中度）"
    HIGH = "高度緊張"


@dataclass
class AllocationResult:
    """配置建議結果"""
    risk_profile: RiskProfile
    core_ratio: float
    satellite_ratio: float
    hedge_ratio: float
    scenario: RiskScenario
    tw_stock_ratio: float
    overseas_core_ratio: float
    overseas_hedge_ratio: float
    recommendation: str


class AssetAllocationAdvisor:
    """資產配置顧問"""

    # 風險屬性配置表
    RISK_PROFILE_ALLOCATION = {
        RiskProfile.AGGRESSIVE: (40, 60, 0),
        RiskProfile.ADVENTUROUS: (50, 40, 10),
        RiskProfile.BALANCED: (60, 25, 15),
        RiskProfile.CONSERVATIVE: (60, 20, 20),
        RiskProfile.VERY_CONSERVATIVE: (50, 10, 40),
    }

    # 風險情境配置表
    RISK_SCENARIO_ALLOCATION = {
        RiskScenario.LOW: (25, 65, 10),
        RiskScenario.MEDIUM: (15, 55, 30),
        RiskScenario.HIGH: (5, 45, 50),
    }

    @staticmethod
    def get_risk_profile(age: int) -> RiskProfile:
        """根據年齡取得風險屬性"""
        if age < 30:
            return RiskProfile.AGGRESSIVE
        elif age < 40:
            return RiskProfile.ADVENTUROUS
        elif age < 50:
            return RiskProfile.BALANCED
        elif age < 60:
            return RiskProfile.CONSERVATIVE
        else:
            return RiskProfile.VERY_CONSERVATIVE

    @staticmethod
    def calculate(
        age: int,
        scenario: RiskScenario = RiskScenario.LOW,
    ) -> AllocationResult:
        """
        計算資產配置建議

        Args:
            age: 使用者年齡
            scenario: 兩岸風險情境

        Returns:
            AllocationResult
        """
        risk_profile = AssetAllocationAdvisor.get_risk_profile(age)

        # 核心/衛星/避險配置
        core, satellite, hedge = AssetAllocationAdvisor.RISK_PROFILE_ALLOCATION[
            risk_profile
        ]

        # 台股/海外配置
        tw_stock, overseas_core, overseas_hedge = (
            AssetAllocationAdvisor.RISK_SCENARIO_ALLOCATION[scenario]
        )

        # 產生建議
        if scenario == RiskScenario.HIGH:
            recommendation = "建議集中美元現金、T-Bill、黃金，降低台股曝險"
        elif scenario == RiskScenario.MEDIUM:
            recommendation = "建議減碼台股，增加海外避險資產"
        else:
            recommendation = "維持正常成長型配置"

        return AllocationResult(
            risk_profile=risk_profile,
            core_ratio=core,
            satellite_ratio=satellite,
            hedge_ratio=hedge,
            scenario=scenario,
            tw_stock_ratio=tw_stock,
            overseas_core_ratio=overseas_core,
            overseas_hedge_ratio=overseas_hedge,
            recommendation=recommendation,
        )
