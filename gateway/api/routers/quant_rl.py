from fastapi import APIRouter, HTTPException

try:
    from api.routes_quant_rl import router
except Exception as exc:  # pragma: no cover - only used in reduced installations
    _import_error = f"{type(exc).__name__}: {exc}"
    router = APIRouter(prefix="/api/v1/quant/rl", tags=["quant-rl"])

    @router.get("/overview")
    def quant_rl_unavailable() -> dict:
        raise HTTPException(status_code=503, detail=f"Quant RL service unavailable: {_import_error}")

__all__ = ["router"]
