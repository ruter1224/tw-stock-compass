"""
賣出決策警示

賣出條件：
- 股價 > 長期價值（已達昂貴價區間）
- 本益比 > 30 倍
- 跌破 60 週均線 5%
"""

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ExitSignalType(Enum):
    """賣出訊號類型"""
    VALUATION = "估值過高"
    PE_HIGH = "本益比過高"
    MA_BREAK = "跌破均線"


class ExitSignalSeverity(Enum):
    """賣出訊號嚴重程度"""
    WARNING = "警告"
    STRONG_SELL = "強烈賣出"


@dataclass
class ExitSignal:
    """賣出訊號"""
    signal_type: ExitSignalType
    severity: ExitSignalSeverity
    description: str
    current_value: float
    threshold: float


@dataclass
class ExitSignalResult:
    """賣出訊號分析結果"""
    signals: list[ExitSignal]
    should_sell: bool
    summary: str


class ExitSignalAnalyzer:
    """賣出訊號分析器"""

    # 閾值
    PE_THRESHOLD = 30.0
    MA_BREAK_PERCENT = 0.05

    @staticmethod
    def analyze(
        current_price: float,
        target_price: float,
        pe_ratio: float,
        ma60: float,
    ) -> ExitSignalResult:
        """
        分析賣出訊號

        Args:
            current_price: 目前股價
            target_price: 長期目標價（合理價上限）
            pe_ratio: 目前本益比
            ma60: 60 週均線

        Returns:
            ExitSignalResult
        """
        signals = []

        # 檢查估值過高
        if current_price > target_price:
            signals.append(
                ExitSignal(
                    signal_type=ExitSignalType.VALUATION,
                    severity=ExitSignalSeverity.WARNING,
                    description=f"股價 {current_price:.0f} 已超過目標價 {target_price:.0f}",
                    current_value=current_price,
                    threshold=target_price,
                )
            )

        # 檢查本益比過高
        if pe_ratio > ExitSignalAnalyzer.PE_THRESHOLD:
            signals.append(
                ExitSignal(
                    signal_type=ExitSignalType.PE_HIGH,
                    severity=ExitSignalSeverity.STRONG_SELL,
                    description=f"本益比 {pe_ratio:.1f} 倍已超過 {ExitSignalAnalyzer.PE_THRESHOLD} 倍",
                    current_value=pe_ratio,
                    threshold=ExitSignalAnalyzer.PE_THRESHOLD,
                )
            )

        # 檢查跌破均線
        ma_threshold = ma60 * (1 - ExitSignalAnalyzer.MA_BREAK_PERCENT)
        if current_price < ma_threshold:
            signals.append(
                ExitSignal(
                    signal_type=ExitSignalType.MA_BREAK,
                    severity=ExitSignalSeverity.WARNING,
                    description=f"股價 {current_price:.0f} 跌破 60 週均線 {ma60:.0f} 的 5%",
                    current_value=current_price,
                    threshold=ma_threshold,
                )
            )

        # 判斷是否應該賣出
        should_sell = any(s.severity == ExitSignalSeverity.STRONG_SELL for s in signals)

        # 產生摘要
        if should_sell:
            summary = "建議賣出：存在強烈賣出訊號"
        elif signals:
            summary = f"注意：有 {len(signals)} 個警告訊號"
        else:
            summary = "目前無賣出訊號"

        return ExitSignalResult(
            signals=signals,
            should_sell=should_sell,
            summary=summary,
        )
