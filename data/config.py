"""
We extract some values from environment variables in this file.
"""

import os

from dotenv import load_dotenv, find_dotenv

# Finding .env file and loading it as environment variables
load_dotenv(find_dotenv())

# Getting bot token and special string to connect to the Mongo Client
BOT_TOKEN = os.getenv('TOKEN')
MONGO_CLIENT = os.getenv('MONGO_CLIENT')
