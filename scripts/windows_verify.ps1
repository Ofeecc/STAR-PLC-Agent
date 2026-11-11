<#
.SYNOPSIS
    STAR-PLC-Agent Windows + CODESYS 一键实测验证与自检脚本
.DESCRIPTION
    针对 Windows 实测机提供一键化环境探测、编译器冒烟测试、参考模型离线仿真验证。
    执行全流程无需调用外部模型 API，零 token 开销验证 CODESYS 环境与编译/仿真管线。
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File scripts\windows_verify.ps1
#>

[CmdletBinding()]
param(
    [switch]$SkipSmoke,
    [switch]$LaunchWeb,
    [string]$Task = 'SELF001'
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $projectRoot

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " STAR-PLC-Agent Windows 实测与环境自检工具" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "项目根目录: $projectRoot" -ForegroundColor Gray

# 1. 检测 Python 与虚拟环境
Write-Host "`n[1/5] 检查 Python / uv 虚拟环境..." -ForegroundColor Yellow
$pythonExe = Join-Path $projectRoot '.venv\Scripts\python.exe'
$uvCmd = Get-Command 'uv' -ErrorAction SilentlyContinue

if (-not (Test-Path -LiteralPath $pythonExe)) {
    if ($uvCmd) {
        Write-Host "虚拟环境不存在，正在使用 uv sync 同步依赖..." -ForegroundColor Cyan
        & uv sync
    } else {
        Write-Error "未找到 .venv 虚拟环境且系统中未检测到 uv 命令。请先运行: pip install uv && uv sync"
        exit 1
    }
}

if (-not (Test-Path -LiteralPath $pythonExe)) {
    Write-Error "虚拟环境初始化失败: 未找到 $pythonExe"
    exit 1
}
Write-Host "  -> Python 解释器: $pythonExe" -ForegroundColor Green

# 2. 探测或配置 CODESYS 路径
Write-Host "`n[2/5] 探测与配置 CODESYS 运行环境..." -ForegroundColor Yellow
$taskTemp = Join-Path $projectRoot '.local_tmp'
New-Item -ItemType Directory -Path $taskTemp -Force | Out-Null
$env:TEMP = $taskTemp
$env:TMP = $taskTemp
$env:PYTHONPATH = Join-Path $projectRoot 'src'
$env:PYTHONIOENCODING = 'utf-8'

& $pythonExe -X utf8 -m plc_agent.cli configure
if ($LASTEXITCODE -ne 0) {
    Write-Warning "自动配置存在告警，请确认 configs\runtime.local.json 中的 CODESYS 路径。"
}

# 3. 运行环境体检 (doctor)
Write-Host "`n[3/5] 运行系统体检 (plc-agent doctor)..." -ForegroundColor Yellow
& $pythonExe -X utf8 -m plc_agent.cli doctor
if ($LASTEXITCODE -ne 0) {
    Write-Error "Doctor 检查失败，请根据上方输出排查缺失项。"
    exit $LASTEXITCODE
}

# 4. CODESYS 编译器冒烟验证 (Valid - Invalid - Repaired)
if (-not $SkipSmoke) {
    Write-Host "`n[4/5] 运行真实 CODESYS 编译器冒烟测试 (compiler-smoke)..." -ForegroundColor Yellow
    Write-Host "提示: 首次启动 CODESYS 编译约耗时 10-30 秒，请稍候..." -ForegroundColor Gray
    & $pythonExe -X utf8 -m plc_agent.cli compiler-smoke
    if ($LASTEXITCODE -ne 0) {
        Write-Error "真实编译冒烟测试失败，停止后续验收。"
        exit 1
    } else {
        Write-Host "  -> CODESYS 编译管线与 ScriptEngine 握手验证通过！" -ForegroundColor Green
    }
} else {
    Write-Host "`n[4/5] 跳过编译器冒烟测试 (-SkipSmoke)" -ForegroundColor Gray
}

# 5. 离线参考实现编译与仿真验证 (0 API Token)
Write-Host "`n[5/5] 运行离线参考实现仿真验证 (test-reference --task $Task --backend codesys)..." -ForegroundColor Yellow
& $pythonExe -X utf8 -m plc_agent.cli test-reference --task $Task --backend codesys
if ($LASTEXITCODE -ne 0) {
    Write-Error "真实执行测试未通过，停止验收。"
    exit 1
} else {
    Write-Host "  -> 任务 $Task 离线参考仿真全覆盖通过！" -ForegroundColor Green
}

Write-Host "`n==========================================================" -ForegroundColor Cyan
Write-Host " 实测自检完成！核心环境就绪状态良好。" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "后续建议操作:" -ForegroundColor White
Write-Host " 1. 启动可视化看板 (WebUI):" -ForegroundColor White
Write-Host "    uv run plc-agent web --port 8765" -ForegroundColor Yellow
Write-Host "    浏览器访问: http://127.0.0.1:8765" -ForegroundColor Gray
Write-Host " 2. 运行单任务真实 Agent 实验 (需配置 API Key):" -ForegroundColor White
Write-Host "    uv run plc-agent --allow-model-api run --condition E3 --task-id SELF001" -ForegroundColor Yellow
Write-Host " 3. 执行完整条件评测集:" -ForegroundColor White
Write-Host "    uv run plc-agent test --condition E3" -ForegroundColor Yellow
Write-Host "    uv run plc-agent aggregate" -ForegroundColor Yellow

if ($LaunchWeb) {
    Write-Host "`n正在启动 WebUI 看板..." -ForegroundColor Cyan
    & $pythonExe -X utf8 -m plc_agent.cli web --port 8765
}
