import os
import shutil
import stat
import subprocess
import sys

VERSION = "1.9.0"
INNO_SETUP_PATH = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
ISS_FILE = ".\setup_script.iss"


def remove_readonly(func, path, _):
    """Сбрасывает атрибут 'только чтение' и повторяет удаление."""
    os.chmod(path, stat.S_IWRITE)
    func(path)

def rmdir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path, onerror=remove_readonly)


def main():
    build_dir = "./dist"

    rmdir(build_dir)

    # Проверяем, что скрипт выполняется из venv
    if sys.prefix == sys.base_prefix:
        print("Please activate the virtual environment first.")
        sys.exit(1)

    # Проверяем, установлен ли Nuitka
    try:
        subprocess.run(["nuitka", "--version"], shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        print("Nuitka is not installed. Please install it first.")
        sys.exit(1)

    # Формируем команду компиляции
    command = [
        "nuitka",
        "./main.py",
        "--onefile",
        "--standalone",
        "--no-pyi-file",
        "--output-dir=dist",
        "--jobs=8",
        "--show-progress",
        "--windows-icon-from-ico=./assets/ZapFiles-icon.ico",
        "--windows-product-name=ZapFiles",
        "--windows-company-name=MeynDev",
        f"--windows-file-version={VERSION}",
        f"--windows-product-version={VERSION}"
    ]

    # Запускаем компиляцию
    result = subprocess.run(command, shell=True)

    if result.returncode != 0:
        print("Compilation failed!")
        sys.exit(1)
    else:
        print("Compilation successful!")

    localization_dir = "./lang"
    target_lang_dir = os.path.join(build_dir, "lang")

    # Создаем новую папку lang
    os.makedirs(target_lang_dir, exist_ok=True)

    # Копируем локализационные файлы
    try:
        shutil.copytree(localization_dir, target_lang_dir, dirs_exist_ok=True)
        print("Localization files copied successfully!")
    except Exception as e:
        print(f"Failed to copy localization files: {e}")
        sys.exit(1)

    result = subprocess.run([INNO_SETUP_PATH, ISS_FILE], shell=True)
    if result.returncode != 0:
        print("Inno setup build failed!")
        sys.exit(1)
    else:
        print("Inno setup build successful!")

    print("Setup compiled successfully!")


if __name__ == "__main__":
    main()
