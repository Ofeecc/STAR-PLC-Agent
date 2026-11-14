# 文档目录索引 (Documentation Index)

本目录按**当前操作与架构文档**、**设计方案与实施计划**、**冻结题库逐题审查记录**及**阶段性历史归档**组织。

## 一、 当前操作、协议与核心文档

| 文档 | 说明 |
| :--- | :--- |
| [windows_field_test_guide.md](windows_field_test_guide.md) | Windows + CODESYS 实机自检、参考 ST 验收与成对/全量实验操作指南（已合并 2026-11-13 交接预检流程） |
| [experiment_protocol.md](experiment_protocol.md) | 实验条件定义、资源预算与评测指标协议（含 2026-11-14 对齐说明） |
| [architecture.md](architecture.md) | STAR 工业 PLC 编程 Agent 核心架构设计文档 |
| [codesys_setup.md](codesys_setup.md) | Real CODESYS compiler setup on Windows |
| [compiler_screenshot.md](compiler_screenshot.md) | Remaining real IDE screenshot & compiler preflight evidence note |
| [automated_simulation.md](automated_simulation.md) | Automatic functional testing in CODESYS IDE simulation |
| [functional_testing.md](functional_testing.md) | Functional testing and CODESYS trace acquisition |
| [functional_trace_format.md](functional_trace_format.md) | Importing actual CODESYS functional observations & trace format |
| [simulation_testing.md](simulation_testing.md) | Optional automated testing in CODESYS IDE simulation |
| [ltl_semantics.md](ltl_semantics.md) | Discrete scan semantics and LTL interpretation |
| [baseline.md](baseline.md) | Historical Codex CLI / baseline compatibility setup record |
| [reproducibility.md](reproducibility.md) | Reproducing and auditing the benchmark |
| [静态分析与模型检查使用指南.md](静态分析与模型检查使用指南.md) | Static Analysis Light 与本地 NuSMV/nuXmv SMV 模型检查使用指南 |
| [historical_readme_results.md](historical_readme_results.md) | 历史 README 结果保留说明（未经同哈希原始日志复核不得作为当前结论） |

## 二、 设计规范与实施计划 (`superpowers/`)

| 文档 | 说明 |
| :--- | :--- |
| [2026-11-08-star-harness-design.md](superpowers/specs/2026-11-08-star-harness-design.md) | STAR Harness 初始设计文档 |
| [2026-11-10-star-v2-design.md](superpowers/specs/2026-11-10-star-v2-design.md) | STAR v2：PLC ST 代码生成与自动测试验证平台设计文档 |
| [2026-11-10-star-v2.md](superpowers/plans/2026-11-10-star-v2.md) | STAR v2 Implementation Plan |
| [2026-11-12-ui-smv-defects-design.md](superpowers/specs/2026-11-12-ui-smv-defects-design.md) | Web UI Alias/State Popovers, Persistent SMV Verification Status, and Audit Defect Fixes（已实现） |

## 三、 冻结题库逐题审查 (`规约逐题审查_20261106/`)

> [!NOTE]
> `dataset/*/*.json` 中的 `review_source` 字段直接引用 `docs/规约逐题审查_20261106/*.md`，因此该目录保留原路径不迁移。

- [规约逐题审查_20261106/README.md](规约逐题审查_20261106/README.md)：32 道题（`PUB001`–`PUB020`、`SELF001`–`SELF012`）初始规约审查索引、反例脚本与 `review_manifest.json`。

## 四、 阶段性报告、审计与历史日志 (`archive/`)

以下文件记录各里程碑的状态快照与审计过程（已随代码合并或被更新版本替代的细节均保留历史上下文）：

| 文档 | 说明 |
| :--- | :--- |
| [交接与实测方案_20261113.md](archive/交接与实测方案_20261113.md) | 2026-11-13 交接文档与未闭合事项清单（修复补丁已合入，Windows 预检/配对流程已并入 `windows_field_test_guide.md`） |
| [审查报告汇总_20261112.md](archive/审查报告汇总_20261112.md) | 偶数题（10 道公开题 + 6 道自建题）审查与交叉复核汇总 |
| [规约与模型全量审计汇总_20261112.md](archive/规约与模型全量审计汇总_20261112.md) | 32 题规约、参考实现与 NuSMV/nuXmv SMV 模型全量审计汇总 |
| [规约规范化_20261111.md](archive/规约规范化_20261111.md) | 规约 `2.1-normalized-20261111` 规范化与逐题定义说明 |
| [更新记录_20261111.md](archive/更新记录_20261111.md) | 2026-11-11 项目更新与验证范围记录 |
| [全题库双语审核界面_20261111.md](archive/全题库双语审核界面_20261111.md) | 全题库双语审核 WebUI 界面说明 |
| [模板库与Token配置建议_20261111.md](archive/模板库与Token配置建议_20261111.md) | 模板库检查与 SA0027 处理及分角色 Token 上限建议 |
| [双Agent两题试跑与留痕.md](archive/双Agent两题试跑与留痕.md) | PUB001 / PUB003 自研 Agent 试跑与留痕记录 |
| [六题规约中文审核.md](archive/六题规约中文审核.md) | 六题规约中文审核说明 |
| [逐拍规约检查器.md](archive/逐拍规约检查器.md) | 逐拍规约检查器与数组扩展阶段记录 |
| [本机验证与修复_20261110.md](archive/本机验证与修复_20261110.md) | 2026-11-10 本机验证与早期修复记录 |
