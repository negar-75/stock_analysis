from pydantic import BaseModel, Field
from enum import Enum
from typing import List
from datetime import date


class TrendSignal(str, Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NATURAL = "NATURAL"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class AnalysisRequest(BaseModel):
    ticker: str
    start_date: date
    end_date: date


class StockInsightResponse(BaseModel):
    trend: TrendSignal
    risk_level: RiskLevel
    summary: str = Field(..., description="short explanation of stock trend")
    key_signals: List[str] = Field(
        ..., description="Important signals that influenced the analysis"
    )
    explanation: str
    disclaimer: str
