"""
產業結構惡化程度評分表

判斷產業當前的衰退是「景氣循環」還是「結構性惡化」。

總分判讀：
- 0-3: 典型景氣循環
- 4-6: 灰色地帶
- 7-10: 結構性惡化
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DeteriorationType(Enum):
    """惡化類型"""
    CYCLICAL = "典型景氣循環"
    GRAY_ZONE = "灰色地帶"
    STRUCTURAL = "結構性惡化"


@dataclass
class DeteriorationScore:
    """產業惡化評分結果"""
    total_score: float  # 0-10
    deterioration_type: DeteriorationType
    recommendation: str
    details: dict


class IndustryDeteriorationAnalyzer:
    """產業結構惡化分析器"""

    @staticmethod
    def analyze(
        volume_trend: float,
        margin_trend: float,
        peer_profit_trend: float,
        substitution_risk: float,
        growth_story: float,
    ) -> DeteriorationScore:
        """
        分析產業結構惡化程度

        Args:
            volume_trend: 過去 5-10 年產業總量趨勢 (0-2)
            margin_trend: 價格與毛利率中樞趨勢 (0-2)
            peer_profit_trend: 同業平均獲利與 ROE 趨勢 (0-2)
            substitution_risk: 技術與需求替代風險 (0-2)
            growth_story: 下一輪成長故事 (0-2)

        Returns:
            DeteriorationScore
        """
        total_score = (
            volume_trend
            + margin_trend
            + peer_profit_trend
            + substitution_risk
            + growth_story
        )

        # 判斷類型
        if total_score <= 3:
            deterioration_type = DeteriorationType.CYCLICAL
            recommendation = "產業長期 OK，眼前是景氣或庫存調整"
        elif total_score <= 6:
            deterioration_type = DeteriorationType.GRAY_ZONE
            recommendation = "需看公司層面誰在贏、誰在輸"
        else:
            deterioration_type = DeteriorationType.STRUCTURAL
            recommendation = "視為夕陽產業，不適合長抱"

        return DeteriorationScore(
            total_score=total_score,
            deterioration_type=deterioration_type,
            recommendation=recommendation,
            details={
                "volume_trend": volume_trend,
                "margin_trend": margin_trend,
                "peer_profit_trend": peer_profit_trend,
                "substitution_risk": substitution_risk,
                "growth_story": growth_story,
            },
        )
