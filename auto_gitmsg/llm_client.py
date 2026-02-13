"""LLM 客户端模块"""

import os
import json
from typing import Optional
from dataclasses import dataclass
import urllib.request
import urllib.error


@dataclass
class LLMConfig:
    """LLM 配置"""
    api_base: str = "https://api.openai.com/v1"
    api_key: Optional[str] = None
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    max_tokens: int = 1000
    timeout: int = 30

    def __post_init__(self):
        # 从环境变量获取 API Key
        if self.api_key is None:
            self.api_key = os.environ.get("OPENAI_API_KEY")


class LLMClient:
    """与大模型交互的客户端"""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        """发送聊天请求

        Args:
            system_prompt: 系统提示词
            user_prompt: 用户提示词

        Returns:
            模型生成的响应文本

        Raises:
            ValueError: API Key 未配置
            RuntimeError: API 调用失败
        """
        if not self.config.api_key:
            raise ValueError(
                "API Key 未配置。请设置环境变量 OPENAI_API_KEY "
                "或在配置文件中指定 api_key。"
            )

        url = f"{self.config.api_base.rstrip('/')}/chat/completions"

        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.config.temperature,
            "max_tokens": self.config.max_tokens
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}"
        }

        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers=headers,
                method="POST"
            )

            with urllib.request.urlopen(req, timeout=self.config.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]

        except urllib.error.HTTPError as e:
            error_body = e.read().decode("utf-8") if e.fp else "Unknown error"
            raise RuntimeError(f"API 调用失败 ({e.code}): {error_body}")
        except urllib.error.URLError as e:
            raise RuntimeError(f"网络请求失败: {e.reason}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"响应解析失败: {e}")
        except KeyError as e:
            raise RuntimeError(f"响应格式异常: 缺少字段 {e}")


def create_client_from_config(config_dict: dict) -> LLMClient:
    """从配置字典创建 LLM 客户端

    Args:
        config_dict: 配置字典

    Returns:
        LLMClient 实例
    """
    llm_config = LLMConfig()

    if "api_base" in config_dict:
        llm_config.api_base = config_dict["api_base"]
    if "api_key" in config_dict:
        llm_config.api_key = config_dict["api_key"]
    if "model" in config_dict:
        llm_config.model = config_dict["model"]
    if "temperature" in config_dict:
        llm_config.temperature = float(config_dict["temperature"])
    if "max_tokens" in config_dict:
        llm_config.max_tokens = int(config_dict["max_tokens"])
    if "timeout" in config_dict:
        llm_config.timeout = int(config_dict["timeout"])

    return LLMClient(llm_config)
