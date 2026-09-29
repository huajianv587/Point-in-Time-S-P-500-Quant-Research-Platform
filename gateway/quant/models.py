from __future__ import annotations

from typing import Any, Dict, List, Optional, Literal, Union

from pydantic import BaseModel, Field


class ArchitectureLayerStatus(BaseModel):
    key: str
    label: str
    priority: str
    ready: bool
    detail: str


class UniverseMember(BaseModel):
    symbol: str
    company_name: str
    sector: str
    industry: str
    region: str = "US"
    benchmark_weight: float = 0.0


class FactorScore(BaseModel):
    name: str
    value: float
    contribution: float
    description: str


class ProjectionScenario(BaseModel):
    label: str
    expected_return: float
    confidence: Optional[float] = None
    band_source: Optional[str] = None


class ResearchSignal(BaseModel):
    symbol: str
    company_name: str
    sector: str
    thesis: str
    action: Literal["long", "neutral", "short"]
    confidence: float
    expected_return: float
    risk_score: float
    overall_score: float
    e_score: float
    s_score: float
    g_score: float
    alpha_model_score: Optional[float] = None
    alpha_model_name: Optional[str] = None
    alpha_rank: Optional[int] = None
    predicted_return_1d: Optional[float] = None
    predicted_return_5d: Optional[float] = None
    sequence_return_1d: Optional[float] = None
    sequence_return_5d: Optional[float] = None
    sequence_volatility_10d: Optional[float] = None
    sequence_drawdown_20d: Optional[float] = None
    predicted_volatility_10d: Optional[float] = None
    predicted_drawdown_20d: Optional[float] = None
    sequence_model_version: Optional[str] = None
    regime_label: Optional[str] = None
    regime_probability: Optional[float] = None
    p1_calibrated_probability: Optional[float] = None
    p1_confidence_calibrated: Optional[float] = None
    fundamental_score: Optional[float] = None
    news_sentiment_score: Optional[float] = None
    p1_stack_score: Optional[float] = None
    p1_model_version: Optional[str] = None
    graph_cluster: Optional[str] = None
    graph_neighbors: List[str] = Field(default_factory=list)
    graph_centrality: Optional[float] = None
    graph_contagion_risk: Optional[float] = None
    graph_diversification_score: Optional[float] = None
    graph_engine: Optional[str] = None
    graph_model_version: Optional[str] = None
    selector_strategy: Optional[str] = None
    selector_priority_score: Optional[float] = None
    bandit_strategy: Optional[str] = None
    bandit_confidence: Optional[float] = None
    bandit_size_multiplier: Optional[float] = None
    bandit_execution_style: Optional[str] = None
    bandit_execution_delay_seconds: Optional[int] = None
    alpha_engine: Optional[str] = None
    decision_score: Optional[float] = None
    decision_confidence: Optional[float] = None
    signal_source: str = "heuristic"
    factor_scores: List[FactorScore] = Field(default_factory=list)
    catalysts: List[str] = Field(default_factory=list)
    data_lineage: List[str] = Field(default_factory=list)
    lineage: List[str] = Field(default_factory=list)
    dataset_id: Optional[str] = None
    protection_status: Literal["pass", "review", "blocked"] = "review"
    frequency: Literal["daily", "intraday", "hybrid"] = "daily"
    data_tier: Literal["l1", "l2"] = "l1"
    registry_gate_status: Literal["pass", "review", "blocked"] = "review"
    blocking_reasons: List[str] = Field(default_factory=list)
    market: str = "US"
    market_data_source: Optional[str] = None
    prediction_mode: Optional[Literal["model", "unavailable"]] = None
    projection_basis_return: Optional[float] = None
    projection_scenarios: Dict[str, ProjectionScenario] = Field(default_factory=dict)
    house_score: Optional[float] = None
    house_grade: Optional[str] = None
    formula_version: Optional[str] = None
    pillar_breakdown: Dict[str, float] = Field(default_factory=dict)
    disclosure_confidence: Optional[float] = None
    controversy_penalty: Optional[float] = None
    data_gap_penalty: Optional[float] = None
    materiality_adjustment: Optional[float] = None
    trend_bonus: Optional[float] = None
    house_explanation: Optional[str] = None
    house_score_v2: Optional[float] = None
    materiality_weights: Dict[str, float] = Field(default_factory=dict)
    evidence_count: Optional[int] = None
    effective_date: Optional[str] = None
    staleness_days: Optional[int] = None
    score_delta: Optional[float] = None


class PortfolioPosition(BaseModel):
    symbol: str
    company_name: str
    weight: float
    expected_return: float
    risk_budget: float
    score: float
    side: Literal["long", "short"]
    thesis: str
    strategy_bucket: Optional[str] = None
    decision_score: Optional[float] = None
    regime_posture: Optional[str] = None
    size_multiplier: Optional[float] = None
    execution_tactic: Optional[str] = None
    execution_delay_seconds: Optional[int] = None
    expected_fill_probability: Optional[float] = None
    estimated_slippage_bps: Optional[float] = None
    estimated_impact_bps: Optional[float] = None
    alpha_engine: Optional[str] = None


class PortfolioSummary(BaseModel):
    strategy_name: str
    benchmark: str
    capital_base: float
    gross_exposure: float
    net_exposure: float
    turnover_estimate: float
    expected_alpha: float
    positions: List[PortfolioPosition] = Field(default_factory=list)
    constraints: Dict[str, Union[float, str]] = Field(default_factory=dict)


