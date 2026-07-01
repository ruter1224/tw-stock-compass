"""
目標 PE 定價測試
"""

import pytest
from compass.core.dimensions import (
    FiveDimensions,
    DimensionScore,
    DimensionLevel,
)
from compass.core.target_pe import TargetPECalculator, Tier


class TestTargetPECalculator:
    """測試目標 PE 計算"""

    def test_tier_s(self):
        """Tier S 夢幻企業"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=20, level=DimensionLevel.KING),
            industry_growth=DimensionScore(score=20, level=DimensionLevel.EXPLOSIVE),
            moat=DimensionScore(score=20, level=DimensionLevel.IRREPLACEABLE),
            financial_model=DimensionScore(score=20, level=DimensionLevel.MONEY_PRINTER),
            risk_discount=DimensionScore(score=20, level=DimensionLevel.SAFE),
        )
        result = TargetPECalculator.calculate(dimensions)
        assert result.tier == Tier.S
        assert result.pe_range.min_pe == 35
        assert result.pe_range.max_pe == 40

    def test_tier_a(self):
        """Tier A 頂級成長"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=18, level=DimensionLevel.KING),
            industry_growth=DimensionScore(score=15, level=DimensionLevel.HIGH_GROWTH),
            moat=DimensionScore(score=16, level=DimensionLevel.IRREPLACEABLE),
            financial_model=DimensionScore(score=15, level=DimensionLevel.QUALITY_MANUFACTURING),
            risk_discount=DimensionScore(score=16, level=DimensionLevel.SAFE),
        )
        result = TargetPECalculator.calculate(dimensions)
        assert result.tier == Tier.A
        assert result.pe_range.min_pe == 25
        assert result.pe_range.max_pe == 30

    def test_tier_b(self):
        """Tier B 穩健優質"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=12, level=DimensionLevel.KEY_PLAYER),
            industry_growth=DimensionScore(score=12, level=DimensionLevel.HIGH_GROWTH),
            moat=DimensionScore(score=12, level=DimensionLevel.HIGH_BARRIER),
            financial_model=DimensionScore(score=12, level=DimensionLevel.QUALITY_MANUFACTURING),
            risk_discount=DimensionScore(score=12, level=DimensionLevel.CONTROLLABLE),
        )
        result = TargetPECalculator.calculate(dimensions)
        assert result.tier == Tier.B
        assert result.pe_range.min_pe == 15
        assert result.pe_range.max_pe == 20

    def test_tier_c(self):
        """Tier C 一般企業"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=8, level=DimensionLevel.MAJOR),
            industry_growth=DimensionScore(score=8, level=DimensionLevel.MODERATE),
            moat=DimensionScore(score=8, level=DimensionLevel.MEDIUM_BARRIER),
            financial_model=DimensionScore(score=8, level=DimensionLevel.HARD_WORK),
            risk_discount=DimensionScore(score=8, level=DimensionLevel.CONTROLLABLE),
        )
        result = TargetPECalculator.calculate(dimensions)
        assert result.tier == Tier.C
        assert result.pe_range.min_pe == 10
        assert result.pe_range.max_pe == 15

    def test_tier_d(self):
        """Tier D 價值陷阱"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=4, level=DimensionLevel.ACCEPTER),
            industry_growth=DimensionScore(score=4, level=DimensionLevel.STAGNANT),
            moat=DimensionScore(score=4, level=DimensionLevel.NO_MOAT),
            financial_model=DimensionScore(score=4, level=DimensionLevel.FRAGILE),
            risk_discount=DimensionScore(score=4, level=DimensionLevel.DANGEROUS),
        )
        result = TargetPECalculator.calculate(dimensions)
        assert result.tier == Tier.D
        assert result.pe_range.min_pe == 5
        assert result.pe_range.max_pe == 10

    def test_calculate_target_price(self):
        """計算目標價"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=18, level=DimensionLevel.KING),
            industry_growth=DimensionScore(score=15, level=DimensionLevel.HIGH_GROWTH),
            moat=DimensionScore(score=16, level=DimensionLevel.IRREPLACEABLE),
            financial_model=DimensionScore(score=15, level=DimensionLevel.QUALITY_MANUFACTURING),
            risk_discount=DimensionScore(score=16, level=DimensionLevel.SAFE),
        )
        result = TargetPECalculator.calculate_target_price(dimensions, eps=30)
        assert result["eps"] == 30
        assert result["target_price_min"] == 25 * 30
        assert result["target_price_max"] == 30 * 30
