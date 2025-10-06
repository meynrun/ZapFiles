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

    # Determine the path to the nuitka executable in the virtual environment
    venv_scripts_dir = Path(sys.prefix) / "Scripts"
    nuitka_executable = (
        venv_scripts_dir / "nuitka" if os.name == "nt" else venv_scripts_dir / "nuitka"
    )
    nuitka_executable = nuitka_executable.with_suffix(".cmd" if os.name == "nt" else "")

    try:
        # Check if nuitka is accessible by running it directly
        subprocess.run(
            [str(nuitka_executable), "--version"],
            check=True,
            capture_output=True,
            text=True,  # Ensure output is decoded as text
        )
    except FileNotFoundError:
        print(
            f"Nuitka is not installed or not found at {nuitka_executable}. Please install it in the virtual environment."
        )
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error running Nuitka: {e.stderr}")
        sys.exit(1)

    command = [
        str(nuitka_executable),  # Use the explicit path to nuitka
        "zapfiles",
        "--standalone",
        "--no-pyi-file",
        "--output-dir=dist",
        "--show-progress",
    ]

    if os.name == "nt":
        command.extend(
            [
                "--windows-icon-from-ico=./assets/ZapFiles-icon.ico",
                "--windows-product-name=ZapFiles",
                "--windows-company-name=Meynrun",
                f"--windows-file-version={VERSION}",
                f"--windows-product-version={VERSION}",
            ]
        )

    while True:
        compiler = (
            questionary.select(
                "What compiler would you like to use?",
                choices=[
                    "Default",
                    "Clang",
                    "MinGW64",
                    "MSVC=latest",
                ],
            )
            .ask()
            .lower()
        )

        if compiler:
            if compiler != "default":
                command.extend([f"--{compiler}"])
            break

    while True:
        try:
            jobs = int(
                questionary.text(
                    "How many jobs would you like to run?",
                ).ask()
            )

            if jobs < 1:
                raise ValueError
            else:
                command.extend([f"--jobs={jobs}"])
                break
        except ValueError:
            print("Please enter a valid number.")

    print(f"Compiling {VERSION} using {compiler} compiler.")
    start_time = time.perf_counter()
    result = subprocess.run(command)

    if result.returncode != 0:
        print(f"Compilation failed: {result.stderr}")
        sys.exit(1)
    else:
        print(
            f"Compilation successful! It took {time.perf_counter() - start_time} seconds."
        )

    localization_dir = "./lang"
    target_lang_dir = os.path.join(build_dir, "zapfiles.dist", "lang")

    os.makedirs(target_lang_dir, exist_ok=True)

    try:
        shutil.copytree(localization_dir, target_lang_dir, dirs_exist_ok=True)
        print("Localization files copied successfully!")
    except Exception as e:
        print(f"Failed to copy localization files: {e}")
        sys.exit(1)

    rmdir(os.path.join(build_dir, "zapfiles.build"))

    try:
        shutil.copytree(
            f"{os.path.join(build_dir, 'zapfiles.dist')}", build_dir, dirs_exist_ok=True
        )
        print("Compiled distribution files copied successfully!")
    except Exception as e:
        print(f"Failed to copy localization files: {e}")
        sys.exit(1)

    rmdir(os.path.join(build_dir, "zapfiles.dist"))

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


if __name__ == "__main__":
    main()
