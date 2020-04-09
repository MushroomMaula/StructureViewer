import json
import os
import pathlib
import platform
import re
from distutils.version import StrictVersion
from zipfile import ZipFile


def get_minecraft_path():
    name = platform.system()
    if name == 'Linux':
        path = '~/.minecraft'
    elif name == 'Darwin':
        path = '~/Library/Application Support/minecraft'
    elif name == 'Windows':
        path = os.path.join(os.environ['APPDATA'], '.minecraft')
    else:
        path = None

    return pathlib.Path(path).absolute()


def get_latest_jar():
    path = get_minecraft_path()
    assert path.is_dir()
    pattern = re.compile(r'^(\d+(?:\.\d+)+)', re.M)

    versions = path / 'versions'
    # grab the actual versions from the folder names
    version_names = '\n'.join(os.listdir(versions))
    jars = sorted(pattern.findall(version_names), key=StrictVersion, reverse=True)

    # find the absolute path to the actual jar
    jar_path = versions.rglob(f'{jars[0]}*.jar')
    # return the first object of the generator
    return next(jar_path)


def extract_textures(jar_file):
    with ZipFile(jar_file) as z:
        for info in z.infolist():
            if r'assets/minecraft/textures' in info.filename:
                # we truncate assets/minecraft/textures as
                # we dont need these folders
                info.filename = info.filename[26:]
                z.extract(info, 'textures')


def extract_block_models(jar_file):
    with ZipFile(jar_file) as z:
        for info in z.infolist():
            if r'assets/minecraft/models' in info.filename:
                info.filename = info.filename[23:]
                z.extract(info, 'models')


def load_json(fp):
    path = os.path.abspath(fp)
    if not path.endswith('.json'):
        path += '.json'
    with open(path, 'r') as f:
        return json.load(f)


def get_odd_even(lst):
    odd = []
    even = []
    for idx, item in enumerate(lst):
        if idx % 2 == 0:
            even.append(item)
        else:
            odd.append(item)
    return even, odd


if __name__ == '__main__':
    file = get_latest_jar()
    extract_textures(file)
    extract_block_models(file)
