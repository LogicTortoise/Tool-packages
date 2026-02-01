# THSTrader Skill

同花顺自动交易 Claude Code Skill

## 文件说明

### thstrader.skill

打包好的 Claude Code Skill 文件，可直接安装使用。

**安装方法**:
```bash
# 复制到 Claude Code skills 目录
cp thstrader.skill ~/.claude/skills/

# 或者使用 Claude Code 命令安装（如果支持）
claude-code skill install thstrader.skill
```

### source/

Skill 的源代码，用于维护和更新。

**结构**:
```
source/
├── SKILL.md                      # Skill 主文档
├── scripts/                      # 可执行脚本
│   ├── trader.py                 # CLI 入口
│   ├── example.py                # 使用示例
│   ├── requirements.txt          # 依赖
│   └── ths/                      # 核心模块
│       ├── __init__.py
│       ├── config.py
│       └── trader.py
└── references/                   # 参考文档
    ├── setup.md                  # 环境配置
    ├── api-reference.md          # API 文档
    └── troubleshooting.md        # 故障排除
```

## 更新 Skill

1. 修改 `source/` 中的文件

2. 使用 skill-creator 重新打包：
   ```bash
   cd ~/.claude/skills/skill-creator
   python scripts/package_skill.py /path/to/source
   ```

3. 替换 `thstrader.skill` 文件

## 功能特性

- ✅ 查询账户余额
- ✅ 查看持仓列表
- ✅ 买入股票
- ✅ 卖出股票
- ✅ 查看可撤单列表
- ✅ 撤单操作
- 📸 自动截图记录
- 🔍 OCR 识别

## 使用示例

在 Claude Code 中直接使用自然语言：

```
"帮我查询股票账户余额"
"买入1000股海康威视，价格31.5元"
"查看我的持仓情况"
"撤销所有未成交的委托"
```

Claude Code 会自动识别并使用此 skill。

## 技术要求

- **Android 模拟器**: BlueStacks (127.0.0.1:5565)
- **分辨率**: 720x1280 (必须)
- **同花顺版本**: 11.46.04
- **Python**: 3.8+
- **依赖**: uiautomator2, easyocr, Pillow

详细配置请参考 `source/references/setup.md`

## 版本历史

- **v1.0** (2026-02-01): 初始版本
  - 支持基本交易功能
  - CLI 和 Python API
  - 完整的参考文档
