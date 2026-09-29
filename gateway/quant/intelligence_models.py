from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


DataTier = Literal["l1", "l2"]
RegistryGateStatus = Literal["pass", "review", "blocked"]


InfoType = Literal[
    "news",
    "filing",
    "esg_report",
    "earnings_call",
    "market_signal",
    "macro",
    "risk_event",
    "rag_evidence",
    "model_signal",
    "connector_status",
]


class InformationItem(BaseModel):
    item_id: str
    item_type: InfoType
    provider: str
    source: str
    title: str
    summary: str
    symbol: str
    company_name: str
    url: Optional[str] = None
    published_at: Optional[str] = None
    observed_at: str
    event_date: Optional[str] = None
    checksum: str
    content_hash: str
    license_note: str = "internal research use"
    freshness_score: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    quality_score: float = Field(ge=0.0, le=1.0)
    dedup_id: str
    leakage_guard: Literal["as_of_safe", "future_dated_warning", "missing_timestamp_warning"]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class EvidenceBundle(BaseModel):
    bundle_id: str
    generated_at: str
    decision_time: str
    universe: List[str] = Field(default_factory=list)
    query: str = ""
    items: List[InformationItem] = Field(default_factory=list)
    connector_status: Dict[str, Any] = Field(default_factory=dict)
    quality_summary: Dict[str, Any] = Field(default_factory=dict)
    lineage: List[str] = Field(default_factory=list)


class StructuredEvent(BaseModel):
    event_id: str
    item_id: str
    symbol: str
    company_name: str
    event_type: str
    esg_axis: Literal["E", "S", "G", "MIXED", "NONE"]
    sentiment: float = Field(ge=-1.0, le=1.0)
    controversy_severity: float = Field(ge=0.0, le=1.0)
    impact_direction: Literal["positive", "neutral", "negative"]
    impact_strength: float = Field(ge=0.0, le=1.0)
    evidence_strength: float = Field(ge=0.0, le=1.0)
    novelty_score: float = Field(ge=0.0, le=1.0)
    decay_half_life_days: int = Field(ge=1)
    observed_at: str
    leakage_guard: str
    metadata: Dict[str, Any] = Field(default_factory=dict)


class FactorCandidate(BaseModel):
    factor_id: str
    name: str
    family: str
    description: str
    horizon_days: int
    universe: List[str] = Field(default_factory=list)
    exposures: Dict[str, float] = Field(default_factory=dict)
    source_item_ids: List[str] = Field(default_factory=list)
    leakage_audit: Dict[str, Any] = Field(default_factory=dict)
    lineage: List[str] = Field(default_factory=list)


class FactorCard(BaseModel):
    factor_id: str
    name: str
    family: str
    definition: str
    status: Literal["promoted", "research_only", "low_confidence", "rejected"]
    market: str = "US"
    frequency: Literal["daily", "intraday", "hybrid"] = "daily"
    data_tier: DataTier = "l1"
    dataset_id: Optional[str] = None
    protection_status: Literal["pass", "review", "blocked"] = "review"
    registry_gate_status: RegistryGateStatus = "review"
    blocking_reasons: List[str] = Field(default_factory=list)
    universe: List[str] = Field(default_factory=list)
    horizon_days: int
    missing_rate: float = Field(ge=0.0, le=1.0)
    ic: float
    rank_ic: float
    turnover_estimate: float = Field(ge=0.0)
    transaction_cost_sensitivity: str
    stability_score: float = Field(ge=0.0, le=1.0)
    sample_count: int
    gate_results: Dict[str, Any] = Field(default_factory=dict)
    failure_modes: List[str] = Field(default_factory=list)
    lineage: List[str] = Field(default_factory=list)


class InstrumentContract(BaseModel):
    symbol: str
    market: str = "US"
    asset_class: Literal["equity"] = "equity"
    venue: str = "NASDAQ"
    currency: str = "USD"
    session_calendar: str = "XNYS"
    lot_size: int = Field(default=1, ge=1)
    timezone: str = "America/New_York"


