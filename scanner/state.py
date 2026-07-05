"""scanner/state.py -- load/save the seen-listings state file."""
import json
from scanner.config import log, STATE_FILE, TODAY


def load_state() -> dict:
    """Load state from JSON file, creating default structure if file doesn't exist."""
    # Default state structure
    state = {
        "listings": {},
        "meta": {}
    }

    # Try to load existing file
    if STATE_FILE.exists():
        try:
            loaded_data = json.loads(STATE_FILE.read_text())
            state.update(loaded_data)
            log.debug(f"Loaded existing state from {STATE_FILE}")
        except Exception as e:
            log.warning(f"Couldn't parse existing state file: {e}. Starting fresh.")

    else:
        log.info(f"{STATE_FILE} not found. Creating new state.")
        log.info(f"Initial meta: {state['meta']}")

    return state


def save_state(state: dict) -> None:
    state["meta"]["last_run"] = TODAY
    state["meta"]["run_count"] = state["meta"].get("run_count", 0) + 1
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    log.info("State saved -> %s  (%d listings)", STATE_FILE.name, len(state["listings"]))
