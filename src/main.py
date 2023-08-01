import asyncio
import multiprocessing
import os
import platform
import shutil
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from zipfile import ZipFile, ZIP_DEFLATED

import aiofiles
from PIL import Image

mods_old = "mods/"
mods_new = "zip/"
tmp = "../../unzip/"

mods_counter = 0
work_counter = 0
prog_counter = 0
redy_counter = 0
st0 = 0


class Mod:

    def __init__(self, name):
        self.name = name
        self.loop = None
        self.mod_path = mods_old + name
        self.tmp_path = tmp + name[:-4]
        self.zip_path = mods_new + name
        os.mkdir(self.tmp_path)
        self.files_list = []

    async def unzip(self):

        async def unzip_file(file, info):
            path = f"{self.tmp_path}/{info.filename}"
            if ((path.endswith("/") or os.path.isdir(path)) and not os.path.exists(path)) or not os.path.exists(
                    os.path.dirname(path)):
                os.makedirs(os.path.dirname(path))
            elif not os.path.exists(path):
                file_content = await asyncio.to_thread(file.read, info)
                async with aiofiles.open(path, "wb") as f:
                    await f.write(file_content)

        with ZipFile(self.mod_path, "r") as zip_file:
            tasks = [self.loop.create_task(unzip_file(zip_file, file_info)) for file_info in zip_file.infolist()]
            await asyncio.gather(*tasks)

    async def zip(self):
        async def zip_file(file_path, arch):
            arch.write(os.path.join(self.tmp_path, file_path), file_path)

        with ZipFile(self.zip_path, mode='w', compression=ZIP_DEFLATED, compresslevel=9) as archive:
            tasks = [self.loop.create_task(zip_file(file_path, archive)) for file_path in self.files_list]
            await asyncio.gather(*tasks)

    async def compress(self):

        # noinspection PyUnresolvedReferences
        async def compress_file(file_path, is_preview):
            try:
                ext = file_path[-4].lower()
                filename = os.path.basename(file_path).lower()
                if filename in ("_n.", "_nr", ".no"):
                    return
                image = Image.open(file_path)
                resize_cof = 0.8
                sizes = {16384: 4, 8192: 4, 4096: 2, 2048: 2, 1024: 2, 512: 2}
                if is_preview:
                    preview_size = (500, 281)
                    real_size = image.size
                    if real_size[0] > preview_size[0] or real_size[1] > preview_size[1]:
                        image = image.resize(preview_size, resample=Image.Resampling.HAMMING, reducing_gap=1.5)
                else:
                    if min(image.size) > 512:
                        x, y = image.size[0], image.size[1]
                        vxy = sizes.keys()
                        if x in vxy and y in vxy:
                            image = image.reduce(sizes[x])
                        else:
                            new_size = (round(resize_cof * x), round(resize_cof * y))
                            image = image.resize(new_size, resample=Image.Resampling.HAMMING, reducing_gap=1.5)
                match ext:
                    case ".png":
                        image.save(file_path, format="PNG", compresslevel=9)
                    case ".jpg":
                        image.save(file_path, format="JPEG", optimize=True, quality=25)
                    case _:
                        image.save(file_path)
                image.close()
            except NotImplementedError:
                # Файлы, которые не может обработать PIL
                pass
            except Exception as e:
                print(f"Error in {file_path}: {e}")

        tasks = []
        for path, names, files in os.walk(self.tmp_path):
            if "mod_info/" in path:
                continue
            for file in files:
                _ext = file[-3:].lower()
                if _ext in ('txt', 'pdn', 'ini'):
                    continue
                fp = os.path.join(path, file)
                zip_path = os.path.relpath(fp, self.tmp_path)
                self.files_list.append(zip_path)
                if _ext in ('jpg', 'png'):  # , "dds"):
                    t = self.loop.create_task(compress_file(fp, zip_path[:-3] + "pc" in self.files_list))
                    tasks.append(t)
            for dir_name in names:
                dir_path = os.path.join(path, dir_name)
                self.files_list.append(os.path.relpath(dir_path, self.tmp_path))

        await asyncio.gather(*tasks)

    async def start(self):
        global work_counter, redy_counter, prog_counter
        work_counter += 1
        c = work_counter
        try:
            s = round(os.path.getsize(self.mod_path) / (1024 * 1024), 2)
            print(f"[{c:<2}] Started: {self.name}")

            st = time.monotonic_ns()
            await self.unzip()
            z = round((time.monotonic_ns() - st) / 1000000000, 2)
            prog_counter += 1

            st = time.monotonic_ns()
            await self.compress()
            cs = round((time.monotonic_ns() - st) / 1000000000, 2)
            prog_counter += 1

            st = time.monotonic_ns()
            await self.zip()
            uz = round((time.monotonic_ns() - st) / 1000000000, 2)
            prog_counter += 1

            shutil.rmtree(self.tmp_path)
            sz = round(os.path.getsize(self.zip_path) / (1024 * 1024), 2)
            if sz > s:
                sz = s
                os.remove(self.zip_path)
                shutil.copy(self.mod_path, self.zip_path)
            te = round((time.monotonic_ns() - st0) / 1000000000, 2)
            redy_counter += 1
            print(f"[{c:<2}] [from_start={te:>8}s] [wait {mods_counter - redy_counter:<2}] | "
                  f"[unzip {z:>6}s] -> [compress {cs:>6}s] -> [zip {uz:>6}s] [{s:>6}mb -> {sz:>6}mb]: {self.name}")
        except Exception as e:
            redy_counter += 1
            print(f"[{c:<2}] Exception: {e}")
            traceback.print_exc()
        self.loop.stop()

    def run(self):
        loop = asyncio.new_event_loop()
        self.loop = loop
        asyncio.run_coroutine_threadsafe(self.start(), loop)
        loop.run_forever()


