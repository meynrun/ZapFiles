import os
import shutil
import stat
import subprocess
import sys

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
        "Before building an update make sure you changed version in zapfiles/constants/__init__.py and in setup_script.iss!"
    )
    build_dir = "./dist"

    rmdir(build_dir)

    if sys.prefix == sys.base_prefix:
        print("Please activate the virtual environment first.")
        sys.exit(1)

    try:
        subprocess.run(
            ["nuitka", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError:
        print("Nuitka is not installed. Please install it first.")
        sys.exit(1)

    command = [
        "nuitka",
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

    result = subprocess.run(command)

    if result.returncode != 0:
        print("Compilation failed!")
        sys.exit(1)
    else:
        print("Compilation successful!")

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
        print("Localization files copied successfully!")
    except Exception as e:
        print(f"Failed to copy localization files: {e}")
        sys.exit(1)

    rmdir(os.path.join(build_dir, "zapfiles.dist"))

    if os.name == "nt":
        build_setup = questionary.confirm("Build a setup using InnoSetup script?")

        if build_setup:
            result = subprocess.run([INNO_SETUP_PATH, ISS_FILE])
            if result.returncode != 0:
                print("Inno setup build failed!")
                sys.exit(1)
            else:
                print("Inno setup build successful!")

            print("Setup compiled successfully!")


if __name__ == "__main__":
    main()
