"""Real Python fixture commands, using the Python packaging console launcher on Windows.

No shell interprets fixture arguments. Windows test environments require pip,
whose vendored distlib launcher is already used for installed Python CLIs.
"""
import io
import os
from pathlib import Path
import sys
import zipfile


def executable_path(path):
    path = Path(path)
    return path.with_name(path.name + '.exe') if os.name == 'nt' and path.suffix != '.exe' else path


def write_executable(path, source):
    path = executable_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if os.name == 'nt':
        from pip._vendor.distlib.scripts import ScriptMaker
        launcher = ScriptMaker(None, str(path.parent))._get_launcher('t')
        archive = io.BytesIO()
        with zipfile.ZipFile(archive, 'w') as stream:
            stream.writestr('__main__.py', source)
        path.write_bytes(launcher + ('#!"' + sys.executable + '"\n').encode('utf-8') + archive.getvalue())
    else:
        path.write_text('#!' + sys.executable + '\n' + source, encoding='utf-8')
        path.chmod(0o755)
    return path
