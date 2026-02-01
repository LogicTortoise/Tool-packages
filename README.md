# Tool Packages

个人工具包集合，包含各类自动化工具的 Claude Code Skills 和开发代码。

## 仓库结构

```
Tool-packages/
├── README.md                    # 本文档
└── <tool-name>/                 # 工具名称目录
    ├── skill/                   # Claude Code Skill 文件
    │   ├── <tool-name>.skill    # 打包的 skill 文件
    │   └── source/              # skill 源代码（可选）
    │       ├── SKILL.md
    │       ├── scripts/
    │       └── references/
    └── development/             # 开发和测试代码
        ├── README.md            # 工具说明文档
        ├── requirements.txt     # Python 依赖
        ├── test_*.py            # 测试脚本
        └── ...                  # 其他开发文件
```

## 目录说明

### skill/ 目录

存放 Claude Code Skill 相关文件：

- **`<tool-name>.skill`**: 打包好的 skill 文件，可直接安装使用
- **`source/`**: skill 的源代码（可选），用于维护和更新 skill

### development/ 目录

存放工具的开发代码和测试文件：

- 完整的项目源代码
- 测试脚本和测试报告
- 开发文档
- 依赖配置文件

## 工具列表

### 1. THSTrader - 同花顺自动交易工具

**功能**: 通过 Android 模拟器自动化操控同花顺 APP 进行模拟炒股

**Skill 位置**: `thstrader/skill/thstrader.skill`

**开发代码**: `thstrader/development/`

**主要功能**:
- 查询账户余额和持仓
- 自动买入/卖出股票
- 管理委托订单和撤单
- 支持策略自动化

**技术栈**: Python + uiautomator2 + ADB + EasyOCR

---

## 使用指南

### 安装 Skill

```bash
# 方法 1: 直接安装 .skill 文件
claude-code skill install <tool-name>/skill/<tool-name>.skill

# 方法 2: 从源代码打包（需要 skill-creator）
cd <tool-name>/skill/source
# 使用 skill-creator 打包
```

### 使用开发代码

```bash
# 进入开发目录
cd <tool-name>/development

# 安装依赖
pip install -r requirements.txt

# 查看使用说明
cat README.md

# 运行测试
python test_*.py
```

## 维护说明

### 添加新工具

1. 创建工具目录：
   ```bash
   mkdir -p <tool-name>/skill <tool-name>/development
   ```

2. 放置 skill 文件到 `<tool-name>/skill/`

3. 放置开发代码到 `<tool-name>/development/`

4. 更新本 README 的"工具列表"部分

### 更新现有工具

1. **更新 Skill**:
   - 修改 `<tool-name>/skill/source/` 中的源代码
   - 重新打包生成新的 `.skill` 文件
   - 替换 `<tool-name>/skill/<tool-name>.skill`

2. **更新开发代码**:
   - 直接修改 `<tool-name>/development/` 中的文件
   - 运行测试确保功能正常
   - 更新 README 和测试报告

## Git 提交规范

- **feat**: 新增工具或功能
- **fix**: 修复 bug
- **docs**: 文档更新
- **refactor**: 代码重构
- **test**: 测试相关
- **chore**: 构建/配置更新

示例：
```bash
git commit -m "feat(thstrader): add auto stop-loss feature"
git commit -m "fix(thstrader): fix UI element detection"
git commit -m "docs(thstrader): update API reference"
```

## 许可证

本仓库为私有仓库，仅供个人使用。

## 联系方式

- GitHub: [私有仓库]
- 维护者: Hht
