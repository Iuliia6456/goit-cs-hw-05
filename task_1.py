import argparse
from pathlib import Path
import shutil
import asyncio

# to run the task: py .\task_1.py -s .\picture\

async def read_folder(source: Path):
    files = []
    for el in source.iterdir():
        if el.is_dir():
            files.extend(await read_folder(el))
        else:
            files.append(el)
    return files

async def copy_file(source_file: Path, dest: Path):
    try:
        file_extension = source_file.suffix
        folder_name = file_extension if file_extension else "unknown"
        folder = dest / folder_name
        folder.mkdir(exist_ok=True, parents=True)
        await asyncio.to_thread(shutil.copy, source_file, folder)
    except shutil.SameFileError:
        print("Source and destination represent the same file")
    except PermissionError:
        print("Permission denied")
    except shutil.Error as e:
        print(f"Error occurred {e}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", type=Path, required=True, help="Source folder")
    parser.add_argument("-d", "--dest", type=Path, default=Path("dest"), help="Destination folder")
    args = parser.parse_args()

    source_folder = args.source
    target_folder = args.dest

    if not source_folder.exists():
        print("Source folder does not exist.")
        return

    try:
        source_files = await read_folder(source_folder)
        await asyncio.gather(*(copy_file(file, target_folder) for file in source_files))
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
