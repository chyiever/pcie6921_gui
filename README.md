# PCIe-6921 eDAS 上位机

本项目使用 Python、PyQt5、NumPy 与厂家 `pcie6921_api.dll` 实现 PCIe-6921 采集卡上位机。项目复用 PCIe-7821 上位机已经验证的 GUI、采集线程、最新显示快照、异步写盘、频谱、Time-Space 与 TCP 通信架构，并将板卡差异集中在 `config.py`、`pcie6921_api.py` 和主窗口设备配置流程中。

## 运行环境

- Windows 64 位
- 64 位 Python 3.9 或兼容版本
- 已正确安装 PCIe-6921 驱动
- `libs/pcie6921_api.dll`，当前文件来自 `E:\codes\PCIe-6921\windows_Issue\dll\x64\pcie6921_api.dll`

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

无卡仿真启动：

```powershell
python run.py --simulate
```

带卡启动：

```powershell
python run.py
```

## 模块结构

- `src/config.py`：6921 参数模型、枚举、校验规则和空间距离计算。
- `src/pcie6921_api.py`：DLL 查找、ctypes 原型、4 KB 对齐 DMA 缓冲、线程安全调用和数据类型转换。
- `src/acquisition_thread.py`：缓冲查询、批量读取、完整数据块分发和最新显示快照。
- `src/main_window.py`：GUI、参数编排、设备启停、显示、保存、TCP 与自动恢复。
- `src/data_saver.py`：非阻塞队列与后台二进制写盘。
- `src/time_space_plot.py`、`src/spectrum_analyzer.py`：实时显示与频谱分析。
- `src/tcp_tab3/`：单通道 Phase 数据的后台 TCP 发送链路。
- `tests/`：不依赖采集卡的参数规则和 DMA 对齐测试。

## 6921 关键约束

- 时钟源编码为 `0=外部`、`1=内部`。
- DLL 未提供触发方向接口，GUI 中触发方向固定为输出说明状态。
- Raw 模式固定使用双 ADC 通道。
- 解调通道数只允许 `1` 或 `2`。
- 上传速率只允许 `1~5`，对应 `250M/125M/83.33M/62.5M/50M`。
- Phase 输入速率与上传速率统一，不存在独立 `rate2phase` 硬件参数。
- Phase 差分阶数限制为 `1~8`。
- 脉冲宽度必须为 `4 ns` 的整数倍。

空间点距为：

$$
\Delta x = d(upload\_rate) \times space\_merge\_point\_num
$$

其中 $d(upload\_rate) \in \{0.4, 0.8, 1.2, 1.6, 2.0\}\ \mathrm{m}$。

## 验证

```powershell
python -m unittest discover -s tests -v
```

带卡联调必须按 `open -> config -> start -> query -> read -> stop -> close` 顺序执行，并重点核对 Raw 交织顺序、Phase/Monitor 实际返回点数、长时间运行缓冲积压和磁盘吞吐。