def main():
    global st0, mods_counter
    st = time.monotonic_ns()
    asyncio.set_event_loop(asyncio.new_event_loop())
    if os.path.exists(mods_new):
        shutil.rmtree(mods_new)
    os.mkdir(mods_new)
    if os.path.exists(tmp):
        shutil.rmtree(tmp)
    os.mkdir(tmp)
    mods = []
    size = 0
    for name in os.listdir(mods_old):
        if os.path.isfile(mods_old + name) and name.endswith(".zip"):
            size += os.path.getsize(mods_old + name)
            mods.append(Mod(name))
    num_cores = multiprocessing.cpu_count()
    mods_counter = len(mods)
    v, m, p = sys.version_info.major, sys.version_info.minor, sys.version_info.micro
    processor_name = "Unknown"
    system = platform.system()
    if system == "Windows":
        import winreg
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        processor_name = winreg.QueryValueEx(key, "ProcessorNameString")[0]
    elif system == "Linux":
        import subprocess
        result = subprocess.run(['lscpu'], stdout=subprocess.PIPE)
        output = result.stdout.decode('utf-8')
        processor_name = [x.split(':')[1].strip() for x in output.split('\n') if 'Model name' in x][0]
        os.system(f"ulimit -n {mods_counter * 500}")
    print(f"Python {v}.{m}.{p} ({system})")
    print(f"Processor: {processor_name.strip()} x{num_cores}")
    print(f"Starting process on {mods_counter} files, {size / (1024 ** 2):.2f}mb, cores {num_cores}...")
    st0 = time.monotonic_ns()
    with ThreadPoolExecutor(max_workers=num_cores) as ex:
        for mod in mods:
            ex.submit(mod.run)
    size2 = sum(os.path.getsize(os.path.join("zip", name)) for name in os.listdir("zip"))
    print(f"Work: {round((time.monotonic_ns() - st) / 1000000000, 4)}s, "
          f"{size / (1024 ** 2):.2f}mb -> {size2 / (1024 ** 2):.2f}mb")


if __name__ == '__main__':
    main()
