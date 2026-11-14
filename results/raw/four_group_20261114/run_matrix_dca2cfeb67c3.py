import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent/'matrix_runner_dca2cfeb67c3/src'))
from plc_agent.batch import main
if __name__ == '__main__':
    raise SystemExit(main())
