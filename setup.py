from pathlib import Path
from setuptools import setup
import subprocess
from git import Repo
import os
from tempfile import TemporaryDirectory


with TemporaryDirectory() as dir:
    dir = Path(dir)
    bdir = (dir / "build")
    Repo.clone_from("https://github.com/eclipse-cyclonedds/cyclonedds.git", to_path=dir)
    bdir.mkdir()

    subprocess.check_call([
        'cmake',
        '-DENABLE_TOPIC_DISCOVERY=ON',
        '-DENABLE_TYPE_DISCOVERY=ON',
        f"-DCMAKE_INSTALL_PREFIX={os.environ['CYCLONEDDS_HOME']}",
        '..'
    ], cwd=bdir)

    subprocess.check_call([
        'cmake',
        '--build', '.',
        '--target', 'install',
        '--parallel'
    ], cwd=bdir)


setup(
    name="cyclonedds_bootstrapped",
    py_modules=['cyclonedds_bootstrapped'],
    install_requires=[
        "cyclonedds @ git+https://github.com/eclipse-cyclonedds/cyclonedds-python.git"
    ]
)

