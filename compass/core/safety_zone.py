"""
追價安全圈計算（雙軌制）

採用雙軌並列輸出：
- 方法一：安全邊際法（葛拉漢法）
- 方法二：DCF 折現法

價位區間（三檔制）：
- 便宜價：目標價 × 70%-85%
- 合理價：目標價 × 85%-100%
- 昂貴價：目標價 × 100% 以上
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional

from compass.core.dimensions import DimensionLevel, FiveDimensions
from compass.core.target_pe import TargetPECalculator, Tier


class PriceZone(Enum):
    """價位區間"""
    CHEAP = "便宜價"
    FAIR = "合理價"
    EXPENSIVE = "昂貴價"


@dataclass
class PriceZoneRange:
    """價位區間範圍"""
    cheap_low: float
    cheap_high: float
    fair_low: float
    fair_high: float
    expensive_low: float

    @property
    def cheap_range(self) -> str:
        return f"{self.cheap_low:.0f}-{self.cheap_high:.0f} 元"

    @property
    def fair_range(self) -> str:
        return f"{self.fair_low:.0f}-{self.fair_high:.0f} 元"

    @property
    def expensive_range(self) -> str:
        return f"{self.excessive_low:.0f} 元以上"


@dataclass
class SafetyZoneResult:
    """追價安全圈計算結果"""
    method: str
    intrinsic_value: float
    discount_rate: Optional[float]
    safety_margin: Optional[float]
    price_zones: PriceZoneRange
    current_price: Optional[float] = None
    current_zone: Optional[PriceZone] = None


@dataclass
class DualTrackSafetyZone:
    """雙軌制安全圈結果"""
    margin_of_safety: SafetyZoneResult
    dcf: SafetyZoneResult
    combined_cheap_range: str
    combined_fair_range: str
    combined_expensive_range: str


class SafetyZoneCalculator:
    """追價安全圈計算器"""

    # 安全邊際比例（依風險等級）
    SAFETY_MARGIN_RATES = {
        DimensionLevel.SAFE: 0.15,  # 10%-20%
        DimensionLevel.CONTROLLABLE: 0.25,  # 20%-30%
        DimensionLevel.RISKY: 0.40,  # 30%-50%
        DimensionLevel.DANGEROUS: 0.50,  # 30%-50%
    }

    # 折現率（依企業類型）
    DISCOUNT_RATES = {
        Tier.S: 0.06,  # 5%-7%
        Tier.A: 0.07,
        Tier.B: 0.08,  # 7%-10%
        Tier.C: 0.10,
        Tier.D: 0.12,  # 10%-15%
    }

    @staticmethod
    def calculate_margin_of_safety(
        target_price: float,
        risk_level: DimensionLevel,
    ) -> SafetyZoneResult:
        """
        方法一：安全邊際法（葛拉漢法）

        Args:
            target_price: 目標價（內在價值）
            risk_level: 風險等級

        Returns:
            SafetyZoneResult
        """
        safety_margin = SafetyZoneCalculator.SAFETY_MARGIN_RATES.get(risk_level, 0.30)
        adjusted_value = target_price * (1 - safety_margin)

        # 計算價位區間
        cheap_low = adjusted_value * 0.70
        cheap_high = adjusted_value * 0.85
        fair_low = adjusted_value * 0.85
        fair_high = adjusted_value
        expensive_low = adjusted_value

        return SafetyZoneResult(
            method="安全邊際法",
            intrinsic_value=target_price,
            discount_rate=None,
            safety_margin=safety_margin,
            price_zones=PriceZoneRange(
                cheap_low=cheap_low,
                cheap_high=cheap_high,
                fair_low=fair_low,
                fair_high=fair_high,
                expensive_low=expensive_low,
            ),
        )

    @staticmethod
    def calculate_dcf(
        target_price: float,
        tier: Tier,
        years: int = 5,
    ) -> SafetyZoneResult:
        """
        方法二：DCF 折現法

        Args:
            target_price: 目標價（未來價值）
            tier: 企業評級
            years: 折現年數

        Returns:
            SafetyZoneResult
        """
        discount_rate = SafetyZoneCalculator.DISCOUNT_RATES.get(tier, 0.10)
        intrinsic_value = target_price / ((1 + discount_rate) ** years)

        # 計算價位區間
        cheap_low = intrinsic_value * 0.70
        cheap_high = intrinsic_value * 0.85
        fair_low = intrinsic_value * 0.85
        fair_high = intrinsic_value
        expensive_low = intrinsic_value

        return SafetyZoneResult(
            method="DCF 折現法",
            intrinsic_value=intrinsic_value,
            discount_rate=discount_rate,
            safety_margin=None,
            price_zones=PriceZoneRange(
                cheap_low=cheap_low,
                cheap_high=cheap_high,
                fair_low=fair_low,
                fair_high=fair_high,
                expensive_low=expensive_low,
            ),
        )

    @staticmethod
    def calculate_dual_track(
        dimensions: FiveDimensions,
        eps: float,
        current_price: Optional[float] = None,
    ) -> DualTrackSafetyZone:
        """
        雙軌制計算

        Args:
            dimensions: 五大維度評分
            eps: 每股盈餘
            current_price: 目前股價

        Returns:
            DualTrackSafetyZone
        """
        # 計算目標價
        target_pe_result = TargetPECalculator.calculate(dimensions)
        target_price = target_pe_result.pe_range.mid_pe * eps

        # 方法一：安全邊際法
        margin_result = SafetyZoneCalculator.calculate_margin_of_safety(
            target_price=target_price,
            risk_level=dimensions.risk_discount.level,
        )

        # 方法二：DCF 折現法
        dcf_result = SafetyZoneCalculator.calculate_dcf(
            target_price=target_price,
            tier=target_pe_result.tier,
        )

        # 設定目前股價位置
        if current_price:
            margin_result.current_price = current_price
            dcf_result.current_price = current_price

            # 判斷價位區間
            margin_result.current_zone = SafetyZoneCalculator._determine_zone(
                current_price, margin_result.price_zones
            )
            dcf_result.current_zone = SafetyZoneCalculator._determine_zone(
                current_price, dcf_result.price_zones
            )

        # 計算綜合區間
        combined_cheap = f"{min(margin_result.price_zones.cheap_low, dcf_result.price_zones.cheap_low):.0f}-{max(margin_result.price_zones.cheap_high, dcf_result.price_zones.cheap_high):.0f} 元"
        combined_fair = f"{min(margin_result.price_zones.fair_low, dcf_result.price_zones.fair_low):.0f}-{max(margin_result.price_zones.fair_high, dcf_result.price_zones.fair_high):.0f} 元"
        combined_expensive = f"{min(margin_result.price_zones.excessive_low, dcf_result.price_zones.excessive_low):.0f} 元以上"

        return DualTrackSafetyZone(
            margin_of_safety=margin_result,
            dcf=dcf_result,
            combined_cheap_range=combined_cheap,
            combined_fair_range=combined_fair,
            combined_expensive_range=combined_expensive,
        )

    @staticmethod
    def _determine_zone(price: float, zones: PriceZoneRange) -> PriceZone:
        """判斷目前股價所在區間"""
        if price <= zones.cheap_high:
            return PriceZone.CHEAP
        elif price <= zones.fair_high:
            return PriceZone.FAIR
        else:
            return PriceZone.EXPENSIVE
