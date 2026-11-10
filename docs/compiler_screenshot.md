# Remaining real IDE screenshot

The actual compiler preflight and all selected build records are preserved and independently checked. A real CODESYS GUI screenshot remains absent: desktop app-opening approval timed out. The report labels its diagnostic excerpt as text evidence and does not portray it as a screenshot. PowerPoint native rendering also could not be acquired (COM 80080005 and desktop opening timeout); editable OOXML and exact SVG source previews were checked separately.

To obtain the remaining screenshot without changing the benchmark, open CODESYS V3.5 SP22 Patch 4 manually, then open a **copy** of one preserved preflight project:

```
results/raw/compiler_smoke_2026-10-25T122405987514+0000/invalid/task.project
results/raw/compiler_smoke_2026-10-25T122405987514+0000/repaired/task.project
```

Use Build → Rebuild and display the Messages pane and FB source. Capture the actual IDE window showing the project, diagnostic locations and error count. The invalid fixture should report two errors for `ThisIdentifierDoesNotExist`; the repaired fixture should report zero. Keep the original experiment workspaces unchanged, and do not log in to a physical PLC.

Save the unaltered image under `report/images/`. For an auditable later addition, write `results/summary/compiler_screenshot.json` with its project-relative `path`, actual file `sha256`, `captured_utc`, `actual_codesys_gui: true`, operator and the copied project's provenance. Insert the actual image into the report, recompile/render/review the affected pages, refresh `artifact_qa.json`, then rerun the release audit and package. Creating a metadata record alone does not establish that a screenshot was actually captured.
