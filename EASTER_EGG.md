# Easter Egg

## 1. Introduction
This template is designed to help you create a telegram bot for a simple quest

## 2. Installation
```bash
# Clone the repository
git clone https://github.com/Cub11k/ActiveSchoolBotTemplate.git
# or via SSH (preferred)
git clone git@github.com:Cub11k/ActiveSchoolBotTemplate.git

# Create a virtual environment, you may use python3.9 or higher
python3.9 -m venv venv

# Activate the virtual environment
source venv/bin/activate  # Linux
venv\Scripts\activate.bat  # Windows Cmd
venv\Scripts\activate.ps1  # Windows PowerShell

# Install the package
# pip>=21.3 is required
# Note that you should be in the root directory of the project
pip install -e .
```

## 3. Development
You will have to fill in the gaps, that are left, primarily in `config.toml` and in the `business_logic` module

## 4. Usage - local testing

### 4.1. Create a bot
1. Create a bot using [@BotFather](https://t.me/BotFather)
2. Copy the token
3. Copy the token to the `config.toml` file, be careful not to push it to GitHub

### 4.2. Adjust `config.toml`
1. Use `memory` storage as a state storage
2. Set `DEBUG` logging level for all loggers
3. Set `use_webhook` to `False`

### 4.3. Run the bot
```bash
launch-polling config.toml
```

## 5. Usage - production
There is a production-ready server waiting for your bot to be deployed.

Simply push your changes in the source code (excluding `config.toml`) to the `dev` branch of the remote repository 
and the bot will be deployed automatically.

## 6. Easter egg

If you want to add any other command to the interface of the bot, you are free to be creative.
Just don't forget to implement the basics first.