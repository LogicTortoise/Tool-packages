# Tool Packages

个人工具包集合，包含各类自动化工具的 AgentSkills 和开发代码。

## 仓库结构

```
Tool-packages/
├── README.md                    # 本文档
└── <tool-name>/                 # 工具名称目录（也是 skill 目录）
    ├── SKILL.md                 # Skill 定义（OpenClaw/AgentSkills 格式）
    ├── scripts/                 # Skill 脚本（可选）
    ├── references/              # Skill 参考文档（可选）
    ├── skill/                   # 打包文件（可选）
    │   └── <tool-name>.skill    # 打包的 .skill 文件
    └── development/             # 开发和测试代码（可选）
        ├── README.md
        ├── requirements.txt
        └── ...
```

**关键**: `SKILL.md` 必须在工具根目录下，OpenClaw 通过 `extraDirs` 扫描时才能识别。

## OpenClaw 集成

本仓库通过 `skills.load.extraDirs` 配置自动加载到 OpenClaw：

```json
"skills": {
  "load": {
    "extraDirs": ["/Users/Hht/Documents/10.github/Tool-packages"]
  }
}
```

新增 skill 只需在本仓库下创建目录并放入 `SKILL.md`，OpenClaw 会自动发现。

## 目录说明

### 根目录文件（Skill 定义）

- **`SKILL.md`**: Skill 定义文件（YAML frontmatter + Markdown 指令），必须在工具根目录
- **`scripts/`**: Skill 使用的可执行脚本
- **`references/`**: 参考文档，按需加载到上下文

### skill/ 目录

- **`<tool-name>.skill`**: 打包好的 .skill 文件，用于分发

### development/ 目录

存放工具的开发代码和测试文件

## 工具列表

### 1. THSTrader - 同花顺自动交易工具

**功能**: 通过 Android 模拟器自动化操控同花顺 APP 进行模拟炒股

**Skill**: `thstrader/SKILL.md`

**开发代码**: `thstrader/development/`

**主要功能**:
- 查询账户余额和持仓
- 自动买入/卖出股票
- 管理委托订单和撤单
- 自选股管理（添加、删除、搜索）
- 从自选股快速交易
- 支持策略自动化

**技术栈**: Python + uiautomator2 + ADB + cnocr (中文OCR)

**架构特点**:
- 使用 mobileas 启发的 Device 类进行连接管理
- 稳定的 u2.connect_usb() 连接方式
- 自动重试机制和错误处理
- 解决 BlueStacks/模拟器兼容性问题

### 2. Bilibili-to-Text - B站视频转文字工具

**功能**: 下载 Bilibili 视频并使用 faster-whisper 转录为高质量中文文本

**Skill**: `bilibili-to-text/SKILL.md`

**主要功能**:
- 自动下载 Bilibili 视频（支持 b23.tv 短链接）
- 高质量语音转文字（95%+ 中文准确度）
- 生成 SRT 字幕 + TXT 纯文本
- 自动语言检测
- 可选内容分析和总结

**技术栈**: Python + you-get + faster-whisper + Whisper medium 模型

**核心优势**:
- 转录质量比 bili2text 提升 15 倍以上
- 处理速度比原版 Whisper 快 4-10 倍
- 中文准确度：⭐⭐⭐⭐⭐
- 支持长视频批量处理

**依赖项目**: `~/Documents/10.github/bili2text/`

---

## 使用指南

### 添加新工具

1. 创建工具目录并放入 `SKILL.md`：
   ```bash
   mkdir <tool-name>
   # 编写 SKILL.md（YAML frontmatter + 指令）
   ```

2. OpenClaw 自动通过 `extraDirs` 发现新 skill

3. 如需环境变量，在 `~/.openclaw/openclaw.json` 的 `skills.entries` 中添加配置

### 更新现有工具

直接修改 `<tool-name>/SKILL.md` 和对应的 `scripts/`、`references/`，OpenClaw watcher 会自动刷新

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
