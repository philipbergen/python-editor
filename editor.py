from __future__ import print_function

import os.path
import subprocess
import tempfile
from distutils.spawn import find_executable


class EditorError(RuntimeError):
    pass


def get_default_editors():
    # TODO: Make platform-specific
    return [
        'vim',
        'emacs',
        'nano',
    ]


def get_editor_args(editor):
    if editor in ['vim', 'gvim']:
        return '-f -o'

    elif editor == 'emacs':
        return '-nw'

    else:
        return ''


def get_platform_editor_var():
    # TODO: Make platform specific
    return "$EDITOR"


def get_editor():
    env_editor = os.path.expandvars('$EDITOR')
    if env_editor != '$EDITOR' and env_editor.strip():
        return env_editor

    for ed in get_default_editors():
        path = find_executable(ed)
        if path is not None:
            return path

    raise EditorError("Unable to find a viable editor on this system."
        "Please consider setting your %s variable" % get_platform_editor_var())


def edit(filename=None, contents=None):
    editor = get_editor()
    args = get_editor_args(os.path.basename(editor))
    args = [editor] + args.split(' ')

    if filename is None:
        tmp = tempfile.NamedTemporaryFile()
        filename = tmp.name

    if contents is not None:
        with open(filename, mode='wb') as f:
            f.write(contents)

    args += [filename]

    proc = subprocess.Popen(args)
    proc.communicate()

    with open(filename, mode='rb') as f:
        return f.read()


def _get_editor(ns):
    print(get_editor())

def _edit(ns):
    print(edit())

if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers()

    cmd = sp.add_parser('get-editor')
    cmd.set_defaults(cmd=_get_editor)

    cmd = sp.add_parser('edit')
    cmd.set_defaults(cmd=_edit)

    ns = ap.parse_args()
    ns.cmd(ns)