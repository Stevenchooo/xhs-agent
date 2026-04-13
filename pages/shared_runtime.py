"""Shared runtime globals for extracted page modules."""

from pathlib import Path

import xhs_agent.config as cfg


def ai_enabled() -> bool:
    return cfg.has_ai_config()


class _DynamicAIGate:
    """Allow legacy `if OPENAI_API_KEY` checks to remain dynamic."""

    def __bool__(self):
        return ai_enabled()


OPENAI_API_KEY = _DynamicAIGate()
AI_SETUP_ERROR = "请先在设置页面配置 Claude API Key（支持 .env.local / CLAUDE_CODE_API_KEY / ANTHROPIC_API_KEY）"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXIF_SCRIPT_PATH = PROJECT_ROOT / "scripts" / "add_exif.py"
SUPPORTED_IMAGE_SUFFIXES = (".jpg", ".jpeg", ".png", ".webp")
