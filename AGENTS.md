# Local project execution

- Ask the user for explicit approval before each real model API experiment. The teacher API has a limited shared budget. An `--allow-model-api` flag records that approval; it does not replace asking the user.
- Run Python unit tests in the sandbox. Run real CODESYS compilation and simulation from a normal Windows process outside the agent sandbox, using the tool's approved escalation mechanism. Do not disable security controls or Windows logging.
- On this computer, launching CODESYS inside the restricted sandbox caused APInstaller.CLI.exe to fail writing the Windows event-log source `AP Installer` (Access denied), producing repeated 0xe0434352 dialogs. The same component and real simulation succeeded outside that sandbox. A sandboxed simulation also failed to connect to the Gateway despite the service running.
- Treat TOOL_ERROR, TIMEOUT, and UNVERIFIED as infrastructure outcomes, never candidate correctness results. FakeBackend is for unit tests, and does not execute candidate ST.
- Keep reference-code validation separate from model/agent benchmark results. Do not publish historical percentages without their matching raw campaign records.
- Never include credentials, `.env`, API key files, or `runtime.local.json` in shared archives or commits.