class BacktestPoint(BaseModel):
    date: str
    portfolio_nav: float
    benchmark_nav: float
    drawdown: float
    gross_exposure: float


class RiskAlert(BaseModel):
    level: Literal["low", "medium", "high"]
    title: str
    description: str
    recommendation: str


class BacktestMetrics(BaseModel):
    cumulative_return: float
    annualized_return: float
    annualized_volatility: float
    sharpe: float
    sortino: float
    max_drawdown: float
    hit_rate: float
    cvar_95: float
    beta: float
    information_ratio: float


class BacktestResult(BaseModel):
    backtest_id: str
    strategy_name: str
    benchmark: str
    period_start: str
    period_end: str
    metrics: BacktestMetrics
    positions: List[PortfolioPosition] = Field(default_factory=list)
    timeline: List[BacktestPoint] = Field(default_factory=list)
    risk_alerts: List[RiskAlert] = Field(default_factory=list)
    experiment_tags: List[str] = Field(default_factory=list)
    data_source: str = "synthetic fallback"
    data_source_chain: List[str] = Field(default_factory=list)
    used_synthetic_fallback: bool = True
    market_data_warnings: List[str] = Field(default_factory=list)


class ExecutionOrder(BaseModel):
    symbol: str
    side: Literal["buy", "sell"]
    quantity: int
    target_weight: float
    limit_price: float
    venue: str
    rationale: str
    order_type: str = "market"
    time_in_force: str = "day"
    notional: Optional[float] = None
    status: str = "planned"
    broker_order_id: Optional[str] = None
    client_order_id: Optional[str] = None
    submitted_at: Optional[str] = None
    filled_qty: Optional[str] = None
    filled_avg_price: Optional[str] = None
    expected_fill_probability: Optional[float] = None
    estimated_slippage_bps: Optional[float] = None
    estimated_impact_bps: Optional[float] = None
    execution_tactic: Optional[str] = None
    execution_delay_seconds: Optional[int] = None
    canary_bucket: Optional[str] = None


class ExecutionPlan(BaseModel):
    execution_id: str
    broker: str
    mode: Literal["paper", "live"]
    ready: bool
    estimated_slippage_bps: float
    compliance_checks: List[str] = Field(default_factory=list)
    orders: List[ExecutionOrder] = Field(default_factory=list)
    submitted: bool = False
    broker_status: str = "planned"
    warnings: List[str] = Field(default_factory=list)
    account_snapshot: Dict[str, Union[str, bool, None]] = Field(default_factory=dict)
    broker_connection: Dict[str, Union[str, bool, None]] = Field(default_factory=dict)


class BrokerDescriptor(BaseModel):
    broker_id: str
    label: str
    channel: str
    configured: bool
    live_supported: bool
    paper_supported: bool
    capabilities: List[str] = Field(default_factory=list)
    auth_hints: List[str] = Field(default_factory=list)
    metadata: Dict[str, Union[str, bool, None]] = Field(default_factory=dict)


class OrderLifecycleEvent(BaseModel):
    event_id: str
    order_id: str
    execution_id: str
    broker_id: str
    state: str
    message: str
    created_at: str
    payload: dict[str, Any] = Field(default_factory=dict)


class OrderLifecycleRecord(BaseModel):
    order_id: str
    execution_id: str
    broker_id: str
    symbol: str
    current_state: str
    retry_count: int = 0
    cancel_requested: bool = False
    submitted_payload: Dict[str, Any] = Field(default_factory=dict)
    last_broker_snapshot: Dict[str, Any] = Field(default_factory=dict)
    events: List[OrderLifecycleEvent] = Field(default_factory=list)


class ExecutionJournal(BaseModel):
    execution_id: str
    broker_id: str
    mode: str
    current_state: str
    created_at: str
    updated_at: str
    allowed_actions: List[str] = Field(default_factory=list)
    risk_summary: List[str] = Field(default_factory=list)
    records: List[OrderLifecycleRecord] = Field(default_factory=list)
    metrics: Dict[str, Union[str, float, bool, None]] = Field(default_factory=dict)


class ValidationWindow(BaseModel):
    label: str
    start: str
    end: str
    sharpe: float
    cumulative_return: float
    turnover_cost_drag: float
    max_drawdown: float
    bucket: Optional[str] = None
    fill_probability: Optional[float] = None
    expected_slippage_bps: Optional[float] = None
    calibrated_confidence: Optional[float] = None


class AlphaValidationReport(BaseModel):
    validation_id: str
    strategy_name: str
    benchmark: str
    generated_at: str
    universe: List[str] = Field(default_factory=list)
    in_sample_sharpe: float
    out_of_sample_sharpe: float
    out_of_sample_cumulative_return: float
    overfit_score: float
    robustness_score: float
    turnover_cost_drag_bps: float
    slippage_bps: float
    impact_cost_bps: float
    fill_probability: float = 0.0
    walk_forward_windows: List[ValidationWindow] = Field(default_factory=list)
    stratified_walk_forward: List[Dict[str, Any]] = Field(default_factory=list)
    calibration: Dict[str, Any] = Field(default_factory=dict)
    notes: List[str] = Field(default_factory=list)


class ExperimentRun(BaseModel):
    experiment_id: str
    name: str
    created_at: str
    objective: str
    benchmark: str
    metrics: Dict[str, Union[float, str]]
    tags: List[str] = Field(default_factory=list)
    artifact_uri: Optional[str] = None


class TrainingPlan(BaseModel):
    target_environment: str
    adapter_strategy: str
    dataset_sources: List[str]
    artifact_store: str
    remote_ready: bool
    notes: List[str]
