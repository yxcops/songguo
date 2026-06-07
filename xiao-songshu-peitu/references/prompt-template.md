# 生图提示词模板

每张图单独生成。根据正文内容替换变量，不要把多张图拼在一起。

如果工具支持参考图，必须使用：

```text
assets/character-reference/squirrel-main.png
```

## 通用模板

```text
Generate one standalone {aspect_ratio} Chinese content illustration.

Use the provided reference image to preserve the recurring character identity.

Recurring IP character:
A 3D plush squirrel character based on the reference image: orange-brown fur, cream cheeks and muzzle, big round brown eyes, round ears, small nose, two front teeth, short paws, and a large dark-green curled tail with glowing blue circuit-like lines and circular nodes. The squirrel must perform the core conceptual action, not just decorate the scene.

Visual direction:
Clean bright background, generous whitespace, modern friendly 3D mascot illustration, lightly whimsical but not childish. The image should explain an idea clearly without becoming a PPT infographic. For article body illustrations, the squirrel should be a working character inside the scene, not a large centered mascot portrait.

Usage and scale:
{用途：正文解释图 / 封面主视觉 / 平台卡片}. If this is an article body illustration, keep the squirrel around 18%-30% of the canvas, generally below 35%. Prefer full-body or 3/4-body action pose. Do not copy the reference image's app-icon framing, white rounded square border, or close-up head composition.

Squirrel state:
{状态：整理 / 缓存 / 守门 / 连接 / 困惑 / 沉淀 / 警惕 / 复用}

Theme:
{正文配图主题}

Core idea:
{这张图要表达的核心意思}

Composition:
{具体画面：小松鼠在哪里、正在做什么、主要物件是什么、信息如何流动}

Suggested elements:
{元素1} / {元素2} / {元素3} / {元素4}

Chinese labels:
{标注词1} / {标注词2} / {标注词3} / {标注词4} / {可选标注词5}

Color use:
Orange-brown and cream for the squirrel. Dark green for the curled tail. Blue glow only for the tail circuit and optional system notes. Orange for flow arrows if needed. Red only for warnings or confirmation marks.

Constraints:
One image explains only one core idea. The information structure should be more important than the character. Keep the squirrel recognizable from the reference image, but do not make it too large unless the image is explicitly a cover visual. Do not turn it into a generic brown squirrel. Do not remove the dark-green curled tail or blue glowing circuit nodes. Do not make it a children's storybook illustration, realistic animal photo, generic pet avatar, dense PPT diagram, complex UI screenshot, app icon, or centered mascot portrait. Use only a few short Chinese labels. The squirrel must be doing the work that explains the concept.
```

## ListenHub CLI 示例

生成前仍需按项目规则向用户确认，因为会消耗额度。

```bash
REFERENCE_IMAGE="$HOME/.codex/skills/xiao-songshu-peitu/assets/character-reference/squirrel-main.png"

listenhub image create \
  --prompt "<上面的完整提示词>" \
  --lang zh \
  --aspect-ratio 16:9 \
  --size 2K \
  --reference "$REFERENCE_IMAGE" \
  --json
```

平台比例按用途调整：

- 小红书图文卡片：3:4。
- 小红书正文插图：4:3 或 16:9。
- 公众号正文配图：16:9 或 4:3。
- 视频封面：16:9。
- 竖屏短视频：9:16。
