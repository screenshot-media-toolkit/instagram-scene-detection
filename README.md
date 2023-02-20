# Instagram Scene Detection

Instagram 截圖場景辨識

## Table of Contents

- [Scenes](#scenes)
- [Run Application](#run-application)
  - [Prerequisites](#prerequisites)
  - [PDM](#pdm-recommended)
  - [PIP + Venv](#pip--venv)
- [Usage](#usage)
- [Configuration](#configuration)
- [Labels](#labels)

## Scenes

- 主頁 (Homepage)
- 限時動態 (Story)
- 留言 (Comment)
- 外部連結 (External)
- 短影片 (Reels)

> Note: 限時動態因為沒有明顯的特徵，所以是用刪去法的方式完成的，辨識率也不會太差。

## Run Application

### Prerequisites

- 下載並編譯 `darknet`

  ```bash
    sh scripts/setup-darknet.sh
  ```

- 放入 `yolov3` model 的設定檔:

  - `metadata` (預設路徑: `./yolov3.data`)
  - `config` (預設路徑: `./yolov3.cfg`)
  - `weights` (預設路徑: `./yolov3.weights`)

- 放入 Google OCR API 的 credentials:

  - `credentials` (預設路徑: `./credentials.json`)

### [PDM](https://pdm.fming.dev) (Recommended)

Clone the repository

```bash
  git clone https://github.com/screenshot-media-toolkit/instagram-scene-detection.git
```

Download dependencies

```bash
  pdm install --prod
```

Run the application

```bash
  pdm run start /path/to/images
```

### `PIP` + `Venv`

Clone the repository

```bash
  git clone https://github.com/screenshot-media-toolkit/instagram-scene-detection.git
```

Create a virtual environment

```bash
  python3 -m venv .venv
```

Activate the environment

```bash
  source .venv/bin/activate
```

Download dependencies

```bash
  pip install -r requirements.txt
```

Run the application

```bash
  python3 src/scene_detection /path/to/images
```

## Usage

```
Usage: python -m scene_detection [OPTIONS] INPUT

  Detect the scene of input image.

  Given an Instagram screenshot, classify the scene of the image to homepage,
  story, comment, external link or reels, and write the results into a CSV
  file.

  INPUT is the path to the Instagram screenshot, either image file or
  directory.

Options:
  -o, --output PATH  Output CSV file
  --help             Show this message and exit.
```

## Configuration

設定檔為 `settings.toml` 可調整的參數有:

- prediction:

  - `confidence_threshold: float` Darknet 中可輸出 label 的最低信心值，不可為 0 (default: `0.01`)
  - `invisible_percentage: float` 截圖中不可視範圍的百分比 (default: `0.13`)

- model:

  - `metadata_path: Path` model metadata 的路徑 (default: `"yolov3.data"`)
  - `config_path: Path` model config 的路徑 (default: `"yolov3.cfg"`)
  - `weights_path: Path` model weights 的路徑 (default: `"yolov3.weights"`)

- ocr-api:

  - `credentials_path: Path` Google Cloud Vision API credentials 的路徑 (default: `"credentials.json"`)

- scene detectors:

  - comment:

    - `acceptable_range: float` 出現 "留言" / "comment" 標題的可接受位置最大百分比 (手機上方為 0) (default: `0.15`)

  - homepage:

    - `confidence_divisor: float` 文字及標籤信心值加總後除的分母 (default: `3`)
    - `labels: string[]` 在 homepage 出現的圖樣的標籤 (default: `["ins_logo", "icon_nav", "icon_msg", "icon_bookmark"]`)

  - external:

    - `confidence_divisor: float` 文字及標籤信心值加總後除的分母 (default: `3`)
    - `labels: string[]` 在 external link 出現的圖樣的標籤 (default: `["external_close", "external_info"]`)

  - reels:

    - `text_confidence: float` 出現 "連續短片" / "reels" 所增加的總信心值 (default: `0.15`)
    - `acceptable_range: float` 出現 "連續短片" / "reels" 標題的可接受位置最大百分比 (default: `0.2`)
    - `labels` 在 reels 出現的圖樣的標籤，包含信心值的倍率及出現位置 (See `settings.toml` for more details)

## Labels

- `ins_logo`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/jYhfJ59.png" alt="instagram-logo-light" height="50" />
    <img src="https://i.imgur.com/1y6NCXA.png" alt="instagram-logo-dark" height="50" />
  </div>

- `icon_nav`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/MWGde83.png" alt="instagram-nav-light" height="50" />
    <img src="https://i.imgur.com/F9ecWaG.png" alt="instagram-nav-dark" height="50" />
  </div>

- `icon_msg`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/YZUtuse.png" alt="instagram-message-light" height="50" />
    <img src="https://i.imgur.com/4XbYFa7.png" alt="instagram-message-dark" height="50" />
  </div>

- `icon_bookmark`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/F67Xabi.png" alt="instagram-bookmark-light" height="50" />
    <img src="https://i.imgur.com/qMhxTUZ.png" alt="instagram-bookmark-dark" height="50" />
  </div>

- `reels_action`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/Pw7Q8NE.png" alt="instagram-reels-acion" height="150" />
  </div>

- `reels_camera`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/vZcHmqp.png" alt="instagram-reels-camera" height="50" />
  </div>

- `external_close`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/p2bOUk6.png" alt="instagram-extenal-close-cross" height="50" />
  </div>

- `external_info`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/4PVoPQI.png" alt="instagram-external-info" height="50" />
  </div>

- `profile_back`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/xSChuGq.png" alt="instagram-profile-back-arrow" height="50" />
  </div>

- `profile_options`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/ixMUYJF.png" alt="instagram-profile-options" height="50" />
  </div>

- `border_options`

  <div style="display: flex; gap: 1rem">
    <img src="https://i.imgur.com/ooFQraf.png" alt="instagram-border-options-light" height="50" />
    <img src="https://i.imgur.com/2ASUo9e.png" alt="instagram-border-options-dark" height="50" />
  </div>
