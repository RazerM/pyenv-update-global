#!/usr/bin/env python3
"""pyenv_update_global

Usage:
    pyenv_update_global [--dry-run]
"""
import re
from collections import defaultdict

from docopt import docopt
from packaging.version import parse as parse_version
from plumbum import FG
from plumbum.cmd import pyenv

args = docopt(__doc__)
DRY_RUN = args['--dry-run']


# Tuples of (python, version). Use None for CPython. Latest matching version
# will be installed (e.g. 3.5.3 for "3.5")
PYTHON_VERSIONS = [
    (None, '2.7'),
    (None, '2.6'),
    (None, '3.6'),
    (None, '3.5'),
    (None, '3.4'),
    (None, '3.3'),
    ('pypy', None),
    ('pypy3', None),
]

re_version = re.compile(
    r'^\s*(?:(?P<name>[\w-]+)-)?(?P<version>[\d\.]+)\n',
    flags=re.MULTILINE)

version_output = pyenv('install', '--list')

available_versions = defaultdict(list)

for match in re_version.finditer(version_output):
    d = match.groupdict()
    name = d['name'] or None
    version = parse_version(d['version'])

    available_versions[name].append(version)

version_list = []

for name, desired_version in PYTHON_VERSIONS:
    # if desired_version given, find latest version that matches it.
    if desired_version is not None:
        matching_versions = sorted(v for v in available_versions[name]
                                   if str(v).startswith(desired_version))
    else:
        matching_versions = sorted(available_versions[name])

    latest_version = matching_versions[-1]

    pyenv_string = name + '-' if name else ''
    pyenv_string += str(latest_version)
    version_list.append(pyenv_string)

# Install any that are missing.
for pyenv_string in version_list:
    cmd = pyenv['install', '--skip-existing', pyenv_string]
    print(cmd)
    if not DRY_RUN:
        cmd & FG

# Set global to the latest versions (with system fallback)
cmd = pyenv[['global', *version_list, 'system']]
print(cmd)
if not DRY_RUN:
    cmd & FG
