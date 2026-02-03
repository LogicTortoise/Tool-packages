---
name: bilibili-to-text
description: Download Bilibili videos and transcribe them to text using faster-whisper. Use when the user provides a Bilibili URL (b23.tv, bilibili.com/video), asks to transcribe/convert a Bilibili video to text, requests video subtitles, or wants to analyze/summarize video content from Bilibili.
---

# Bilibili Video to Text

Convert Bilibili videos to high-quality text transcripts using faster-whisper with Whisper medium model.

## Overview

This skill enables downloading Bilibili videos and converting them to text with 15x better quality than alternative tools. It produces SRT subtitles, TXT plain text, and optional Markdown documents.

**Key advantages**:
- High-quality Chinese transcription (95%+ accuracy)
- 4-10x faster than original Whisper
- Multiple output formats (SRT + TXT + MD)
- Automatic language detection

## Quick Start

### Single Video Workflow

Execute these commands in sequence:

```bash
# 1. Navigate to project directory
cd ~/Documents/10.github/bili2text

# 2. Download video
you-get "<bilibili-url>"

# 3. Find the downloaded video
find . -name "*.mp4" -type f -mtime -1

# 4. Transcribe to text
python3 faster_whisper_subtitle.py \
    "<video-file-path>" \
    "subtitles/<output-name>.srt" \
    medium
```

**Example**:
```bash
cd ~/Documents/10.github/bili2text
you-get "https://b23.tv/stO0N9K"
python3 faster_whisper_subtitle.py \
    "./是什么导致了金银暴跌？我们接下来应该怎么应对？（下）-当前宏观经济形势与热点分析.mp4" \
    "subtitles/金银暴跌分析.srt" \
    medium
```

### Output Files

After transcription completes:
- `subtitles/<name>.srt` - SRT subtitle file with timestamps
- `subtitles/<name>.txt` - Plain text version (auto-generated)

### Reading Transcripts

Always read the TXT file for analysis:
```bash
# Read the transcript
cat subtitles/<name>.txt
```

Then provide analysis or summary as requested by the user.

## Workflow Details

### 1. Download Video

Use `you-get` to download from Bilibili:

```bash
cd ~/Documents/10.github/bili2text
you-get "<url>"
```

**Supported URL formats**:
- `https://www.bilibili.com/video/BV1XoqJBiE7T`
- `https://b23.tv/stO0N9K`
- `BV1XoqJBiE7T` (BV number only)

**Notes**:
- Default quality: 480P (no login required)
- 720P+ requires login cookies
- Videos download to current directory with Chinese filename

### 2. Locate Downloaded File

Find the video file:
```bash
find . -name "*.mp4" -type f -mtime -1
```

Or list recent downloads:
```bash
ls -lt *.mp4 | head -5
```

### 3. Transcribe Video

Run faster-whisper transcription:

```bash
python3 faster_whisper_subtitle.py \
    "<video-path>" \
    "subtitles/<output-name>.srt" \
    medium
```

**Parameters**:
- Param 1: Input video file path
- Param 2: Output SRT file path
- Param 3: Model size (`medium` recommended for Chinese)

**Processing indicators**:
```
📹 视频: <path>
📝 输出: <srt-path>
🤖 模型: medium
⏳ 加载 Whisper 模型...
✅ 模型加载完成
🎙️  开始转录...
📊 检测到的语言: zh (概率: 100.00%)
⏱️  视频时长: 1153.5 秒
💾 写入字幕文件...
  已处理 10 个片段...
  已处理 20 个片段...
  ...
✅ 完成! 共生成 480 个字幕片段
📄 生成纯文本版本: subtitles/<name>.txt
✅ 纯文本文件生成完成!
```

**Processing time**:
- 5-min video: ~2-3 minutes
- 15-min video: ~5-8 minutes
- 30-min video: ~15-20 minutes
- Ratio: ~0.5-0.7x of video duration

### 4. Analyze Results

Read the TXT file and provide analysis:

```bash
# Read transcript
cat subtitles/<name>.txt

# Or use Read tool
Read subtitles/<name>.txt
```

Then summarize key points, conclusions, or answer user questions based on the transcript content.

## Model Selection

| Model | Size | Speed | Chinese Accuracy | Recommended |
|-------|------|-------|-----------------|-------------|
| tiny | 39M | ⭐⭐⭐⭐⭐ | ⭐ | ❌ Not recommended |
| small | 244M | ⭐⭐⭐⭐ | ⭐⭐ | ⚠️ Testing only |
| **medium** | **769M** | **⭐⭐⭐** | **⭐⭐⭐⭐⭐** | ✅ **Strongly recommended** |
| large | 1550M | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⚠️ High resource usage |

**Conclusion**: Use **medium model** for best quality/speed balance in Chinese recognition.

## Project Structure

```
~/Documents/10.github/bili2text/
├── faster_whisper_subtitle.py   # Single video transcription
├── bili_to_text.sh              # One-click automation script
├── batch_convert_corrected.py   # Batch processing
├── generate_markdown.py         # Markdown generation
├── bilibili_video/              # Downloaded videos
└── subtitles/                   # Transcription outputs
    ├── *.srt                    # SRT subtitle files
    ├── *.txt                    # Plain text files
    └── *.md                     # Markdown documents
```

## Common Issues

### Video Already Exists

If `you-get` shows "file already exists":
```bash
# Find existing video
find . -name "*<keyword>*" -type f
```

### Cannot Find Video File

Check download directory:
```bash
ls -lt *.mp4 | head -10
```

Videos use Chinese titles from Bilibili metadata.

### Model Download Location

First run downloads model automatically:
- Location: `~/.cache/huggingface/hub/models--Systran--faster-whisper-medium/`
- Size: ~1.4GB
- Only downloads once, reused for all future transcriptions

## Technical Details

**faster-whisper parameters**:
```python
from faster_whisper import WhisperModel

# Load model
model = WhisperModel("medium", device="cpu", compute_type="int8")

# Transcribe with optimal settings
segments, info = model.transcribe(
    video_path,
    language="zh",          # Chinese recognition
    vad_filter=True,        # Filter silence
    beam_size=5,            # Higher quality
    word_timestamps=True    # Word-level timestamps
)
```

**Key configurations**:
- `device="cpu"`: CPU mode (more stable on Mac)
- `compute_type="int8"`: 4-10x speed boost via quantization
- `vad_filter=True`: Automatic silence filtering
- `beam_size=5`: Beam search for better accuracy

## Output Formats

### SRT Subtitle Format
```srt
1
00:00:00,000 --> 00:00:04,839
今天这一课我们就专门聊一套很实用的实战方法

2
00:00:04,839 --> 00:00:07,480
强势骨右侧三次健仓法
```

### Plain Text Format
```
今天这一课我们就专门聊一套很实用的实战方法
强势骨右侧三次健仓法
它是瑞哥针对强势骨设计的一套
```

Each line is one sentence/phrase for easy reading and processing.

## Workflow Summary

**For typical usage**:

1. User provides Bilibili URL
2. Download video with `you-get`
3. Transcribe with `faster_whisper_subtitle.py` using medium model
4. Read the generated TXT file
5. Provide summary or analysis as requested

**Always use the medium model for Chinese videos to ensure high-quality transcription.**
