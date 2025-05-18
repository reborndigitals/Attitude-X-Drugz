import random
import string
import os
from os import getenv
import time
import pymongo
from telethon import TelegramClient, events, Button
from pyrogram import Client, filters
from thumbnails import *
from fonts import *

# Use getenv for all sensitive/configurable values
API_ID = os.getenv("API_ID",)
API_HASH = os.getenv("API_HASH", "")
STRING_SESSION = os.getenv("STRING_SESSION", "")
GROUP = os.getenv("GROUP", "Hydrax_Music_update")
CHANNEL = os.getenv("CHANNEL", "Hydrax_Music_update")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
OWNER_ID = os.getenv("OWNER_ID", 6076474757)
LOGGER_ID = os.getenv("LOGGER_ID", None)
mongodb = os.getenv("MONGODB_URI", "")
# Working directory
ggg = os.getcwd()

# Initialize data structures
temporary = {}
active = []
playing = {}
queues = {}
clients = {}
played = {}
linkage = {}
conversations = {}
connector = {}
songs_client = {}
owners = {}
spam_chats = []
broadcasts = {}
broadcast_message = {}

# Track start time
StartTime = time.time()

# Set up MongoDB connection
mongo_client = pymongo.MongoClient(mongodb)
db = mongo_client['voice']
user_sessions = db['user_sessions']
collection = db["users"]
