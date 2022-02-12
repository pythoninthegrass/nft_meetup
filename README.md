# nft_meetup

Takes the Medium article [Create Your Own NFT Collection With Python](https://betterprogramming.pub/create-your-own-nft-collection-with-python-82af40abf99f) and cleans up the code to generate NFT images.

## Setup
* Clone the [substrapunk](https://github.com/usetech-llc/substrapunks) repo files and extract into the current directory
    ```bash
    git clone https://github.com/UniqueNetwork/substrapunks.git
    ```
* [Install Poetry](https://python-poetry.org/docs/#installation)
    ```bash
    # Install Poetry
    curl -sSL https://install.python-poetry.org | $(which python3) -
    ```

## Usage
### asdf
```bash
# add python plugin
asdf plugin-add python

# install stable python
asdf install python latest

# refresh symlinks for installed python runtimes
asdf reshim python

# set stable to system python
asdf global python latest

# optional: local python (e.g., python 3.11)
cd $work_dir
asdf local python latest

# check installed python
asdf list python
```

### Poetry
```bash
# Change config
poetry config virtualenvs.in-project true           # .venv in `pwd`
poetry config experimental.new-installer false      # fixes JSONDecodeError on Python3.10

# Activate virtual environment (venv)
poetry shell

# Install all dependencies
poetry install

# Add multiple libraries
poetry add Pillow ipython

# Run script and exit environment
poetry run python main.py

# Deactivate venv
exit  # ctrl-d
```

## TODO
* ~~asdf~~
* wsl
  * enable
  * `.wslconfig` options
* debug path / dependencies
* submodule repo
* gh actions

## Further Reading
[Introduction | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/)

[Commands | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/cli#export)

[Set up a WSL development environment | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/setup/environment)

[Advanced settings configuration in WSL | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/wsl-config)

[Understanding The Python Path Environment Variable in Python](https://www.simplilearn.com/tutorials/python-tutorial/python-path)
