# 🚀 快速启动指南

## 项目概览
**S&P 500 Multi-Factor Quantitative Research Platform** - 私人量化研究终端

---

## 📋 前置要求

- Python 3.9+
- Node.js 16+ (仅用于前端构建，静态文件已生成可跳过)
- Git

---

## 🎯 快速启动（5分钟）

### 步骤 1：进入项目目录
```bash
cd /Users/guohuiwen/量化平台项目/Point-in-Time-S-P-500-Quant-Research-Platform-main
```

### 步骤 2：安装 Python 依赖
```bash
# 使用 pip
pip install -r requirements.txt

# 或使用 uv (更快)
uv pip install -r requirements.txt
```

### 步骤 3：配置环境变量（可选）
```bash
cp .env.example .env
# 编辑 .env 添加 API keys（Alpaca、OpenAI 等）
# 如果没有 API keys，平台会使用 fallback 模式
```

### 步骤 4：启动后端服务
```bash
python -m uvicorn gateway.main:app --host 0.0.0.0 --port 8000
```

### 步骤 5：访问界面
打开浏览器访问：

1. **着陆页（产品介绍）**  
   http://localhost:8000/

2. **原控制台（完整功能）**  
   http://localhost:8000/app/

3. **新版高级 UI（推荐）**  
   http://localhost:8000/ui-v2.html

4. **API 文档**  
   http://localhost:8000/docs

---

## 📊 核心功能验证

### 1. 检查平台状态
```bash
curl http://localhost:8000/api/v1/quant/platform/overview | jq
```

应该返回：
```json
{
  "platform_name": "Private S&P 500 Quant Research Platform",
  "universe": "SP500",
  "members_count": 26,
  "status": "operational"
}
```

### 2. 查看默认宇宙
```bash
curl http://localhost:8000/api/v1/quant/universe/default | jq
```

### 3. 运行简单回测
访问 http://localhost:8000/app/#/backtest 或使用 API：
```bash
curl -X POST http://localhost:8000/api/v1/quant/backtests/run \
  -H "Content-Type: application/json" \
  -d '{
    "strategy_name": "momentum_cross",
    "capital_base": 1000000,
    "lookback_days": 90
  }'
```

---

## 🎨 UI 对比

### 原有界面（保留）
- **着陆页**: 深色科技风，动态 K 线背景
- **控制台**: Quant Terminal，完整功能集成

### 新版高级 UI（推荐用于演示）
- **设计风格**: GitHub 风格深色主题
- **特点**: 
  - 清晰的信息层次
  - 现代卡片式布局
  - 实时数据可视化占位
  - 响应式设计

**文件位置**: `dist/ui-v2.html`

---

## 📈 导入完整 S&P 500 成分股

### 准备 CSV 文件
CSV 应包含以下列（列名可以灵活匹配）：
```csv
symbol,company_name,sector,industry,weight
AAPL,Apple Inc.,Technology,Consumer Electronics,0.068
MSFT,Microsoft Corporation,Technology,Software,0.072
...
```

### 运行导入脚本
```bash
python scripts/import_sp500_universe.py path/to/sp500.csv --snapshot-date 2024-12-31
```

导入后会生成 `data/sp500_universe.json`，包含：
- SHA-256 校验和
- 快照日期
- 导入时间
- 成分股完整性验证

---

## 🧪 运行测试

### 快速验证
```bash
python -m pytest tests/ -v --tb=short -k "not e2e"
```

### 完整测试套件
```bash
python -m pytest tests/ -v
```

### API 集成测试
```bash
python -m pytest tests/test_api_contracts.py -v
```

---

## 🔧 常见问题

### Q1: 启动报错 "Port 8000 already in use"
```bash
# 查找占用端口的进程
lsof -i :8000

# 杀掉进程或使用其他端口
python -m uvicorn gateway.main:app --host 0.0.0.0 --port 8001
```

### Q2: 没有 Alpaca API Key 能用吗？
可以。平台会使用 yfinance 作为 fallback 数据源。部分功能（实时交易）不可用。

### Q3: 如何查看日志？
```bash
# 启动时添加日志级别
python -m uvicorn gateway.main:app --log-level debug
```

### Q4: 如何重置数据库？
```bash
rm -rf storage/quant/*.db
# 重启服务会自动重建
```

---

## 🎯 Demo 场景（面试演示）

### 场景 1：展示平台概览
1. 访问新版 UI: http://localhost:8000/ui-v2.html
2. 展示 Dashboard 页面
3. 讲解：多因子信号、组合表现、风险指标

### 场景 2：运行回测
1. 访问控制台: http://localhost:8000/app/#/backtest
2. 选择策略：Momentum Cross
3. 设置参数：资本 $1M，回测 90 天
4. 查看结果：Sharpe、回撤、累计收益

### 场景 3：查看因子分析
1. 访问 Factor Lab
2. 展示 Value、Momentum、Volatility 因子
3. 查看 IC / RankIC 验证

### 场景 4：展示 API 文档
1. 访问 http://localhost:8000/docs
2. 展示 RESTful API 设计
3. 演示实时调用

---

## 📚 核心文件说明

### 后端核心
- `gateway/main.py` - FastAPI 应用入口
- `gateway/quant/service.py` - 量化系统核心服务
- `gateway/quant/market_data.py` - 市场数据网关
- `gateway/quant/alpha_ranker.py` - Alpha 信号排序
- `gateway/quant/signals.py` - 技术信号引擎

### 前端
- `dist/index.html` - 着陆页
- `dist/app/index.html` - 控制台主页面
- `dist/ui-v2.html` - 新版高级 UI

### 配置
- `.env.example` - 环境变量模板
- `pyproject.toml` - Python 项目配置
- `requirements.txt` - 依赖列表

### 数据
- `data/sp500_universe.json` - 成分股快照（需导入）
- `storage/quant/` - SQLite 缓存和回测结果

---

## 🚀 下一步

1. ✅ 启动平台，验证核心功能
2. 📸 截图新 UI 界面
3. 📝 根据 RESUME_DESCRIPTION.md 更新简历
4. 🎤 准备面试问题回答

---

## 💡 提示

- **演示时强调架构**：模块化设计、可插拔数据源、时点完整性
- **诚实说明限制**：研究原型，部分成分股，非生产系统
- **展示学习能力**：量化金融、多因子模型、系统设计

---

## 📞 支持

- 文档: `README.md`
- 优化报告: `OPTIMIZATION_REPORT.md`
- 简历描述: `RESUME_DESCRIPTION.md`
- API 文档: http://localhost:8000/docs

**祝求职顺利！** 🎉
