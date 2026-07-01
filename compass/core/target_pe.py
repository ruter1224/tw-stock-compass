"""
目標本益比定價評分表

五大維度加總後，對應評級與目標本益比區間：
- Tier S 夢幻企業: 35-40 倍
- Tier A 頂級成長: 25-30 倍
- Tier B 穩健優質: 15-20 倍
- Tier C 一般企業: 10-15 倍
- Tier D 價值陷阱: 5-10 倍
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from compass.core.dimensions import FiveDimensions


class Tier(Enum):
    """企業評級"""
    S = "Tier S 夢幻企業"
    A = "Tier A 頂級成長"
    B = "Tier B 穩健優質"
    C = "Tier C 一般企業"
    D = "Tier D 價值陷阱"


@dataclass
class TargetPERange:
    """目標本益比區間"""
    min_pe: float
    max_pe: float
    mid_pe: float

    @property
    def range_str(self) -> str:
        return f"{self.min_pe:.0f}-{self.max_pe:.0f} 倍"


@dataclass
class TargetPEResult:
    """目標 PE 計算結果"""
    tier: Tier
    pe_range: TargetPERange
    total_score: int
    description: str


# Tier 對應表
TIER_MAPPING = [
    (85, 100, Tier.S, TargetPERange(35, 40, 37.5), "幾乎無缺點，市場願意給予無限想像空間"),
    (70, 84, Tier.A, TargetPERange(25, 30, 27.5), "成長快且技術強，但有單一客戶與地緣政治風險"),
    (55, 69, Tier.B, TargetPERange(15, 20, 17.5), "好公司，但受限於代工屬性或單一客戶"),
    (40, 54, Tier.C, TargetPERange(10, 15, 12.5), "營收巨大但毛利低，常態本益比不高"),
    (0, 39, Tier.D, TargetPERange(5, 10, 7.5), "看起來便宜，但成長停滯或風險過高"),
]


class TargetPECalculator:
    """目標本益比計算器"""

    @staticmethod
    def calculate(dimensions: FiveDimensions) -> TargetPEResult:
        """
        根據五大維度總分計算目標本益比

        Args:
            dimensions: 五大維度評分

        Returns:
            TargetPEResult
        """
        total_score = dimensions.total_score

        for min_score, max_score, tier, pe_range, description in TIER_MAPPING:
            if min_score <= total_score <= max_score:
                return TargetPEResult(
                    tier=tier,
                    pe_range=pe_range,
                    total_score=total_score,
                    description=description,
                )

        # 預設回傳 Tier D
        return TargetPEResult(
            tier=Tier.D,
            pe_range=TargetPERange(5, 10, 7.5),
            total_score=total_score,
            description="看起來便宜，但成長停滯或風險過高",
        )

    @staticmethod
    def calculate_target_price(
        dimensions: FiveDimensions,
        eps: float,
        eps_source: str = "predicted_median",
    ) -> dict:
        """
        計算目標價

        Args:
            dimensions: 五大維度評分
            eps: 每股盈餘
            eps_source: EPS 來源 (predicted_median/industry_trend/ttm)

        Returns:
            包含目標價區間的字典
        """
        result = TargetPECalculator.calculate(dimensions)

        return {
            "tier": result.tier.value,
            "total_score": result.total_score,
            "pe_range": result.pe_range.range_str,
            "eps": eps,
            "eps_source": eps_source,
            "target_price_min": result.pe_range.min_pe * eps,
            "target_price_mid": result.pe_range.mid_pe * eps,
            "target_price_max": result.pe_range.max_pe * eps,
            "description": result.description,
        }
