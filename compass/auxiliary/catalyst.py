"""
價值催化劑儀表板

催化劑類別：
- 基本面：法說會日程、高現金股利宣告、財報利多
- 技術面：60 週均線方向、週 MACD 綠柱/紅柱
- 籌碼面：大戶持股連續增減（1%-2%）、股價不漲訊號
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional
from datetime import date


class CatalystType(Enum):
    """催化劑類型"""
    FUNDAMENTAL = "基本面"
    TECHNICAL = "技術面"
    CHIPS = "籌碼面"


class CatalystStrength(Enum):
    """催化劑強度"""
    STRONG = "強烈"
    MODERATE = "中等"
    WEAK = "微弱"


@dataclass
class CatalystSignal:
    """催化劑訊號"""
    catalyst_type: CatalystType
    name: str
    description: str
    strength: CatalystStrength
    date: Optional[date] = None
    data_source: Optional[str] = None


@dataclass
class CatalystResult:
    """催化劑分析結果"""
    signals: list[CatalystSignal]
    overall_strength: CatalystStrength
    summary: str


class CatalystAnalyzer:
    """催化劑分析器"""

    @staticmethod
    def analyze_fundamental(
        investor_conference_date: Optional[date] = None,
        high_dividend_announced: bool = False,
        earnings_beat: bool = False,
    ) -> list[CatalystSignal]:
        """
        分析基本面催化劑

        Args:
            investor_conference_date: 法說會日期
            high_dividend_announced: 是否宣告高現金股利
            earnings_beat: 財報是否優於預期

        Returns:
            list of CatalystSignal
        """
        signals = []

        if investor_conference_date:
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.FUNDAMENTAL,
                    name="法說會日程",
                    description=f"法說會將於 {investor_conference_date} 舉行",
                    strength=CatalystStrength.MODERATE,
                    date=investor_conference_date,
                )
            )

        if high_dividend_announced:
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.FUNDAMENTAL,
                    name="高現金股利",
                    description="公司已宣告高現金股利",
                    strength=CatalystStrength.STRONG,
                )
            )

        if earnings_beat:
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.FUNDAMENTAL,
                    name="財報利多",
                    description="財報優於市場預期",
                    strength=CatalystStrength.STRONG,
                )
            )

        return signals

    @staticmethod
    def analyze_technical(
        ma60_trend: str,
        weekly_macd: str,
    ) -> list[CatalystSignal]:
        """
        分析技術面催化劑

        Args:
            ma60_trend: 60 週均線方向 ("up"/"down"/"flat")
            weekly_macd: 週 MACD 狀態 ("green"/"red"/"neutral")

        Returns:
            list of CatalystSignal
        """
        signals = []

        if ma60_trend == "up":
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.TECHNICAL,
                    name="60 週均線向上",
                    description="長期趨勢向上",
                    strength=CatalystStrength.STRONG,
                )
            )
        elif ma60_trend == "down":
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.TECHNICAL,
                    name="60 週均線向下",
                    description="長期趨勢向下",
                    strength=CatalystStrength.WEAK,
                )
            )

        if weekly_macd == "green":
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.TECHNICAL,
                    name="週 MACD 紅柱",
                    description="動能轉強",
                    strength=CatalystStrength.MODERATE,
                )
            )
        elif weekly_macd == "red":
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.TECHNICAL,
                    name="週 MACD 綠柱",
                    description="動能轉弱",
                    strength=CatalystStrength.WEAK,
                )
            )

        return signals

    @staticmethod
    def analyze_chips(
        major_holder_change: float,
        price_not_rising: bool,
    ) -> list[CatalystSignal]:
        """
        分析籌碼面催化劑

        Args:
            major_holder_change: 大戶持股變化 (%)
            price_not_rising: 股價不漲訊號

        Returns:
            list of CatalystSignal
        """
        signals = []

        if major_holder_change >= 2:
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.CHIPS,
                    name="大戶持續加碼",
                    description=f"大戶持股增加 {major_holder_change:.1f}%",
                    strength=CatalystStrength.STRONG,
                )
            )
        elif major_holder_change <= -2:
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.CHIPS,
                    name="大戶持續減碼",
                    description=f"大戶持股減少 {abs(major_holder_change):.1f}%",
                    strength=CatalystStrength.WEAK,
                )
            )

        if price_not_rising:
            signals.append(
                CatalystSignal(
                    catalyst_type=CatalystType.CHIPS,
                    name="股價不漲訊號",
                    description="大戶加碼但股價未漲，可能為底部吸納",
                    strength=CatalystStrength.MODERATE,
                )
            )

        return signals

    @staticmethod
    def get_overall_strength(signals: list[CatalystSignal]) -> CatalystStrength:
        """計算整體催化劑強度"""
        if not signals:
            return CatalystStrength.WEAK

        strong_count = sum(1 for s in signals if s.strength == CatalystStrength.STRONG)
        moderate_count = sum(1 for s in signals if s.strength == CatalystStrength.MODERATE)

        if strong_count >= 2:
            return CatalystStrength.STRONG
        elif strong_count + moderate_count >= 2:
            return CatalystStrength.MODERATE
        else:
            return CatalystStrength.WEAK
