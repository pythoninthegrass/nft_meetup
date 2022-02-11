# nft_meetup

Takes the Medium article [Create Your Own NFT Collection With Python](https://betterprogramming.pub/create-your-own-nft-collection-with-python-82af40abf99f) and cleans up the code to generate NFT images.

## Setup
* Download the [substrapunk](https://github.com/usetech-llc/substrapunks/archive/refs/heads/master.zip) repo files and extract into the current directory.
* Install Poetry
    ```bash
    # Install
    curl -sSL https://install.python-poetry.org | $(which python3) -
    ```

## Usage
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
