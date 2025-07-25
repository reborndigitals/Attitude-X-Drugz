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
STRING_SESSION = os.getenv("STRING_SESSION", "BQGVn2EAP_P3wNGw5EC62KWf66UWqO8_snHTIoT2qOBxqG7slnLMLAbEbPDlPIA_GDDkUxYAgI3DMABtwDiB8wLrJ10OmjgNuLCVeBvYcA13VYsryydjl5WL6XUbH17SQ7dZEDPsdNDdFazAnSNivsVIYoytJB61bkFAajDkmaTKOlYUKy0XA5si2Xhmew-kWen8pVSazgQKcNRxgtbIJdQD_B_zzUMMSn4aMS1Nj6B_9D5pYnh8jUo78yk-jc2svuYmYqkRFUv5TCSnW08hiXdY-OQ6X-9o1s6OOAzvvdy2M4m781O0uQxVPcwDYDiRL2P3vnIDttkEtxbPgBqEhHkAHY9DOQAAAAGkzbnBAA")
GROUP = os.getenv("GROUP", "HeartBeat_Fam")
CHANNEL = os.getenv("CHANNEL", "HeartBeat_Offi")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7956556231:AAEgPQOQsvTqpFV5I6BuFBCcPn-z_RGaKgc")
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
