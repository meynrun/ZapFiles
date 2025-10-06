![ZapFiles](./assets/ZapFiles-banner.png)

---

<!-- TOC -->

* [🧾 О проекте](#-о-проекте)
* [🖥️ Платформа и лицензия](#-платформа-и-лицензия)
* [🌐 Языки](#-языки)
* [⬇️ Скачать](#-скачать)
* [📦 Установка из исходников](#-установка-из-исходников)
* [🛠️ Сборка установщика (Windows)](#-сборка-установщика-windows)
* [⚙️ Конфигурация](#-конфигурация)

<!-- TOC -->

---

## 🧾 О проекте

**ZapFiles** — это удобный и безопасный инструмент для передачи файлов с использованием сквозного шифрования.

---

## 💻 Платформа и лицензия

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)
[![Лицензия](https://img.shields.io/github/license/Ileriayo/markdown-badges?style=for-the-badge)](./LICENSE)

---

## 💾 Языки

[![English](https://img.shields.io/badge/English-0078D4?style=for-the-badge&logo=download&logoColor=white)](./README.md)
[![Русский](https://img.shields.io/badge/Русский-D52B1E?style=for-the-badge&logo=download&logoColor=white)](./README-ru.md)

---

## ⬇️ Скачать

[![Последняя сборка](https://img.shields.io/badge/Скачать%20последнюю%20версию-66CC00?style=for-the-badge&logo=download&logoColor=white)](https://github.com/meynrun/ZapFiles/releases/latest/download/Setup-x64.exe)

---

## 📦 Установка из исходников

> **Примечание:** если `uv` не установлен, следуйте инструкции: [astral.sh/uv](https://github.com/astral-sh/uv)

1. Клонируйте репозиторий:

```sh
git clone https://github.com/meynrun/ZapFiles.git
cd ZapFiles
```

2. Создайте виртуальное окружение и активируйте его:

```sh
uv venv
```

3. Установите зависимости:

```sh
uv sync
```

---

## 🔨 Сборка установщика (Windows)

1. Установите [Inno Setup](https://jrsoftware.org/download.php/is.exe)
2. Запустите скрипт сборки:

```sh
uv run build.py
```

Скрипт соберёт ZapFiles в директорию `.\dist\` и установочный `Setup-x64.exe` в директорию `.\Output\` с помощью Inno
Setup.

---

## 🔧 Конфигурация

|        Ключ         |   Тип   | Описание                                       |     Допустимые значения      |             По умолчанию              |
|:-------------------:|:-------:|:-----------------------------------------------|:----------------------------:|:-------------------------------------:|
| `check_for_updates` | boolean | Автоматическая проверка обновлений при запуске |       `true`, `false`        |                `true`                 |
|     `language`      | string  | Язык интерфейса ZapFiles                       |      `auto`, `en`, `ru`      |                `auto`                 |
|   `enable_emojis`   | boolean | Использовать ли эмодзи в интерфейсе            |       `true`, `false`        |                `true`                 |
|    `clear_mode`     | string  | Метод очистки экрана                           | `ASCII`, `ASCII2`, `command` |                `ASCII`                |
|   `download_path`   | string  | Путь к папке загрузок                          |       абсолютный путь        | `%user%/Downloads/ZapFiles Downloads` |
|    `enable_tips`    | boolean | Включить советы                                |       `true`, `false`        |                `true`                 |

---
