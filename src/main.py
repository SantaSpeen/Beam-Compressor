import asyncio
import multiprocessing
import os
import shutil
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from zipfile import ZipFile, ZIP_DEFLATED

import aiofiles
from PIL import Image

counter = 0
ready = 0
st0 = 0


# Image.ID.append("BC4U")


async def _unzip(extract_to, zip_file, file_info):
    file_name = file_info.filename
    file_content = await asyncio.to_thread(zip_file.read, file_info)
    path = f"{extract_to}/{file_name}"
    if ((path.endswith("/") or os.path.isdir(path)) and not os.path.exists(path)) or not os.path.exists(
            os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))
    elif not os.path.exists(path):
        async with aiofiles.open(path, "wb") as f:
            await f.write(file_content)


async def unzip_archive(zip_file_path: str, extract_to: str):
    zip_file = ZipFile(zip_file_path)
    wt = []
    for file_info in zip_file.infolist():
        t = asyncio.create_task(_unzip(extract_to, zip_file, file_info))
        wt.append(t)
    await asyncio.gather(*wt)
    zip_file.close()


def zip_archive(file_paths, archive_name, unzip_path):
    with ZipFile(archive_name, mode='w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
        for file_path in file_paths:
            archive.write(os.path.join(unzip_path, file_path), file_path)
        archive.close()


async def compress_file(file_path):
    try:
        ext = file_path[-3].lower()
        image = Image.open(file_path)
        resize_cof = 0.8
        sizes = {16384: 4, 8192: 4, 4096: 2, 2048: 2, 1024: 2, 512: 2}
        if min(image.size) >= 513:
            x, y = image.size[0], image.size[1]
            vxy = sizes.keys()
            if x in vxy and y in vxy:
                image = image.reduce(sizes[x])
            else:
                new_size = (round(resize_cof * x), round(resize_cof * y))
                image = image.resize(new_size, resample=Image.Resampling.HAMMING, reducing_gap=1.5)
        match ext:
            case "png":
                image.save(file_path, format="PNG", compresslevel=9)
            case "jpg":
                image.save(file_path, format="JPEG", optimize=True, quality=25)
            # case "dds":
            #     image.save(buffer, format="DDS")
            case _:
                image.save(file_path)
        image.close()
    except NotImplementedError:
        # Файлы, которые не может обработать PIL
        pass
    except Exception as e:
        print(f"Error in {file_path}: {e}")
        # traceback.print_exc()


async def compress_files(unzip_path):
    loop = asyncio.get_event_loop()
    wt = []
    all_files = []
    for path, names, files in os.walk(unzip_path):
        for file in files:
            ext = file[-3:].lower()
            if ext in ('txt', 'pdn', 'ini'):
                continue
            file_path = os.path.join(path, file)
            if ext in ('jpg', 'png'):  # , "dds"):
                t = loop.create_task(compress_file(file_path))
                wt.append(t)
            all_files.append(os.path.relpath(file_path, unzip_path))
        for dir in names:
            dir_path = os.path.join(path, dir)
            all_files.append(os.path.relpath(dir_path, unzip_path))

    await asyncio.gather(*wt)
    return all_files


async def worker(name, loop):
    global counter, ready
    counter += 1
    c = counter
    try:

        mods_path = "mods/" + name
        unzip_path = "../../unzip/" + name[:-4]
        zip_path = "zip/" + name
        os.mkdir(unzip_path)
        s = round(os.path.getsize(mods_path) / (1024 * 1024), 2)
        print(f"[{c:<2}] Started: {name}")

        st = time.monotonic_ns()
        await unzip_archive(mods_path, unzip_path)
        z = round((time.monotonic_ns() - st) / 1000000000, 2)
        # print(f"[{c:<2}] Ready unzip_archive")

        st = time.monotonic_ns()
        all_files = await compress_files(unzip_path)
        cs = round((time.monotonic_ns() - st) / 1000000000, 2)
        # print(f"[{c:<2}] Ready compress_files")

        st = time.monotonic_ns()
        zip_archive(all_files, zip_path, unzip_path)
        uz = round((time.monotonic_ns() - st) / 1000000000, 2)

        shutil.rmtree(unzip_path)
        sz = round(os.path.getsize(zip_path) / (1024 * 1024), 2)
        te = round((time.monotonic_ns() - st0) / 1000000000, 2)
        ready += 1
        print(f"[{c:<2}] [from_start={te:>8}s] [wait {counter - ready:<2}] | "
              f"[unzip {z:>6}s] -> [compress {cs:>6}s] -> [zip {uz:>6}s] [{s:>6}mb -> {sz:>6}mb]: {name}")
    except Exception as e:
        ready += 1
        print(f"[{c:<2}] Exception: {e}")
        traceback.print_exc()
    loop.stop()


def _worker(name):
    loop = asyncio.new_event_loop()
    asyncio.run_coroutine_threadsafe(worker(name, loop), loop)
    loop.run_forever()


def main():
    global st0
    st = time.monotonic_ns()
    asyncio.set_event_loop(asyncio.new_event_loop())
    if os.path.exists("zip"):
        shutil.rmtree("zip")
    os.mkdir("zip")
    if os.path.exists("../../unzip"):
        shutil.rmtree("../../unzip")
    os.mkdir("../../unzip")
    names = []
    size = 0
    for name in os.listdir("mods"):
        if os.path.isfile("mods/" + name) and name.endswith(".zip"):
            size += os.path.getsize("mods/" + name)
            names.append(name)
    num_cores = multiprocessing.cpu_count()
    print(f"Starting process on {len(names)} files, {size / (1024 ** 2):.2f}mb, cores {num_cores}...")
    st0 = time.monotonic_ns()
    with ThreadPoolExecutor(max_workers=num_cores) as ex:
        for name in names:
            ex.submit(_worker, name)
    size = sum(os.path.getsize(os.path.join("zip", name)) for name in os.listdir("zip"))
    print(f"Work: {round((time.monotonic_ns() - st) / 1000000000, 4)}s, new size: {size / (1024 ** 2):.2f}mb")


if __name__ == '__main__':
    main()