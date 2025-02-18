from pathlib import Path

from .base import BasePrompt, PromptRegistry

# Đường dẫn đến thư mục templates
TEMPLATE_DIR = Path(__file__).parent / "templates"

# Các prompt mặc định
DEFAULT_PROMPTS = {
    "system": {
        "file": "system.txt",
        "kwargs": {
            "language": "Vietnamese",
            "specialties": ["Đa khoa", "Y học cơ bản"],
            "data_sources": ["PubMed", "Cơ sở dữ liệu nội bộ"],
        },
    },
    "query_transform": {"file": "query_transform.txt", "kwargs": {}},
    "synthesis": {"file": "synthesis.txt", "kwargs": {}},
}


def load_prompts():
    """Load và đăng ký tất cả các prompt."""
    for name, config in DEFAULT_PROMPTS.items():
        template_path = TEMPLATE_DIR / config["file"]
        if template_path.exists():
            PromptRegistry.register_from_file(
                name=name, file_path=str(template_path), **config.get("kwargs", {})
            )
        else:
            raise FileNotFoundError(f"Template file not found: {template_path}")


# Load prompts khi import module
load_prompts()
