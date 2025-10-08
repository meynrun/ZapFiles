import os
import shutil
import stat
import subprocess
import sys
import time
from pathlib import Path

import questionary

from zapfiles.constants import VERSION

INNO_SETUP_PATH = "C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe"
ISS_FILE = ".\\setup_script.iss"


def remove_readonly(func, path, _):
    os.chmod(path, stat.S_IWRITE)
    func(path)


def rmdir(path: str) -> None:
    if os.path.exists(path):
        shutil.rmtree(path, onerror=remove_readonly)


def create_version_file(version: str, output_path: str) -> str:
    """Создаёт временный файл версии для PyInstaller."""
    # Убедимся, что директория output_path существует
    os.makedirs(output_path, exist_ok=True)

    version_content = f"""
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers=({version.replace(".", ", ")}, 0),
    prodvers=({version.replace(".", ", ")}, 0),
    mask=0x3f,
    flags=0x0,
    OS=0x40004,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
  ),
  kids=[
    StringFileInfo(
      [
        StringStruct('CompanyName', 'Meynrun'),
        StringStruct('FileDescription', 'ZapFiles'),
        StringStruct('FileVersion', '{version}'),
        StringStruct('ProductName', 'ZapFiles'),
        StringStruct('ProductVersion', '{version}'),
        StringStruct('OriginalFilename', 'ZapFiles.exe')
      ]
    ),
    VarFileInfo([VarStruct('Translation', [0x0409, 1252])])
  ]
)
"""
    version_file = os.path.join(output_path, "version.txt")
    with open(version_file, "w", encoding="utf-8") as f:
        f.write(version_content)
    return version_file


def main():
    print("Building " + VERSION)
    print(
        "Before building an update make sure you changed version in zapfiles/constants/__init__.py, pyproject.toml and in setup_script.iss!"
    )
    build_dir = "./dist"

    rmdir(build_dir)

    if sys.prefix == sys.base_prefix:
        print("Please activate the virtual environment first.")
        sys.exit(1)

    # Determine the path to the pyinstaller executable in the virtual environment
    venv_scripts_dir = Path(sys.prefix) / "Scripts"
    pyinstaller_executable = (
        venv_scripts_dir / "pyinstaller"
        if os.name == "nt"
        else venv_scripts_dir / "pyinstaller"
    )
    pyinstaller_executable = pyinstaller_executable.with_suffix(
        ".exe" if os.name == "nt" else ""
    )

    try:
        # Check if pyinstaller is accessible by running it directly
        subprocess.run(
            [str(pyinstaller_executable), "--version"],
            check=True,
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        print(
            f"PyInstaller is not installed or not found at {pyinstaller_executable}. Please install it in the virtual environment."
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running PyInstaller: {e.stderr}")
        sys.exit(1)

    command = [
        str(pyinstaller_executable),
        Path("zapfiles") / "__main__.py",
        "--distpath=dist",
        "--workpath=build",
        "--noconfirm",
        "--log-level=INFO",
    ]

    if os.name == "nt":
        # Создаём временный файл версии
        version_file = create_version_file(VERSION, build_dir)
        command.extend(
            [
                "--icon=./assets/ZapFiles-icon.ico",
                f"--version-file={version_file}",
                "--name=zapfiles",
                "--add-data=lang;lang",
            ]
        )

    # PyInstaller не поддерживает опцию --jobs, поэтому она исключена
    print(f"Compiling {VERSION} using PyInstaller.")
    start_time = time.perf_counter()
    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"Compilation failed: {result.stderr}")
        sys.exit(1)
    else:
        print(
            f"Compilation successful! It took {time.perf_counter() - start_time} seconds."
        )

    # # Копирование локализаций (на случай, если --add-data не сработал)
    # localization_dir = "./lang"
    # target_lang_dir = os.path.join(build_dir, "ZapFiles", "lang")
    #
    # os.makedirs(target_lang_dir, exist_ok=True)
    #
    # try:
    #     shutil.copytree(localization_dir, target_lang_dir, dirs_exist_ok=True)
    #     print("Localization files copied successfully!")
    # except Exception as e:
    #     print(f"Failed to copy localization files: {e}")
    #     sys.exit(1)

    # Удаление временной папки build
    rmdir("./build")

    if os.name == "nt":
        build_setup = questionary.confirm("Build a setup using InnoSetup script?").ask()

        if build_setup:
            start_time = time.perf_counter()
            result = subprocess.run([INNO_SETUP_PATH, ISS_FILE])
            if result.returncode != 0:
                print(f"Inno setup build failed: {result.stderr}")
                sys.exit(1)
            else:
                print(
                    f"Inno setup build successful! It took {time.perf_counter() - start_time} seconds."
                )

    # Удаление временного файла версии
    if os.name == "nt" and os.path.exists(version_file):
        os.remove(version_file)


if __name__ == "__main__":
    main()
