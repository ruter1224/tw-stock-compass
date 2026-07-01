"""
五大維度評分測試
"""

import pytest
from compass.core.dimensions import (
    FiveDimensions,
    DimensionScore,
    DimensionLevel,
    evaluate_supply_chain_position,
    evaluate_industry_growth,
    evaluate_moat,
    evaluate_financial_model,
    evaluate_risk_discount,
)


class TestEvaluateSupplyChainPosition:
    """測試維度① 產業鏈地位"""

    def test_king_level(self):
        """統治者等級"""
        result = evaluate_supply_chain_position(
            market_share=60,
            pricing_power=True,
            customer_dependency=5,
        )
        assert result.score >= 16
        assert result.level == DimensionLevel.KING

    def test_key_player_level(self):
        """關鍵寡占等級"""
        result = evaluate_supply_chain_position(
            market_share=25,
            pricing_power=True,
            customer_dependency=30,
        )
        assert 11 <= result.score <= 15

    def test_accepter_level(self):
        """價格接受者等級"""
        result = evaluate_supply_chain_position(
            market_share=3,
            pricing_power=False,
            customer_dependency=70,
        )
        assert result.score < 6
        assert result.level == DimensionLevel.ACCEPTER


class TestEvaluateIndustryGrowth:
    """測試維度② 產業成長性"""

    def test_explosive_growth(self):
        """爆發成長"""
        result = evaluate_industry_growth(cagr=35)
        assert result.score == 20
        assert result.level == DimensionLevel.EXPLOSIVE

    def test_high_growth(self):
        """高速成長"""
        result = evaluate_industry_growth(cagr=25)
        assert result.score == 15
        assert result.level == DimensionLevel.HIGH_GROWTH

    def test_moderate_growth(self):
        """溫和成長"""
        result = evaluate_industry_growth(cagr=15)
        assert result.score == 10
        assert result.level == DimensionLevel.MODERATE

    def test_stagnant(self):
        """停滯或衰退"""
        result = evaluate_industry_growth(cagr=5)
        assert result.score == 5
        assert result.level == DimensionLevel.STAGNANT


class TestEvaluateMoat:
    """測試維度③ 企業護城河"""

    def test_irreplaceable(self):
        """無法替代"""
        result = evaluate_moat(
            switching_cost=9,
            certification_years=3,
            patent_count=150,
        )
        assert result.score >= 16
        assert result.level == DimensionLevel.IRREPLACEABLE

    def test_no_moat(self):
        """無護城河"""
        result = evaluate_moat(
            switching_cost=1,
            certification_years=0,
            patent_count=0,
        )
        assert result.score < 6
        assert result.level == DimensionLevel.NO_MOAT


class TestEvaluateFinancialModel:
    """測試維度④ 財務與商業模式"""

    def test_money_printer(self):
        """印鈔機模式"""
        result = evaluate_financial_model(
            gross_margin=55,
            roe=25,
            free_cash_flow=150,
        )
        assert result.score >= 16
        assert result.level == DimensionLevel.MONEY_PRINTER

    def test_fragile(self):
        """體質脆弱"""
        result = evaluate_financial_model(
            gross_margin=8,
            roe=5,
            free_cash_flow=-50,
        )
        assert result.score < 6
        assert result.level == DimensionLevel.FRAGILE


class TestEvaluateRiskDiscount:
    """測試維度⑤ 風險折扣因子"""

    def test_safe(self):
        """極低風險"""
        result = evaluate_risk_discount(
            customer_concentration=2,
            supply_chain_risk=1,
            geopolitical_risk=2,
            leverage_ratio=1,
        )
        assert result.score >= 16
        assert result.level == DimensionLevel.SAFE

    def test_dangerous(self):
        """極度危險"""
        result = evaluate_risk_discount(
            customer_concentration=9,
            supply_chain_risk=8,
            geopolitical_risk=9,
            leverage_ratio=8,
        )
        assert result.score < 6
        assert result.level == DimensionLevel.DANGEROUS


class TestFiveDimensions:
    """測試五大維度總分"""

    def test_total_score(self):
        """總分計算"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=18, level=DimensionLevel.KING),
            industry_growth=DimensionScore(score=15, level=DimensionLevel.HIGH_GROWTH),
            moat=DimensionScore(score=16, level=DimensionLevel.IRREPLACEABLE),
            financial_model=DimensionScore(score=14, level=DimensionLevel.QUALITY_MANUFACTURING),
            risk_discount=DimensionScore(score=17, level=DimensionLevel.SAFE),
        )
        assert dimensions.total_score == 80

    def test_to_dict(self):
        """轉換為字典"""
        dimensions = FiveDimensions(
            supply_chain_position=DimensionScore(score=18, level=DimensionLevel.KING),
            industry_growth=DimensionScore(score=15, level=DimensionLevel.HIGH_GROWTH),
            moat=DimensionScore(score=16, level=DimensionLevel.IRREPLACEABLE),
            financial_model=DimensionScore(score=14, level=DimensionLevel.QUALITY_MANUFACTURING),
            risk_discount=DimensionScore(score=17, level=DimensionLevel.SAFE),
        )
        result = dimensions.to_dict()
        assert result["total_score"] == 80
        assert result["supply_chain_position"]["score"] == 18
