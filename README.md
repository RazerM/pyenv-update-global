# pyenv_update_global

This script installs the latest Pythons matching a list of criteria, then activates them using `pyenv global`.

## Instructions

1. Edit `pyenv_update_global.py` to specify the Python versions you want:

    ```python
    PYTHON_VERSIONS = [
        # Install latest CPython 3.5.x
        (None, '3.5'),
        # Install latest PyPy
        ('pypy', None),
        # Install Latest Miniconda3 4.0.x
        ('miniconda3', '4.0'),
    ]
    ```

2. Run `pyenv_update_global.py` (requires Python 3.5 or later), optionally using `--dry-run`.

    ```bash
    $ python3 pyenv_update_global.py --dry-run
    ```

    ```none
    /usr/local/Cellar/pyenv/1.0.6/libexec/pyenv install --skip-existing 3.5.2
    /usr/local/Cellar/pyenv/1.0.6/libexec/pyenv install --skip-existing pypy-5.6.0
    /usr/local/Cellar/pyenv/1.0.6/libexec/pyenv install --skip-existing miniconda3-4.0.5
    /usr/local/Cellar/pyenv/1.0.6/libexec/pyenv global 3.5.2 pypy-5.6.0 miniconda3-4.0.5 system
    ```

## Caveats

It only matches version numbers like `x.y.z` since that's all I need.