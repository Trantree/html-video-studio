# HTML Video Studio

用HTML+Python自动化生成1080×1920竖屏短视频的开源工具链，无需手动剪辑。

## 特性

- 🚀 **纯本地运行**：无付费API依赖，Playwright + Edge-TTS + ffmpeg 全开源组件
- 🎬 **HTML渲染画面**：用HTML/CSS做可视化画面，浏览器逐帧截图为视频帧
- 🎙️ **免费AI配音**：调用微软Edge-TTS，无需API Key，支持多种中文音色
- ⏱️ **自动时间轴**：根据配音实际时长自动计算每个镜头的长度，无需手动卡秒数
- 📦 **批量出片**：写一个JSON配置即可生成整条视频，改配置即可复用模板

## 快速开始

### 环境要求

- Python 3.10+
- ffmpeg（已加入系统PATH）

### 安装

```bash
git clone https://github.com/Trantree/html-video-studio.git
cd html-video-studio
pip install -r requirements.txt
playwright install chromium
```

### 生成你的第一个视频

1. 复制示例故事配置：
```bash
cp stories/example.json stories/my_first_video.json
```

2. 编辑 `stories/my_first_video.json`，替换成你自己的文案和数据

3. 生成配音与时间轴：
```bash
python build_audio.py --story stories/my_first_video.json --out ./work
```

4. 逐帧渲染画面：
```bash
python render_story.py --story stories/my_first_video.json --out ./work --mode full
```

5. 合成最终视频：
```bash
python render_story.py --story stories/my_first_video.json --out ./work --mux
```

输出文件在 `./work/final.mp4`，1080×1920 竖屏30fps。

## 项目结构

```
html-video-studio/
├── build_audio.py          # 配音生成与时间轴自动回填
├── render_story.py         # 逐帧渲染与视频合成
├── templates/
│   └── base.html           # 基础HTML画面模板
├── stories/
│   └── example.json         # 示例项目配置
└── requirements.txt
```

## 常见问题

**Q: 生成的视频字体不对？**
A: 确保你的系统安装了对应字体，或在模板中替换成系统已有字体。

**Q: 配音声音太小？**
A: ffmpeg混音时加 `normalize=0` 参数，避免音量被自动衰减。

**Q: 怎么换音色？**
A: 修改story.json中的`voice.name`字段，可选音色列表见Edge-TTS文档。

## License

MIT