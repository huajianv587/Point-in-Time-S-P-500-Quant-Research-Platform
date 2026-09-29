
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    universe: list[str] = Field(default_factory=list)
    benchmark: str = "SPY"
    research_question: str = "Run the default S&P 500 multi-factor research pipeline"
    capital_base: float = 1_000_000
    horizon_days: int = 20


class BacktestRequest(BaseModel):
    strategy_name: str = "S&P 500 Multi-Factor Long-Only"
    universe: list[str] = Field(default_factory=list)
    benchmark: str = "SPY"
    capital_base: float = 1_000_000
    lookback_days: int = 126
