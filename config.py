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
API_ID = getenv("API_ID",)
API_HASH = getenv("API_HASH", "")
STRING_SESSION = getenv("SESSION_STR", "")
GROUP = getenv("GROUP", "nub_coder_s")
CHANNEL = getenv("CHANNEL", "nub_coders_updates")
BOT_TOKEN = getenv("BOT_TOKEN", "")
OWNER_ID = getenv("OWNER_ID", 6076474757)
mongodb = getenv("MONGODB_URI", "")
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
