import os
import datetime
import time
from tqdm import tqdm
from tqdm._tqdm import trange
from pathlib import Path
import PIL
from PIL import Image
from PIL.ExifTags import TAGS

import exifread

source = 'D:/Pictures/Jpeg2'
target = 'N:/bakphoto'

try:
    O_BINARY = os.O_BINARY
except:
    O_BINARY = 0
READ_FLAGS = os.O_RDONLY | O_BINARY
WRITE_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_TRUNC | O_BINARY
BUFFER_SIZE = 128 * 1024

def copyfile(src, dst):
    try:
        fin = os.open(src, READ_FLAGS)
        stat = os.fstat(fin)
        fout = os.open(dst, WRITE_FLAGS, stat.st_mode)
        for x in iter(lambda: os.read(fin, BUFFER_SIZE),""):
            os.write(fout, x)
    finally:
        try: os.close(fin)
        except:
            print('except1:')
            pass
        try: os.close(fout)
        except:
            print('except2:')
            pass

def copy2(src,dst):
    blocksize = 65536
    with open(src, "rb") as f , open(dst, 'wb') as w:
        for block in iter(lambda: f.read(blocksize), b""):
            w.write(block)


def TimeStampToTime(timestamp):
    timeStruct = time.localtime(timestamp)
    return time.strftime('%Y-%m-%d %H:%M:%S', timeStruct)


def build_dup_dict(dir_path, pattern='*'):
    p = Path(dir_path)
    fList  = list(p.glob('**/' + pattern))
    size = len(fList)
    print("all files: {}".format(size))
    bar = tqdm(fList)
    count = 0
    for item in bar:
        count += 1
        showLog = False


        if int(count) % int(100) == 0:
            #print("copy : {}% time:{}".format(count*100/size,TimeStampToTime(time.time())))
            showLog = True
        else:
            showLog = False
        file = str(item)
        #print("check: {}".format(file))
        if os.path.isdir(file):
            print("jump peth: {}".format(file))
        else:
            # 过滤文件类型

            filetype = os.path.splitext(file)[-1]
            #if  filetype != ".Jpeg":
            #    print("文件类型不拷贝: {}".format(filetype))
            #    continue
            # 判断文件大小
            filetime = time.localtime(os.path.getctime(file))
            fsize = os.path.getsize(file)/(1024*1024)
            #print("file: {} size:{}MB check:{}".format(file,fsize,fsize>50))
            #p = exifread.process_file(open(file, 'rb'))
            #print("文件信息：{}".format(p))
            try:
                img = Image.open(file)
                img_exif = img.getexif()
                filetime = time.strptime(img_exif[36867], '%Y:%m:%d %H:%M:%S')

                #print("文件信息2：{}".format(img_exif))
            except BaseException  as e:
                #print('no exif:', e)
                pass

            # 文件复制到指定地址
            filepath = target + "/" + time.strftime('%Y', filetime) + "/" + time.strftime('%Y-%m-%d', filetime) + "/"
            filedest = filepath + file.split("\\")[-1]


            if not os.path.exists(filepath):
                os.makedirs(filepath)
            if not os.path.exists(filedest):
                if fsize > 50:
                    print("文件过大 转换格式保存: {} new:{}".format(file, filedest))
                    try:
                        img.save(filedest)
                    except BaseException  as e:
                        print('文件转换失败 file:{}'.format(file), e)
                        pass
                else:copy2(file, filedest)
                #if(showLog):print("文件拷贝：{} {}".format(file,filedest))
            else:
                pass
                #if(showLog):print("文件已在：{}".format(filedest))

def main():
    print("字典：{}".format(TAGS))
    build_dup_dict(source)
    print("finish :{}".format(TimeStampToTime(time.time())))


if __name__ == '__main__':
    main()
