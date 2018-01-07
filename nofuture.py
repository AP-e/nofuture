""" no-future """
import pathlib
import os
import shutil
import subprocess
import itertools

SOURCE_DIR='nodata' # root of archives
OUTPUT_DIR='music' # to decompress into
EXTS = ['zip', 'rar']

# archive extension: command line arguments
def p7zip_decompress(fpath, destination=''):
    """Decompress specified file using p7zip."""
    command_args = ['7z', 'x', fpath, '-y']
    if destination:
        command_args.append(f'-o{destination}')
    subprocess.run(command_args, check=True)

def decompress(source, output, exts):
    """Decompress specified archives using command-line utilities."""
    archives = sorted(itertools.chain.from_iterable(
        source.glob(f'*.{ext}') for ext in exts))
    
    failed, removed = [], []
    for fpath in archives:
        try:
            p7zip_decompress(fpath, output)
        except subprocess.CalledProcessError:
            failed.append(fpath)
        else:
            os.remove(fpath)
            removed.append(fpath)
    
    print(f'Decompressed and removed {len(removed)} archives')
    if failed:
        print('Could not decompress:\n\t' + 
              '\n\t'.join((fpath.name for fpath in failed)))

if __name__ == '__main__':
    decompress(pathlib.Path(SOURCE_DIR), pathlib.Path(OUTPUT_DIR), EXTS)
