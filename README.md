# 量化交易机器人（Mac 版本）

## 项目简介
本项目是基于 Python 的数字货币量化交易机器人，针对 macOS 环境进行了优化，适合快速部署及二次开发。系统包含策略管理、风险控制、数据获取和交易执行等模块。

## 主要特性
- **跨平台兼容**：使用 Python 3，适合在 macOS 上运行。
- **多策略支持**：内置 DMR 均线交叉策略，可按需扩展。
- **自动化数据获取**：集成 Binance 测试网接口，自动拉取行情数据。
- **风险管理**：提供仓位管理与止损止盈设置。
- **日志与监控**：记录交易日志并跟踪收益表现。

## 快速开始
1. 克隆项目并进入目录：
   ```bash
   git clone https://github.com/Godcreate/DEMO_00_binance_python.git
   cd DEMO_00_binance_python
   ```
2. （可选）创建虚拟环境：
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```
4. 配置 API 密钥：
   - 在 `config/testnet_config.py` 或 `config/config.py` 中填入 Binance 提供的 `API_KEY` 和 `API_SECRET`。
5. 获取历史数据：
   ```bash
   python data/data_fetcher.py
   ```
6. 运行主程序：
   ```bash
   python main.py
   ```

## 部署步骤概览
- 使用 Python 3.9 或以上版本。
- 保证 `ccxt`, `pandas`, `numpy` 已按 `requirements.txt` 安装。
- 在运行前确保 `config` 中的密钥和参数已配置。
- 根据需要自定义策略文件并在 `main.py` 中引用。
- 查看 `trading_log.txt` 获取运行日志和收益信息。

