![ZapFiles](./assets/ZapFiles-banner.png)

---

<!-- TOC -->
  * [🧾 About the Project](#-about-the-project)
  * [🖥️ Platform & License](#-platform--license)
  * [🌐 Languages](#-languages)
  * [⬇️ Download](#-download)
  * [📦 Installing from Source](#-installing-from-source)
  * [🛠️ Building the Installer (Windows)](#-building-the-installer-windows)
  * [⚙️ Configuration](#-configuration)
<!-- TOC -->

---

## 🧾 About the Project

**ZapFiles** is a simple and secure file transfer tool that ensures your privacy through end-to-end encryption.

---

## 🖥️ Platform & License

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
[![License](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

---

## 🌐 Languages

[![English](https://img.shields.io/badge/English-0078D4?style=for-the-badge&logo=download&logoColor=white)](./README.md)
[![Русский](https://img.shields.io/badge/Русский-D52B1E?style=for-the-badge&logo=download&logoColor=white)](./README-ru.md)

---

## ⬇️ Download

[![Latest Release](https://img.shields.io/badge/Download%20Latest%20Version-66CC00?style=for-the-badge&logo=download&logoColor=white)](https://github.com/meynrun/ZapFiles/releases/latest/download/Setup-x64.exe)

---

## 📦 Installing from Source

> **Note:** If `uv` is not installed, follow the instructions here: [astral.sh/uv](https://github.com/astral-sh/uv)

1. Clone the repository:
```sh
git clone https://github.com/meynrun/ZapFiles.git
cd ZapFiles
````

2. Create and activate a virtual environment:

```sh
uv venv
```

3. Install dependencies:

```sh
uv sync
```

---

## 🛠️ Building the Installer (Windows)

1. Install [Inno Setup](https://jrsoftware.org/download.php/is.exe)
2. Run the build script:

```sh
uv run build.py
```

The script will build ZapFiles into the `./dist/` directory, and the installer `Setup-x64.exe` will be placed in the `./Output/` directory using Inno Setup.

---

## ⚙️ Configuration

|         Key         |  Type   | Description                                |        Allowed Values        |             Default Value             |
|:-------------------:|:-------:|:-------------------------------------------|:----------------------------:|:-------------------------------------:|
| `check_for_updates` | boolean | Automatically check for updates on launch  |       `true`, `false`        |                `true`                 |
|     `language`      | string  | Interface language                         |      `auto`, `en`, `ru`      |                `auto`                 |
|   `enable_emojis`   | boolean | Whether to display emojis in the interface |       `true`, `false`        |                `true`                 |
|    `clear_mode`     | string  | Console clear method                       | `ASCII`, `ASCII2`, `command` |                `ASCII`                |
|   `download_path`   | string  | Path to the download folder                |        absolute path         | `%user%/Downloads/ZapFiles Downloads` |

---
