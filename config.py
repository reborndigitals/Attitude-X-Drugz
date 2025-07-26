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
API_ID = os.getenv("API_ID","10284859")
API_HASH = os.getenv("API_HASH", "b0ad58eb8b845ba0003e0d9ce5fc2196")
STRING_SESSION = os.getenv("STRING_SESSION", "BQGVn2EAOZapXLQ0NmnX88wthxdt_rEiV4Hn4Jg8M1b4tMpIRfDLqZNi0OTgqMULoPa5AaJ9cbmLsC_nqJMxeL6d7F_MKD_jyh1JVL3uCQ0yFbTiM7hLYaXRF57p7jmn7sSYF2fwY8NeXDpZHTDLanDt0k0L_din7fAIHyhCHRT_t7CJ8W3zUkrxSOpBicwvQCYla3phRvwjstba6uI3bKcYJUiBcEoGlQBguj6N1eRvTm-KwsOQuy1cCJDwAcv6TJRMqgqMT1Z8BQ5UvKr4YD0Iaxy65cuQVCplD6A9rPkT0XATA4NXf7hzHtyR5PAfaIw2PL5YRKtJPOimLq3UwhJOwxXTzwAAAAGkzbnBAA")
GROUP = os.getenv("GROUP", "HeartBeat_Fam")
CHANNEL = os.getenv("CHANNEL", "HeartBeat_Offi")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7992290736:AAGNT441X0menIQ1ZBxc9RjHQHYfEL0Qz2E")
OWNER_ID = int(os.getenv("OWNER_ID", 1281282633))
LOGGER_ID = os.getenv("LOGGER_ID", "-1001735663878")
mongodb = os.getenv("MONGODB_URI", "mongodb+srv://heartbeat:Beat7Heart@heartbeat.1h1nbxv.mongodb.net/?retryWrites=true&w=majority")
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
