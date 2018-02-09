import pytest
from pathlib import Path
import os
import patoolib
from nofuture import decompress
from nofuture.config import ARCHIVES_DIR, STAGING_DIR, ARCHIVE_FORMATS

RELEASE = {'id': 6666365,
           'title': "X / Don't Get Me Started",
           'artists': ("Hodge", "Acre"),
           'tracks': ("X", "Don't Get Me Started"),
           'label': "Wisdom Teeth",
           'catno': "WSDM002",
           'dirname': "Hodge & Acre - X _ Don't Get Me Started [2015] [EP]",
           'files': ("01 Hodge - X.mp3", "02 Acre - Don't Get Me Started.mp3"),
           'archivename': "HAXDGMS"}

@pytest.fixture
def archives_dir(tmpdir):
    return tmpdir.mkdir(ARCHIVES_DIR)

@pytest.fixture
def staging_dir(tmpdir):
    return tmpdir.mkdir(STAGING_DIR)

@pytest.fixture
def decompressed_dir(tmpdir):
    """Return path of artificial release directory (i.e. contents of downloaded archive)."""
    dir_ = tmpdir.mkdir(RELEASE['dirname'])
    for fname in RELEASE['files']:
        p = dir_.join(fname).write('')
    return dir_

@pytest.fixture()
def archive(archives_dir, decompressed_dir, request):
    """Return path of archive created from release directory."""
    archive = archives_dir.join(RELEASE['archivename']).new(ext=request.param)
    patoolib.create_archive(str(archive), [str(decompressed_dir)])
    return archive
