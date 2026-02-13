.PHONY: install uninstall clean test help build clean-bin

BIN_DIR ?= ~/bin

help:
	@echo "GCM - Git Commit Message Generator"
	@echo ""
	@echo "  make install    安装到本地（pip editable）"
	@echo "  make uninstall  卸载"
	@echo "  make clean      清理缓存"
	@echo "  make test       测试运行"
	@echo "  make rebuild    重新安装"
	@echo "  make build      打包二进制到 $(BIN_DIR)"
	@echo "  make clean-bin  清理二进制文件"

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

build:
	@echo "打包二进制文件..."
	pip install pyinstaller -q
	pyinstaller --onefile --name gcm gcm/cli.py
	install -m 755 dist/gcm $(BIN_DIR)/
	rm -rf build/ dist/ gcm.spec
	@echo "已安装到 $(BIN_DIR)/gcm"

clean-bin:
	@echo "清理二进制文件..."
	rm -rf build/ dist/ gcm.spec
	rm -f $(BIN_DIR)/gcm
	@echo "清理完成"
