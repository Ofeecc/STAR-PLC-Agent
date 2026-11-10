# Real CODESYS compiler setup on Windows

The external Python process orchestrates CODESYS; ST is compiled by the installed CODESYS application. The Python reference controllers cannot establish CODESYS compilation or PLC runtime correctness. This document describes a documented integration path. Installation, profile selection, and all three compiler fixtures must be verified on the actual machine before benchmark compilation rates are reported.

## Installation on D drive

Download **CODESYS Development System 3, 64 bit** from the [official Store](https://store.codesys.com/en/codesys.html). The Store requires a registered account for downloads. During this project the user is handling the installer. Choose a D-drive installation location, for example `D:\CODESYS`, when the installer allows it. Keep the CODESYS Scripting component. A separately installed Scripting add-on may be needed if the selected installation excludes it; use the CODESYS Installer to add it to the same IDE instance. Preserve the installed compiler, Standard library, and Control Win device descriptions. The normal Development System compilation task does not require purchasing an optional test manager.

Record the actual installer version and destination. Do not infer the installed version from the Store's current-version label. Do not start or download to physical PLC equipment. The compilation backend opens only an isolated project copy.

## Find executable and exact profile

The executable is normally below the selected installation's `CODESYS\Common` directory. Search the actual installation folder, then record its file version and shortcut command line. For example, after substituting the real D-drive installation root:

```powershell
Get-ChildItem -LiteralPath 'D:\CODESYS' -Filter CODESYS.exe -File -Recurse |
    Select-Object FullName,@{Name='Version';Expression={$_.VersionInfo.FileVersion}}
Get-ChildItem -LiteralPath 'D:\CODESYS' -Filter *.profile -File -Recurse |
    Select-Object FullName
```

Use the exact `--profile` value from the installed shortcut or profile selection; an illustrative `CODESYS V3.5 SP22` is not evidence that this profile is installed. When multiple installations share a profile name, the [official command-line documentation](https://content.helpme-codesys.com/en/CODESYS%20Development%20System/_cds_commandline.html) specifies `--additionalfolder` to select the intended instance. Keep that same selection for every experiment.

Set these process-level variables in a PowerShell terminal. Values below are placeholders to replace, not verified paths:

```powershell
$env:PLC_CODESYS_EXE = 'D:\ACTUAL_INSTALL\CODESYS\Common\CODESYS.exe'
$env:PLC_CODESYS_PROFILE = 'EXACT INSTALLED PROFILE'
$env:PLC_CODESYS_TEMPLATE = Join-Path (Get-Location) 'codesys\templates\benchmark.project'
$env:PYTHONPATH = (Resolve-Path '.\src').Path
# Only when this installation needs it:
# $env:PLC_CODESYS_ADDITIONAL_FOLDER = 'ACTUAL ADDITIONAL FOLDER'
```

These variables contain no API key. They can instead be set by a local launcher. Keep local paths out of portable experiment descriptions except as recorded environment metadata.

## Create the compiler template

A device and application tree is version-dependent. We do not manufacture an unverified device ID. The reliable initial procedure is to create a standard project once in the installed IDE:

1. Open the intended CODESYS instance and choose **File > New Project > Standard project**.
2. Save it as `codesys\templates\benchmark.project` inside this repository.
3. Select the actually installed **CODESYS Control Win V3 x64** target (or the locally available Control Win target) and **Structured Text** for `PLC_PRG`.
4. Confirm the device tree contains exactly one `Application`, a Library Manager with its Standard dependency resolved, and a task configuration calling `PLC_PRG`. Leave `PLC_PRG` as an empty `PROGRAM PLC_PRG` with an empty `VAR ... END_VAR` declaration.
5. Use **Build > Rebuild** once. Resolve missing target, library, or compiler-version errors before continuing. Save and close the template so the automation can open copies independently.
6. Keep the target/device version, compiler version, library versions, task period, template file, and its hash fixed across E1-E4. Screenshots from this actual step can be used as environment evidence, but they are not benchmark task results.

The backend deliberately rejects templates with zero or multiple applications. It creates `FB_Task`, inserts its declaration and implementation in their separate editor parts, and enables `link_always` so an otherwise unused function block is compiled. It then checks that the compiled POU has a signature CRC. A compiler profile that cannot provide this evidence remains an infrastructure limitation until an explicit caller binding is implemented and validated.

The [object-container API](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptIecLanguageObjectContainer.html) documents DUT, function-block, function, and program creation. Its modern online page displays the special-check `create_pou` overload but older profiles also expose the generic overload used here. The installed runtime remains the final compatibility check. `create_dut` defaults to `DutType.Structure`; supporting DUT declarations are replaced in full. The [text-document API](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptTextualObject.html) documents full-buffer replacement and normalized newlines; the script reads the editor buffer back to verify insertion.

## Run the read-only installation probe

Before template creation, the probe can enumerate actual installed device descriptions and any project/profile files under the installation root. If a template path is supplied, it reads its object tree without saving it. It does not create a device, install a package, or alter a project.

```powershell
$env:PLC_CODESYS_PROBE = Join-Path (Get-Location) 'results\raw\codesys_probe.json'
& $env:PLC_CODESYS_EXE "--profile=$env:PLC_CODESYS_PROFILE" `
    "--runscript=$((Resolve-Path '.\codesys\scripts\probe.py').Path)" --noUI
```

Append `--additionalfolder=...` if required. Inspect the resulting JSON. A process exit code alone cannot establish that the script ran; the JSON file must exist and contain this invocation's actual executable and device inventory. Probe errors are recorded by stage. The script's `actual_compilation` value remains `false`.

## Validate real compilation with three fixtures

Use the Project1 interpreter, with `PYTHONPATH` set as above:

```powershell
& 'C:\Users\田子佼\.conda\envs\Project1\python.exe' -X utf8 `
    '.\codesys\validate_backend.py'
```

The check creates fresh subdirectories under `results\raw\compiler_smoke` and tests:

| Fixture | Implementation | Required actual result |
|---|---|---|
| Valid | `y := x;` | PASS and compiled POU CRC |
| Invalid | `y := ;` | COMPILE_FAIL with actual compiler errors |
| Repaired | `y := x;` | PASS and compiled POU CRC |

This is a manually repaired backend fixture, not an LLM repair experiment. If the compiler configuration is absent it writes `NOT_RUN`; if infrastructure fails it stops, preserving evidence. Do not relabel either situation as a model syntax failure.

For each actual attempt preserve `request.json`, `candidate.json`, `FB_Task.st`, `task.project`, `invocation.json`, `stdout.log`, `stderr.log`, `codesys_evidence.json`, and `compile_result.json`. Success requires a matching nonce and source hash, a completed rebuild, no `Error` or `FatalError`, a compiled `FB_Task` signature, and a normal process exit. The [application API](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptApplication.html) provides clean/rebuild. The [message API](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptSystem.html) supplies typed diagnostics. The [object API](https://content.helpme-codesys.com/en/ScriptingEngine/ScriptObject.html) documents forced linking and POU signature CRCs.

The script cleans the application and clears existing message categories before rebuilding. Never reuse a result file from another candidate. Templates are copied into a new workspace for every attempt. Infrastructure/target/library errors must be investigated before treating candidate-related errors as code-generation failures.

## Command-line protocol

The external process invokes the installed executable with an argument list, `--profile`, `--runscript`, `--scriptargs:<ASCII nonce>`, and `--noUI`. Full request data travel through a UTF-8 JSON file named by `PLC_CODESYS_REQUEST`, avoiding complex JSON quoting on the command line. The embedded script checks that the nonce arrives in `sys.argv`. CODESYS executes its own scripting Python; it does not use Project1 for this part. [Official script launch examples](https://content.helpme-codesys.com/en/CODESYS%20Scripting/_cds_starting_script_via_command_line.html) demonstrate the colon form of `--scriptargs` and the `sys.argv` behavior. Whether a selected installed version accepts the invocation is verified by the smoke fixtures, not presumed from the documentation.

## Functional testing and limitations

A successful rebuild only establishes compilation. To obtain real runtime evidence, use an isolated Control Win simulation or local SoftPLC, reset the FB instance for each test case, set every sampled input, invoke exactly one scan, and observe outputs at scan end. Preserve timestamps, actual outputs, case ID, candidate source hash, application version, and the operator or automated test procedure. Ordinary variable writes and a free-running PLC task are insufficient to promise a single controlled scan; verify the stepping mechanism and input/observation timing before recording results.

TON-based public cases require a controlled elapsed-time source or a measured scan period and explicit timing tolerance. Advancing a Python loop is not advancing the runtime timer. PUB004's 500-hour accumulation boundary cannot be claimed from a short wall-clock test without a separately validated time-control path. The generic FIFO's official VARIANT interface also requires a verified CODESYS type/reflection binding; a concrete DINT-only replacement does not establish genericity.

Manual testing is acceptable for this assignment. Record unexecuted cases as `NOT_RUN` or `UNVERIFIED`. Python oracle checks validate expected sequences independently and must remain labelled `PYTHON_REFERENCE_ONLY`. Finite traces do not prove unbounded LTL liveness. Automated PLCVerif integration and physical hardware deployment are outside this documented mandatory compiler path.

## Verification record

This file is an operation guide and API review, not an installation or experiment certificate. Actual status must be taken from `results/raw`, the environment inventory, and experiment summaries. At authoring, installed-profile execution of these scripts has not been observed by the authoring agent.
