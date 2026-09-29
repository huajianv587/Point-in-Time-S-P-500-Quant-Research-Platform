from typing import Optional, Dict

from gateway.quant.service import get_quant_system


def run_agent_task(payload: Optional[Dict] = None) -> Dict:
    payload = payload or {}
    service = get_quant_system()
    return {
        "module": "strategy_agent",
        "status": "ready",
        "benchmark": service.default_benchmark,
        "payload": payload,
    }