class DatasetManifest(BaseModel):
    dataset_id: str
    generated_at: str
    market: str = "US"
    frequency: Literal["daily", "intraday", "hybrid"] = "daily"
    data_tier: DataTier = "l1"
    as_of_time: str
    universe: List[str] = Field(default_factory=list)
    instruments: List[InstrumentContract] = Field(default_factory=list)
    provider_chain: List[str] = Field(default_factory=list)
    freshness: Dict[str, Any] = Field(default_factory=dict)
    market_depth_status: Dict[str, Any] = Field(default_factory=dict)
    depth_session_ids: List[str] = Field(default_factory=list)
    provider_capabilities: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    lineage: List[str] = Field(default_factory=list)
    feature_store: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class ResearchProtectionReport(BaseModel):
    report_id: str
    generated_at: str
    dataset_id: Optional[str] = None
    decision_time: Optional[str] = None
    market: str = "US"
    frequency: Literal["daily", "intraday", "hybrid"] = "daily"
    data_tier: DataTier = "l1"
    required_data_tier: DataTier = "l1"
    protection_status: Literal["pass", "review", "blocked"] = "review"
    market_depth_status: Dict[str, Any] = Field(default_factory=dict)
    checks: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    blocking_checks: List[str] = Field(default_factory=list)
    blocking_reasons: List[str] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    lineage: List[str] = Field(default_factory=list)


class OrderBookLevel(BaseModel):
    level: int = Field(ge=1)
    price: float = Field(ge=0.0)
    size: float = Field(ge=0.0, default=0.0)
    order_count: Optional[int] = Field(default=None, ge=0)


class OrderBookSnapshot(BaseModel):
    snapshot_id: str
    symbol: str
    provider: str
    timestamp: str
    session: str = "regular"
    is_real: bool = False
    bids: List[OrderBookLevel] = Field(default_factory=list)
    asks: List[OrderBookLevel] = Field(default_factory=list)
    best_bid: float = Field(ge=0.0, default=0.0)
    best_ask: float = Field(ge=0.0, default=0.0)
    mid_price: float = Field(ge=0.0, default=0.0)
    spread_bps: float = Field(ge=0.0, default=0.0)
    total_bid_size: float = Field(ge=0.0, default=0.0)
    total_ask_size: float = Field(ge=0.0, default=0.0)
    imbalance: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)


class MarketDepthReplay(BaseModel):
    session_id: str
    generated_at: str
    symbol: str
    provider: str
    data_tier: DataTier = "l1"
    is_real_provider: bool = False
    snapshots: List[OrderBookSnapshot] = Field(default_factory=list)
    summary: Dict[str, Any] = Field(default_factory=dict)
    warnings: List[str] = Field(default_factory=list)
    lineage: List[str] = Field(default_factory=list)


class MarketDepthStatus(BaseModel):
    generated_at: str
    symbols: List[str] = Field(default_factory=list)
    selected_provider: str = "unavailable"
    configured_providers: List[str] = Field(default_factory=list)
    provider_capabilities: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    available: bool = False
    is_real_provider: bool = False
    history_ready: bool = False
    realtime_ready: bool = False
    data_tier: DataTier = "l1"
    eligibility_status: RegistryGateStatus = "review"
    blocking_reasons: List[str] = Field(default_factory=list)
    latest: List[OrderBookSnapshot] = Field(default_factory=list)
    lineage: List[str] = Field(default_factory=list)


