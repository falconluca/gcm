"""LLM 客户端模块"""

import os
from typing import Optional
from dataclasses import dataclass

from openai import OpenAI


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
        # 从环境变量获取配置
        if self.api_key is None:
            self.api_key = os.environ.get("OPENAI_API_KEY")

        # 支持 OPENAI_API_URL 环境变量（兼容智谱等第三方服务）
        api_url = os.environ.get("OPENAI_API_URL")
        if api_url and self.api_base == "https://api.openai.com/v1":
            self.api_base = api_url


class LLMClient:
    """与大模型交互的客户端"""

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or LLMConfig()
        self._client: Optional[OpenAI] = None

    @property
    def client(self) -> OpenAI:
        """懒加载 OpenAI 客户端"""
        if self._client is None:
            if not self.config.api_key:
                raise ValueError(
                    "API Key 未配置。请设置环境变量 OPENAI_API_KEY "
                    "或在配置文件中指定 api_key。"
                )

            self._client = OpenAI(
                api_key=self.config.api_key,
                base_url=self.config.api_base,
                timeout=self.config.timeout
            )
        return self._client

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
        try:
            response = self.client.chat.completions.create(
                model=self.config.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.choices[0].message.content

        except Exception as e:
            raise RuntimeError(f"API 调用失败: {e}")


def create_client_from_config(config_dict: dict) -> LLMClient:
    """从配置字典创建 LLM 客户端

    Args:
        config_dict: 配置字典

    Returns:
        LLMClient 实例
    """
    # 先让 LLMConfig 从环境变量加载默认值
    llm_config = LLMConfig()

    # 配置文件中的值覆盖环境变量
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
