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
STRING_SESSION = os.getenv("STRING_SESSION", "BQDMBnkAhl63LfVwI1-Pu38Cj_U5J1fg94CoUuYa8VcOfu6JcKTsMf6IjdKxGuJUmTyLcycSMFw4H_amfXQ-6B8q0DoT1uA7xM4nAxR8XBQvDkepomQoB9qF6fiTRTBMJjIXFfVgNUY_5JI9PK08mJ26whDradE6lMEPlvVcR4Jto3KdaLpvTPE45nmx5VeAUl_LAgy4o3VgOa9S0yKy8Ha8d0ueGa_A8goiXm52ADheVq2EOcCuu09e-kJixlMujIuDrqLFd4S_RLlfTSvvmYAF0eOu1b6jz1vOwFahGBQCOT_eucH26KQe-VUlWlT-ECD3LyRJIwezaSrYZADjw_aXMUqQaQAAAAHjb-HaAA")
GROUP = os.getenv("GROUP", "HeartBeat_Fam")
CHANNEL = os.getenv("CHANNEL", "HeartBeat_Offi")
BOT_TOKEN = os.getenv("BOT_TOKEN", "7921879783:AAFdFgIr1ti-FOvGa00W1t6hyskwyjp6IC0")
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
