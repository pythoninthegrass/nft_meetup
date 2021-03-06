# nft_meetup

Takes the Medium article [Create Your Own NFT Collection With Python](https://betterprogramming.pub/create-your-own-nft-collection-with-python-82af40abf99f) and cleans up the code to generate NFT images.

## Setup
* ~~Clone the [substrapunks](https://github.com/usetech-llc/substrapunks) repo files and extract into the current directory~~
    ```bash
    git clone https://github.com/UniqueNetwork/substrapunks.git
    ```
    * **NOTE**: this was integrated into the script with `gitpython`. No need to run manually
* Install 
    * [editorconfig](https://editorconfig.org/)
    * [asdf](https://asdf-vm.com/manage/core.html#installation-setup)
    * [poetry](https://python-poetry.org/docs/)

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
* `.vscode` settings
    * add arguments
    * env  
* debug path / dependencies

## Further Reading
[Introduction | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/)

[Commands | Documentation | Poetry - Python dependency management and packaging made easy](https://python-poetry.org/docs/cli#export)

[Set up a WSL development environment | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/setup/environment)

[Advanced settings configuration in WSL | Microsoft Docs](https://docs.microsoft.com/en-us/windows/wsl/wsl-config)

[Understanding The Python Path Environment Variable in Python](https://www.simplilearn.com/tutorials/python-tutorial/python-path)
