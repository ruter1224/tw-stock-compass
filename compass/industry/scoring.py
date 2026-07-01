"""
2026 產業站隊與選股評分表

供應鏈重組下的產業定位驗證。

評分維度：
- 政策護城河 (30%)
- 地緣韌性 (30%)
- 定價權力 (25%)
- 生產效率 (15%)

總分判讀：
- >= 8: 核心配置
- 6-7: 中性觀察
- < 5: 結構性風險
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class IndustryPosition(Enum):
    """產業定位"""
    CORE = "核心配置"
    NEUTRAL = "中性觀察"
    RISKY = "結構性風險"


@dataclass
class PositionScore:
    """產業站隊評分結果"""
    total_score: float
    position: IndustryPosition
    recommendation: str
    details: dict


class IndustryPositionScorer:
    """產業站隊評分器"""

    # 權重
    WEIGHTS = {
        "policy_moat": 0.30,
        "geopolitical_resilience": 0.30,
        "pricing_power": 0.25,
        "production_efficiency": 0.15,
    }

    @staticmethod
    def score(
        policy_moat: float,
        geopolitical_resilience: float,
        pricing_power: float,
        production_efficiency: float,
    ) -> PositionScore:
        """
        計算產業站隊評分

        Args:
            policy_moat: 政策護城河 (1-10)
            geopolitical_resilience: 地緣韌性 (1-10)
            pricing_power: 定價權力 (1-10)
            production_efficiency: 生產效率 (1-10)

        Returns:
            PositionScore
        """
        weights = IndustryPositionScorer.WEIGHTS

        total_score = (
            policy_moat * weights["policy_moat"]
            + geopolitical_resilience * weights["geopolitical_resilience"]
            + pricing_power * weights["pricing_power"]
            + production_efficiency * weights["production_efficiency"]
        )

        # 判斷定位
        if total_score >= 8:
            position = IndustryPosition.CORE
            recommendation = "長期受益產業，急跌可加碼"
        elif total_score >= 6:
            position = IndustryPosition.NEUTRAL
            recommendation = "轉型中，需追蹤 CAPEX 成效"
        else:
            position = IndustryPosition.RISKY
            recommendation = "被犧牲者，不建議因便宜而投入"

        return PositionScore(
            total_score=total_score,
            position=position,
            recommendation=recommendation,
            details={
                "policy_moat": policy_moat,
                "geopolitical_resilience": geopolitical_resilience,
                "pricing_power": pricing_power,
                "production_efficiency": production_efficiency,
            },
        )
