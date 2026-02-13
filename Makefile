.PHONY: install uninstall clean test help

help:
	@echo "GCM - Git Commit Message Generator"
	@echo ""
	@echo "  make install    安装到本地"
	@echo "  make uninstall  卸载"
	@echo "  make clean      清理缓存"
	@echo "  make test       测试运行"
	@echo "  make rebuild    重新安装"

install:
	pip install -e .

uninstall:
	pip uninstall -y gcm

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true

test:
	@echo "测试 gcm 命令..."
	gcm --help

rebuild: clean install
	@echo "重新安装完成"
