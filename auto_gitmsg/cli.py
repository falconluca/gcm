"""命令行入口模块"""

import argparse
import sys
import os
from pathlib import Path
from typing import Optional

import yaml

from auto_gitmsg import __version__
from auto_gitmsg.git_utils import (
    is_git_repo,
    get_staged_changes,
    StagedChanges
)
from auto_gitmsg.prompts import build_user_prompt, get_system_prompt
from auto_gitmsg.llm_client import LLMClient, create_client_from_config


def find_config_file() -> Optional[Path]:
    """查找配置文件

    查找顺序:
    1. 当前目录的 .gitmsg.yaml
    2. 当前目录的 .gitmsg.yml
    3. 用户主目录的 .gitmsg.yaml
    4. 用户主目录的 .gitmsg.yml
    """
    config_names = [".gitmsg.yaml", ".gitmsg.yml"]

    # 当前目录
    for name in config_names:
        path = Path.cwd() / name
        if path.exists():
            return path

    # 用户主目录
    for name in config_names:
        path = Path.home() / name
        if path.exists():
            return path

    return None


def load_config(config_path: Optional[Path] = None) -> dict:
    """加载配置文件

    Args:
        config_path: 配置文件路径，如果为 None 则自动查找

    Returns:
        配置字典
    """
    if config_path is None:
        config_path = find_config_file()

    if config_path and config_path.exists():
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}

    return {}


def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        prog="gitmsg",
        description="自动生成 Git Commit Message"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="生成详细的 commit message"
    )

    parser.add_argument(
        "-c", "--config",
        type=str,
        help="指定配置文件路径"
    )

    parser.add_argument(
        "--api-base",
        type=str,
        help="API 基础 URL"
    )

    parser.add_argument(
        "--api-key",
        type=str,
        help="API Key（不推荐在命令行中使用）"
    )

    parser.add_argument(
        "-m", "--model",
        type=str,
        help="使用的模型名称"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只显示生成的 commit message，不执行 git commit"
    )

    return parser.parse_args()


def generate_commit_message(
    changes: StagedChanges,
    client: LLMClient,
    verbose: bool = False
) -> str:
    """生成 commit message

    Args:
        changes: 暂存区变更
        client: LLM 客户端
        verbose: 是否详细模式

    Returns:
        生成的 commit message
    """
    system_prompt = get_system_prompt()
    user_prompt = build_user_prompt(changes, verbose=verbose)

    return client.chat(system_prompt, user_prompt)


def main():
    """主入口函数"""
    args = parse_args()

    # 检查是否在 git 仓库中
    if not is_git_repo():
        print("错误: 当前目录不在 Git 仓库中", file=sys.stderr)
        sys.exit(1)

    # 获取暂存区变更
    changes = get_staged_changes()

    if not changes.files:
        print("暂存区没有变更。请先使用 'git add' 添加变更。", file=sys.stderr)
        sys.exit(1)

    # 加载配置
    config_path = Path(args.config) if args.config else None
    config = load_config(config_path)

    # 命令行参数覆盖配置文件
    if args.api_base:
        config["api_base"] = args.api_base
    if args.api_key:
        config["api_key"] = args.api_key
    if args.model:
        config["model"] = args.model

    # 创建 LLM 客户端
    client = create_client_from_config(config)

    # 生成 commit message
    try:
        commit_msg = generate_commit_message(
            changes,
            client,
            verbose=args.verbose
        )
    except ValueError as e:
        print(f"配置错误: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"生成失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 输出结果
    print(commit_msg)


if __name__ == "__main__":
    main()
