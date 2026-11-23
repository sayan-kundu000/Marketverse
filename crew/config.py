"""Marketverse Configuration & Environment Initialization."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Base workspace directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env file
load_dotenv(BASE_DIR / ".env")

# Ensure telemetry is disabled and LOCALAPPDATA is safely sandboxed
os.environ.setdefault("CREWAI_TELEMETRY_OPT_OUT", "true")
os.environ.setdefault("OTEL_SDK_DISABLED", "true")

# Redirect LOCALAPPDATA to workspace directory to avoid sandbox permission errors
workspace_localappdata = BASE_DIR / ".localappdata"
workspace_localappdata.mkdir(parents=True, exist_ok=True)
os.environ["LOCALAPPDATA"] = str(workspace_localappdata)

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")
SERPER_API_KEY = os.getenv("SERPER_API_KEY", "")
MARKETVERSE_OFFLINE_MODE = os.getenv("MARKETVERSE_OFFLINE_MODE", "false").lower() in ("true", "1", "yes")

# Directories
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
