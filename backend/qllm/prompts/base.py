from typing import Any, Dict

from llama_index.core.prompts import PromptTemplate


class BasePrompt:
    """Class cơ sở cho tất cả các prompt."""

    def __init__(self, template: str, **kwargs):
        self.template = template
        self.prompt = PromptTemplate(template)
        self.kwargs = kwargs

    def format(self, **kwargs) -> str:
        """
        Format prompt với các tham số được cung cấp.
        """
        # Kết hợp kwargs mặc định với kwargs được cung cấp
        format_kwargs = {**self.kwargs}
        format_kwargs.update(kwargs)
        return self.prompt.format(**format_kwargs)

    @classmethod
    def from_file(cls, file_path: str, **kwargs):
        """
        Tạo prompt từ file template.
        """
        with open(file_path, "r", encoding="utf-8") as f:
            template = f.read()
        return cls(template, **kwargs)


class PromptRegistry:
    """Quản lý tất cả các prompt trong hệ thống."""

    _registry: Dict[str, BasePrompt] = {}

    @classmethod
    def register(cls, name: str, prompt: BasePrompt):
        """Đăng ký một prompt mới."""
        cls._registry[name] = prompt

    @classmethod
    def get(cls, name: str) -> BasePrompt:
        """Lấy prompt theo tên."""
        if name not in cls._registry:
            raise KeyError(f"Prompt '{name}' không tồn tại trong registry")
        return cls._registry[name]

    @classmethod
    def register_from_file(cls, name: str, file_path: str, **kwargs):
        """Đăng ký prompt từ file template."""
        prompt = BasePrompt.from_file(file_path, **kwargs)
        cls.register(name, prompt)
