"""
五大維度企業競爭力評級

維度① 產業鏈地位（話語權與統治力）
維度② 產業成長性（未來 2-3 年 CAGR）
維度③ 企業護城河（替代難度與門檻）
維度④ 財務與商業模式（賺錢的品質）
維度⑤ 風險折扣因子（越高分越安全）
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class DimensionLevel(Enum):
    """維度等級"""
    KING = "統治者（King）"
    KEY_PLAYER = "關鍵寡占（Key Player）"
    MAJOR = "供應鏈要角"
    ACCEPTER = "價格接受者"
    EXPLOSIVE = "爆發成長"
    HIGH_GROWTH = "高速成長"
    MODERATE = "溫和成長"
    STAGNANT = "停滯或衰退"
    IRREPLACEABLE = "無法替代"
    HIGH_BARRIER = "高門檻"
    MEDIUM_BARRIER = "中等門檻"
    NO_MOAT = "無護城河"
    MONEY_PRINTER = "印鈔機模式"
    QUALITY_MANUFACTURING = "優質製造"
    HARD_WORK = "辛苦錢（代工）"
    FRAGILE = "體質脆弱"
    SAFE = "極低風險（Safe）"
    CONTROLLABLE = "可控風險"
    RISKY = "高風險（Risky）"
    DANGEROUS = "極度危險"


@dataclass
class DimensionScore:
    """單一維度評分結果"""
    score: int  # 0-20
    level: DimensionLevel
    system_suggestion: Optional[int] = None  # 系統建議分數
    manual_adjustment: Optional[int] = None  # 手動調整值
    adjustment_reason: Optional[str] = None  # 調整理由
    auxiliary_info: Optional[dict] = None  # 輔助資訊


@dataclass
class FiveDimensions:
    """五大維度評分"""
    supply_chain_position: DimensionScore  # ① 產業鏈地位
    industry_growth: DimensionScore  # ② 產業成長性
    moat: DimensionScore  # ③ 企業護城河
    financial_model: DimensionScore  # ④ 財務與商業模式
    risk_discount: DimensionScore  # ⑤ 風險折扣因子

    @property
    def total_score(self) -> int:
        """計算總分"""
        return (
            self.supply_chain_position.score
            + self.industry_growth.score
            + self.moat.score
            + self.financial_model.score
            + self.risk_discount.score
        )

    def to_dict(self) -> dict:
        """轉換為字典"""
        return {
            "supply_chain_position": {
                "score": self.supply_chain_position.score,
                "level": self.supply_chain_position.level.value,
            },
            "industry_growth": {
                "score": self.industry_growth.score,
                "level": self.industry_growth.level.value,
            },
            "moat": {
                "score": self.moat.score,
                "level": self.moat.level.value,
            },
            "financial_model": {
                "score": self.financial_model.score,
                "level": self.financial_model.level.value,
            },
            "risk_discount": {
                "score": self.risk_discount.score,
                "level": self.risk_discount.level.value,
            },
            "total_score": self.total_score,
        }


def evaluate_supply_chain_position(
    market_share: float,
    pricing_power: bool,
    customer_dependency: float,
) -> DimensionScore:
    """
    評估維度① 產業鏈地位

    Args:
        market_share: 全球市佔率 (0-100)
        pricing_power: 是否有定價權
        customer_dependency: 最大客戶占比 (0-100)

    Returns:
        DimensionScore
    """
    score = 0

    # 市佔率評分 (0-8)
    if market_share >= 50:
        score += 8
    elif market_share >= 30:
        score += 6
    elif market_share >= 15:
        score += 4
    elif market_share >= 5:
        score += 2

    # 定價權評分 (0-6)
    if pricing_power:
        score += 6
    else:
        score += 2

    # 客戶集中度評分 (0-6)
    if customer_dependency <= 10:
        score += 6
    elif customer_dependency <= 25:
        score += 4
    elif customer_dependency <= 50:
        score += 2

    # 決定等級
    if score >= 16:
        level = DimensionLevel.KING
    elif score >= 11:
        level = DimensionLevel.KEY_PLAYER
    elif score >= 6:
        level = DimensionLevel.MAJOR
    else:
        level = DimensionLevel.ACCEPTER

    return DimensionScore(
        score=score,
        level=level,
        auxiliary_info={
            "market_share": market_share,
            "pricing_power": pricing_power,
            "customer_dependency": customer_dependency,
        },
    )


def evaluate_industry_growth(cagr: float) -> DimensionScore:
    """
    評估維度② 產業成長性

    Args:
        cagr: 複合成長率 (%)

    Returns:
        DimensionScore
    """
    if cagr >= 30:
        score = 20
        level = DimensionLevel.EXPLOSIVE
    elif cagr >= 20:
        score = 15
        level = DimensionLevel.HIGH_GROWTH
    elif cagr >= 10:
        score = 10
        level = DimensionLevel.MODERATE
    else:
        score = 5
        level = DimensionLevel.STAGNANT

    return DimensionScore(
        score=score,
        level=level,
        auxiliary_info={"cagr": cagr},
    )


def evaluate_moat(
    switching_cost: float,
    certification_years: float,
    patent_count: int,
) -> DimensionScore:
    """
    評估維度③ 企業護城河

    Args:
        switching_cost: 轉換成本評分 (0-10)
        certification_years: 認證年數
        patent_count: 專利數量

    Returns:
        DimensionScore
    """
    score = 0

    # 轉換成本評分 (0-10)
    score += int(switching_cost)

    # 認證時間評分 (0-5)
    if certification_years >= 2:
        score += 5
    elif certification_years >= 1:
        score += 3
    else:
        score += 1

    # 專利數量評分 (0-5)
    if patent_count >= 100:
        score += 5
    elif patent_count >= 50:
        score += 3
    elif patent_count >= 10:
        score += 2

    # 決定等級
    if score >= 16:
        level = DimensionLevel.IRREPLACEABLE
    elif score >= 11:
        level = DimensionLevel.HIGH_BARRIER
    elif score >= 6:
        level = DimensionLevel.MEDIUM_BARRIER
    else:
        level = DimensionLevel.NO_MOAT

    return DimensionScore(
        score=min(score, 20),
        level=level,
        auxiliary_info={
            "switching_cost": switching_cost,
            "certification_years": certification_years,
            "patent_count": patent_count,
        },
    )


def evaluate_financial_model(
    gross_margin: float,
    roe: float,
    free_cash_flow: float,
) -> DimensionScore:
    """
    評估維度④ 財務與商業模式

    Args:
        gross_margin: 毛利率 (%)
        roe: 股東權益報酬率 (%)
        free_cash_flow: 自由現金流 (億元)

    Returns:
        DimensionScore
    """
    score = 0

    # 毛利率評分 (0-8)
    if gross_margin >= 50:
        score += 8
    elif gross_margin >= 30:
        score += 6
    elif gross_margin >= 15:
        score += 4
    else:
        score += 2

    # ROE 評分 (0-6)
    if roe >= 20:
        score += 6
    elif roe >= 15:
        score += 4
    elif roe >= 10:
        score += 2

    # 自由現金流評分 (0-6)
    if free_cash_flow > 100:
        score += 6
    elif free_cash_flow > 50:
        score += 4
    elif free_cash_flow > 0:
        score += 2

    # 決定等級
    if score >= 16:
        level = DimensionLevel.MONEY_PRINTER
    elif score >= 11:
        level = DimensionLevel.QUALITY_MANUFACTURING
    elif score >= 6:
        level = DimensionLevel.HARD_WORK
    else:
        level = DimensionLevel.FRAGILE

    return DimensionScore(
        score=score,
        level=level,
        auxiliary_info={
            "gross_margin": gross_margin,
            "roe": roe,
            "free_cash_flow": free_cash_flow,
        },
    )


def evaluate_risk_discount(
    customer_concentration: float,
    supply_chain_risk: float,
    geopolitical_risk: float,
    leverage_ratio: float,
) -> DimensionScore:
    """
    評估維度⑤ 風險折扣因子

    Args:
        customer_concentration: 客戶集中度風險 (0-10, 越高越危險)
        supply_chain_risk: 供應鏈風險 (0-10)
        geopolitical_risk: 地緣政治風險 (0-10)
        leverage_ratio: 財務槓桿風險 (0-10)

    Returns:
        DimensionScore
    """
    # 風險越低分數越高
    avg_risk = (
        customer_concentration + supply_chain_risk + geopolitical_risk + leverage_ratio
    ) / 4

    # 反轉評分：風險越低分數越高
    score = int(20 - avg_risk * 2)
    score = max(0, min(20, score))

    # 決定等級
    if score >= 16:
        level = DimensionLevel.SAFE
    elif score >= 11:
        level = DimensionLevel.CONTROLLABLE
    elif score >= 6:
        level = DimensionLevel.RISKY
    else:
        level = DimensionLevel.DANGEROUS

    return DimensionScore(
        score=score,
        level=level,
        auxiliary_info={
            "customer_concentration": customer_concentration,
            "supply_chain_risk": supply_chain_risk,
            "geopolitical_risk": geopolitical_risk,
            "leverage_ratio": leverage_ratio,
        },
    )
