# Private S&P 500 Platform Direction

The product boundary is a private S&P 500 research and decision platform.
ESG is one optional factor family, alongside value, quality, momentum,
volatility, sentiment, macro, event, and alternative data.

## Data flow

```text
S&P 500 snapshot
  -> point-in-time data store
  -> fundamental / price / macro / news / optional ESG features
  -> factor discovery and leakage/cost gates
  -> portfolio construction and risk controls
  -> backtest / paper trading / review
  -> Agent explanation and research memory
```

The default universe endpoint exposes whether a complete constituent snapshot
is loaded. Export a constituent file from Capital IQ or another licensed source,
normalize it to CSV, and set `SP500_CONSTITUENTS_PATH` before claiming full
S&P 500 coverage. A small embedded catalog is only a development fallback.

For Agent integration, use the local FastAPI endpoints as the control plane:

- `GET /api/v1/quant/universe/default`
- `GET /api/v1/quant/platform/overview`
- `POST /api/v1/quant/research/run`
- `POST /api/v1/quant/factors/discover`
- `POST /api/v1/quant/backtests/run`

Capital IQ remains a licensed data source and browser research surface. The
platform should consume an explicit export or approved API response, record its
snapshot date, import time, source, and hash, and block historical backtests
when point-in-time availability cannot be established.