class SweepRun(BaseModel):
    run_id: str
    generated_at: str
    strategy_name: str
    benchmark: str
    universe: List[str] = Field(default_factory=list)
    market: str = "US"
    frequency: Literal["daily", "intraday", "hybrid"] = "daily"
    data_tier: DataTier = "l1"
    dataset_id: Optional[str] = None
    protection_status: Literal["pass", "review", "blocked"] = "review"
    market_depth_status: Dict[str, Any] = Field(default_factory=dict)
    provider_capabilities: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    parameter_grid: Dict[str, List[Any]] = Field(default_factory=dict)
    combinations: List[Dict[str, Any]] = Field(default_factory=list)
    summary: Dict[str, Any] = Field(default_factory=dict)
    best_run: Dict[str, Any] = Field(default_factory=dict)
    walk_forward: Dict[str, Any] = Field(default_factory=dict)
    lineage: List[str] = Field(default_factory=list)


class TearsheetReport(BaseModel):
    report_id: str
    generated_at: str
    backtest_id: str
    strategy_name: str
    market: str = "US"
    frequency: Literal["daily", "intraday", "hybrid"] = "daily"
    data_tier: DataTier = "l1"
    protection_status: Literal["pass", "review", "blocked"] = "review"
    market_depth_status: Dict[str, Any] = Field(default_factory=dict)
    summary: Dict[str, Any] = Field(default_factory=dict)
    sections: Dict[str, Any] = Field(default_factory=dict)
    html: str
    lineage: List[str] = Field(default_factory=list)


class SimulationScenario(BaseModel):
    symbol: str = "AAPL"
    universe: List[str] = Field(default_factory=list)
    horizon_days: int = Field(default=20, ge=1, le=252)
    shock_bps: float = 0.0
    transaction_cost_bps: float = 8.0
    slippage_bps: float = 5.0
    paths: int = Field(default=256, ge=32, le=5000)
    seed: int = 42
    scenario_name: str = "base_case"
    event_assumption: str = ""
    regime: str = "neutral"
    event_id: Optional[str] = None
    evidence_run_id: Optional[str] = None
    required_data_tier: DataTier = "l1"


class SimulationResult(BaseModel):
    simulation_id: str
    generated_at: str
    scenario: SimulationScenario
    data_tier: DataTier = "l1"
    expected_return: float
    median_return: float
    probability_of_loss: float
    max_drawdown_p95: float
    value_at_risk_95: float
    expected_shortfall_95: float
    path_summary: Dict[str, float] = Field(default_factory=dict)
    factor_attribution: Dict[str, float] = Field(default_factory=dict)
    historical_analogs: List[Dict[str, Any]] = Field(default_factory=list)
    market_depth_status: Dict[str, Any] = Field(default_factory=dict)
    lineage: List[str] = Field(default_factory=list)


class DecisionReport(BaseModel):
    decision_id: str
    generated_at: str
    decision_time: str
    symbol: str
    company_name: str
    action: Literal["long", "neutral", "short"]
    position_weight_range: Dict[str, float]
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_interval: Dict[str, float]
    expected_return: float
    main_evidence: List[InformationItem] = Field(default_factory=list)
    counter_evidence: List[InformationItem] = Field(default_factory=list)
    risk_triggers: List[str] = Field(default_factory=list)
    factor_attribution: Dict[str, float] = Field(default_factory=dict)
    factor_cards: List[FactorCard] = Field(default_factory=list)
    simulation: Optional[SimulationResult] = None
    verifier_checks: Dict[str, Any] = Field(default_factory=dict)
    data_versions: Dict[str, Any] = Field(default_factory=dict)
    model_versions: Dict[str, Any] = Field(default_factory=dict)
    audit_trail: List[str] = Field(default_factory=list)


class OutcomeRecord(BaseModel):
    outcome_id: str
    decision_id: Optional[str] = None
    symbol: str
    recorded_at: str
    decision_time: Optional[str] = None
    horizon_days: int
    predicted_return: Optional[float] = None
    realized_return: float
    benchmark_return: float = 0.0
    excess_return: float
    direction_hit: Optional[bool] = None
    brier_component: Optional[float] = None
    regret: Optional[float] = None
    drawdown_breach: bool = False
    notes: str = ""
    lineage: List[str] = Field(default_factory=list)
