import hashlib
import time
import filecmp
import functools
import datetime
import os
from pathlib import Path
from tqdm import tqdm
from tqdm._tqdm import trange
import PIL
from PIL import Image
from PIL.ExifTags import TAGS

dup = {}
photo_path = 'D:\Pictures'


def md5sum(filename, blocksize=65536):
    hash = hashlib.md5()
    with open(filename, "rb") as f:
        for block in iter(lambda: f.read(blocksize), b""):
            hash.update(block)
    return hash.hexdigest()


'''把时间戳转化为时间: 1479264792 to 2016-11-16 10:53:12'''


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def build_dup_dict(dir_path, pattern='*'):
    def save(file):
        hash = md5sum(file)
        if hash not in dup.keys():
            dup[hash] = [file]
        else:
            dup[hash].append(file)

    p = Path(dir_path)
    for item in tqdm(list(p.glob('**/' + pattern))):
        file = str(item)
        if os.path.isdir(file):
           print("jump peth: {}",file)
        else:
            save(file)


def cmp(a, b):
    if b < a:
        return -1
    if a < b:
        return 1
    return 0


def main():
    def get_duplicate():
        return {k: v for k, v in dup.items() if len(v) > 1}

    build_dup_dict(photo_path)

    for hash, files in tqdm(list(get_duplicate().items())):
        files = sorted(files, key=lambda x: os.path.getctime(x), reverse=False)
        #当第一个文件位于bakphoto，将其后移，优先删除
        if ("bakphoto" in files[0]):
            tmp = files[0]
            files[0] = files[1]
            files[1] = tmp
        print("same files: {} {}".format(hash, files))
        for file in files[1:]:
            if filecmp.cmp(files[0], file):
                print("delete {}: {}".format(file, TimeStampToTime(os.path.getctime(file))))
                os.remove(file)
            else:
                print("not same {}: {}".format(files[0],file))


if __name__ == '__main__':
    main()
