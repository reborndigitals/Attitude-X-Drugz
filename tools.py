import json
import subprocess
import requests
import re
from io import BytesIO
from urllib.parse import parse_qs, urlparse

import asyncio
import math
import os
import shlex
from pyrogram.errors.exceptions import InviteHashExpired , ChannelPrivate ,GroupcallForbidden
from typing import Tuple
from pytgcalls import idle, PyTgCalls
from pytgcalls.types import AudioQuality
from pytgcalls.types import MediaStream
from pytgcalls.types import VideoQuality
from PIL import Image
from pymediainfo import MediaInfo
from pyrogram.types import Message
import time
from pytgcalls.exceptions import NotInCallError
from pytgcalls.types import ChatUpdate, StreamEnded



from pytgcalls.exceptions import (
    NoActiveGroupCall,
)
import os
from asyncio import sleep
import os
import sys
from re import sub
from fonts import *
from pyrogram import Client, filters, enums
from pyrogram.types import Message
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import time
import asyncio
from config import *
from pyrogram import Client, filters
import gc
import time

from pyrogram.errors import (
    FloodWait,
    RPCError,
)


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
SUDO = []
AUTH = {}
BLOCK = []
# Replace with your actual API ID and API hash from my.telegram.org                     
async def handle_disconnect(client, retries=5, delay=5):
    """Handles disconnects by attempting to reconnect with retries."""
    for attempt in range(retries):
        try:
            print(f"Attempting to reconnect (attempt {attempt + 1}/{retries})...")
            await client.connect()
            if client.is_connected:
                print("Successfully reconnected.")
                break  # Exit the loop if reconnected successfully
        except FloodWait as e:
            print(f"Floodwait encountered, waiting {e.value} seconds")
            await asyncio.sleep(e.value)
        except RPCError as e:
             print(f"RPC Error, not retrying: {e}")
             break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    else:
        print(f"Failed to reconnect after {retries} attempts.")


import os
import shutil

def clear_directory(directory_path):
    # Check if the directory exists
    if not os.path.exists(directory_path):
        print(f"The directory {directory_path} does not exist.")
        return
    
    # Check if the path is actually a directory
    if not os.path.isdir(directory_path):
        print(f"{directory_path} is not a directory.")
        return
    
    # List all files and directories in the given directory
    for item in os.listdir(directory_path):
        item_path = os.path.join(directory_path, item)
        
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                # Remove file or symbolic link
                os.unlink(item_path)
            elif os.path.isdir(item_path):
                # Remove directory and all its contents
                shutil.rmtree(item_path)
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")
    
    print(f"Directory {directory_path} has been cleared.")

import asyncio
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram import enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from yt_dlp import YoutubeDL
import re

def extract_video_id(url):
    """
    Extract YouTube video ID from various forms of YouTube URLs.
    
    Args:
        url (str): YouTube video URL
        
    Returns:
        str: Video ID or None if not found
    """
    try:
        # Patterns for different types of YouTube URLs
        patterns = [
            r'(?:v=|/v/|youtu\.be/|/embed/)([^&?/]+)',  # Standard, shortened and embed URLs
            r'(?:watch\?|/v/|youtu\.be/)([^&?/]+)',     # Watch URLs
            r'(?:youtube\.com/|youtu\.be/)([^&?/]+)'    # Channel URLs
        ]
        
        # Try each pattern
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        return None
        
    except Exception as e:
        return f"Error extracting video ID: {str(e)}"


def format_number(num):
    """Format number to international system (K, M, B)"""
    if num is None:
        return "N/A"
    
    if num < 1000:
        return str(num)
    
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    
    # Add precision based on magnitude
    if magnitude > 0:
        num = round(num, 1)
        if num.is_integer():
            num = int(num)
    
    return f"{num:g}{'KMB'[magnitude-1]}"

import yt_dlp
import datetime

def parse_and_format_date(date_str):
    """
    Parse and format date string
    
    Args:
        date_str (str): Date string to parse
    
    Returns:
        str: Formatted date or 'N/A'
    """
    if not date_str:
        return 'N/A'
    
    try:
        # Try different date formats
        date_formats = [
            '%Y%m%d',  # YouTube format
            '%Y-%m-%d',  # ISO format
            '%d/%m/%Y',  # DD/MM/YYYY
            '%m/%d/%Y',  # MM/DD/YYYY
        ]
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.datetime.strptime(date_str, date_format)
                return parsed_date.strftime('%B %d, %Y')
            except ValueError:
                continue
        
        return 'N/A'
    except Exception:
        return 'N/A'

def get_video_details(video_id):
    """
    Get video details using yt_dlp
    
    Args:
        video_id (str): Video ID to fetch details for
    
    Returns:
        dict: Video details or error message
    """
    # Try YouTube first
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat':True,
        }

        # Try YouTube URL first
        youtube_url = f"https://www.youtube.com/watch?v={video_id}"
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract initial info
            info = ydl.extract_info(youtube_url, download=False)

            # Process upload date
            upload_date = parse_and_format_date(info.get('upload_date'))

            # Process duration
            duration = 'N/A'
            if info.get('duration'):
                try:
                    duration = str(
                        datetime.datetime.fromtimestamp(
                            info.get('duration')
                        ).strftime('%H:%M:%S')
                    )
                except (ValueError, TypeError):
                    duration = 'N/A'

            # Prepare details dictionary
            details = {
                'title': info.get('title', 'N/A'),
                'thumbnail': info.get('thumbnail', 'N/A'),
                'duration': duration,
                'view_count': info.get('view_count', 'N/A'),
                'like_count': info.get('like_count', 'N/A'),
                'channel_name': info.get('uploader', 'N/A'),
                'subscriber_count': info.get('channel_follower_count', 'N/A'),
                'upload_date': upload_date,
                'video_url': youtube_url,
                'platform': 'YouTube'
            }

            return details

    except (yt_dlp.utils.ExtractorError, yt_dlp.utils.DownloadError) as youtube_error:
        # If YouTube extraction fails, try Instagram
        try:
            # Construct Instagram Reel URL
            instagram_url = f"https://www.instagram.com/reel/{video_id}/"
            
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'extract_flat': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # Extract Instagram Reel info
                info = ydl.extract_info(instagram_url, download=False)

                # Process upload date
                upload_date = parse_and_format_date(info.get('upload_date'))

                # Process duration
                duration = 'N/A'
                if info.get('duration'):
                    try:
                        duration = str(
                            datetime.datetime.fromtimestamp(
                                info.get('duration')
                            ).strftime('%H:%M:%S')
                        )
                    except (ValueError, TypeError):
                        duration = 'N/A'

                # Prepare Instagram details
                details = {
                    'title': info.get('title', 'N/A'),
                    'thumbnail': info.get('thumbnail', 'N/A'),
                    'duration': duration,
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'channel_name': info.get('uploader', 'N/A'),
                    'subscriber_count': 0,
                    'upload_date': upload_date,
                    'video_url': instagram_url,
                    'platform': 'Instagram'
                }

                return details

        except Exception as instagram_error:
            # If both fail, return error details
            return {
                'error': f"Extraction failed for both YouTube and Instagram. Original error: {youtube_error}"
            }

import datetime
import os
import magic

def is_streamable(file_path):
    """
    Check if a file is potentially streamable.
    
    Args:
        file_path (str): Path to the file to be checked
    
    Returns:
        bool: True if file is potentially streamable, False otherwise
    """
    # Check if file exists
    if not os.path.exists(file_path):
        return False

    # Supported streamable file extensions
    STREAMABLE_EXTENSIONS = {
        'video': {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', 
                  '.webm', '.m4v', '.mpg', '.mpeg', '.3gp'},
        'audio': {'.mp3', '.wav', '.flac', '.aac', '.ogg', 
                  '.wma', '.m4a', '.opus'}
    }

    try:
        # Get file extension
        file_extension = os.path.splitext(file_path)[1].lower()

        # Use python-magic for MIME type detection
        mime = magic.Magic(mime=True)
        detected_mime_type = mime.from_file(file_path)
        
        # Check streamability based on MIME type and extension
        is_video_mime = detected_mime_type.startswith('video/')
        is_audio_mime = detected_mime_type.startswith('audio/')
        
        is_video_ext = file_extension in STREAMABLE_EXTENSIONS['video']
        is_audio_ext = file_extension in STREAMABLE_EXTENSIONS['audio']

        # Return True if any streaming condition is met
        return is_video_mime or is_audio_mime or is_video_ext or is_audio_ext

    except Exception:
        return False

# Example usage
import psutil
import os
async def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        up_time += time_list.pop() + ", "

    time_list.reverse()
    up_time += ":".join(time_list)
    return up_time
def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
      return ""
    return " ".join(split[1:])



async def is_active_chat(chat_id):
    if chat_id not in active:
        return False
    else:
        return True

async def add_active_chat(chat_id):
    if chat_id not in active:
         active.append(chat_id)


async def remove_active_chat(chat_id):
    if chat_id in active:
        active.remove(chat_id)
    chat_dir = f"{ggg}/user_{clients['bot'].me.id}/{chat_id}"
    os.makedirs(chat_dir, exist_ok=True)
    clear_directory(chat_dir)

'''
async def autoleave_vc(message, duration_str,chat):
    """
    Automatically leave voice chat when only the bot remains in the call for 5 seconds
    """
    
    while True:
        try:
            # Track if song duration changes
            if chat.id in playing and playing[chat.id]:
                current_song = playing[chat.id]
                if str(current_song['duration']) != str(duration_str):
                    break
        except Exception:
            pass

        try:
            # Get current call members
            members = []
            async for member in clients["session"].get_call_members(chat.id):
                members.append(member)

            # Check if only bot remains in call
            if len(members) == 1 and members[0].chat.id == clients["session"].me.id:
                # Confirm persistent presence check
                await asyncio.sleep(25)
                
                # Recheck after cooldown
                members = []
                async for member in clients["session"].get_call_members(chat.id):
                    members.append(member)

                # Final verification before leaving
                if len(members) == 1 and members[0].chat.id == clients["session"].me.id:
                    await clients["call_py"].leave_call(chat.id)
                    # Cleanup operations
                    try:
                        queues[chat.id].clear()
                        playing[chat.id].clear()
                    except KeyError:
                        pass
                    
                    await remove_active_chat(chat.id)
                    await clients["bot"].send_message(
                        message.chat.id,
                        "⚠️ Nᴏ ᴀᴄᴛɪᴠᴇ ʟɪsᴛᴇɴᴇʀs ᴅᴇᴛᴇᴄᴛᴇᴅ. Lᴇᴀᴠɪɴɢ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ."
                    )
                    await remove_active_chat(chat.id)
                    break

        except Exception as e:
            print(f"Autoleave error: {e}")
            break

        # Reduced check interval
        await asyncio.sleep(8)

async def pautoleave_vc(message, duration_str):
    """
    Automatically leave voice chat when members count is <= 1 for 5 seconds
    
    :param user_client: User client to get call members and send messages
    :param call_py: PyTgCalls client for leaving call
    :param message: Message object containing chat information
    :param playing: Dictionary tracking currently playing songs
    :param duration_str: Current song duration
    """
    while True:
        try:
            # Check if current song duration changed
            if message.chat.id in playing and playing[message.chat.id]:
                current_song = playing[message.chat.id]
                if str(current_song['duration']) != str(duration_str):
                    break
        except Exception:
            pass

        # Get current call members
        members = []
        try:
          async for i in clients["session"].get_call_members(message.chat.id):
            members.append(i)
        except:
           break
        # Check if members count is <= 1
        if len(members) <= 1:
            # Wait 5 seconds to confirm
            await asyncio.sleep(5)
            
            # Recheck members count after 5 seconds
            members = []
            async for i in clients["session"].get_call_members(message.chat.id):
                members.append(i)
            
            # If still <= 1 member, leave the voice chat
            if len(members) <= 1:
                await clients["call_py"].leave_call(message.chat.id)
                # Send message about leaving
                try:
                    queues[message.chat.id].clear()
                except:
                   pass
                try:
                    playing[message.chat.id].clear()
                except:
                   pass
                await remove_active_chat(message.chat.id)
                await clients["bot"].send_message(
                    message.chat.id, 
                    f"ɴᴏ ᴏɴᴇ ɪꜱ ʟɪꜱᴛᴇɴɪɴɢ ᴛᴏ ᴛʜᴇ ꜱᴛʀᴇᴀᴍ, ꜱᴏ ᴛʜᴇ ᴀꜱꜱɪꜱᴛᴀɴᴛ ʟᴇꜰᴛ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ."
                )
                break
        
        # Wait before next check
        await asyncio.sleep(10)
'''

async def update_progress_button(message, duration_str,chat):
    try:
        total_seconds = sum(int(x) * 60 ** i for i, x in enumerate(reversed(duration_str.split(":"))))

        while True:
            try:
                updated_msg = await clients["call_py"]._mtproto.get_messages(message.chat.id,message.id)
            except:
                break
            try:
                # Fetch elapsed seconds
                elapsed_seconds = int(await clients["call_py"].time(chat.id))
            except Exception as e:
                # If an exception occurs, the song has ended
                break
            try:
               if chat.id in playing and playing[chat.id]:
                   current_song = playing[chat.id]
                   if str(current_song['duration']) != str(duration_str):
                       break            # Format elapsed time
            except Exception as e:
                pass
            elapsed_str = time.strftime('%M:%S', time.gmtime(int(time.time() - played[chat.id])))
            elapsed_seconds = int(time.time() - played[chat.id])
            # Calculate progress bar (6 `─` with spaces)
            progress_length = 8
            position = min(int((elapsed_seconds / total_seconds) * progress_length), progress_length)
            progress_bar = "⭑" * position + "✪" + "⭑" * (progress_length - position - 1)
            progress_bar = progress_bar.strip()  # Remove trailing spaces

            progress_text = f"{elapsed_str} {progress_bar} {duration_str}"

            # Insert progress bar between the first and last rows
            keyboard = message.reply_markup.inline_keyboard
            progress_row = [InlineKeyboardButton(text=progress_text, callback_data="ignore")]
            updated_keyboard = keyboard[:1] + [progress_row] + keyboard[1:]

            await message.edit_reply_markup(InlineKeyboardMarkup(updated_keyboard))
            await asyncio.sleep(9)
    except Exception as e:
        print(f"Progress update error: {e}")


def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "ᴍ", "ʜ", "ᴅᴀʏs"]
    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for i in range(len(time_list)):
        time_list[i] = str(time_list[i]) + time_suffix_list[i]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

queue_styles = {
    1: """🌈 𝗤𝗨𝗘𝗨𝗘 𝗔𝗗𝗗𝗘𝗗 »✨
┏━━━━━━━━━━━━
┣ 𝗠𝗼𝗱𝗲 » {}
┣ 𝗧𝗶𝘁𝗹𝗲 » {}
┣ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 » {}
┗ 𝗣𝗼𝘀𝗶𝘁𝗶𝗼𝗻 » #{}""",

    2: """✧･ﾟ 𝓐𝓭𝓭𝓮𝓭 𝓣𝓸 𝓠𝓾𝓮𝓾𝓮 ･ﾟ✧
━━━━━━━━━━━━
♪ 𝓜𝓸𝓭𝓮 » {}
♪ 𝓣𝓲𝓽𝓵𝓮 » {}
♪ 𝓛𝓮𝓷𝓰𝓽𝓱 » {}
♪ 𝓟𝓸𝓼𝓲𝓽𝓲𝓸𝓷 » #{}""",

    3: """⋆｡°✩ 𝐒𝐨𝐧𝐠 𝐐𝐮𝐞𝐮𝐞𝐝 ✩°｡⋆
┏━━━━━━━━━━━
┣ 𝐌𝐨𝐝𝐞 » {}
┣ 𝐓𝐫𝐚𝐜𝐤 » {}
┣ 𝐓𝐢𝐦𝐞 » {}
┗ 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧 » #{}""",

    4: """⚡ 𝕋𝕣𝕒𝕔𝕜 𝔸𝕕𝕕𝕖𝕕 𝕥𝕠 ℚ𝕦𝕖𝕦𝕖 ⚡
╔═══════════
║ 𝕄𝕠𝕕𝕖: {}
║ 𝕋𝕚𝕥𝕝𝕖: {}
║ 𝔻𝕦𝕣𝕒𝕥𝕚𝕠𝕟: {}
╚ ℙ𝕠𝕤𝕚𝕥𝕚𝕠𝕟: #{}""",

    5: """<blockquote>⋆｡°✩ **𝐃яʋɢ-𝐃ɛαƖ ✩°｡⋆</blockquote>
<blockquote>┏━━━━━━━━━━━━━━━
┣✰ **𝐏σιƨσи** ➥ {}
┣✰ **𝐑ɛᴧтƨ** ➥ {}
┗✰ **𝐑ᴧтιиɢ** ➥ #{}</blockquote>\n<blockquote>☆ . * ● ¸ . ✦ .★° :. ★ * • ○ ° ★</blockquote>""",
    

    6: """🌊 𝙌𝙪𝙚𝙪𝙚 𝙐𝙥𝙙𝙖𝙩𝙚𝙙 🌊
┏━━━━━━━━━━━
┣ 𝙈𝙤𝙙𝙚 » {}
┣ 𝙏𝙞𝙩𝙡𝙚 » {}
┣ 𝙇𝙚𝙣𝙜𝙩𝙝 » {}
┗ 𝙌𝙪𝙚𝙪𝙚 » #{}""",

    7: """👑 𝖀𝖕𝖈𝖔𝖒𝖎𝖓𝖌 𝕿𝖗𝖆𝖈𝖐 👑
▰▰▰▰▰▰▰▰▰▰▰▰▰
◈ 𝕸𝖔𝖉𝖊: {}
◈ 𝕿𝖎𝖙𝖑𝖊: {}
◈ 𝕯𝖚𝖗𝖆𝖙𝖎𝖔𝖓: {}
◈ 𝕻𝖔𝖘𝖎𝖙𝖎𝖔𝖓: #{}""",

    8: """✦ 𝐄𝐧𝐪𝐮𝐞𝐮𝐞𝐝 𝐌𝐮𝐬𝐢𝐜 ✦
═════════════
★ Mode: {}
★ Title: {}
★ Duration: {}
★ Position: #{}""",

    9: """🎧 ADDED ＴＯ ＱＵＥＵＥ 🎧
┌───────────┐
│ ＭＯＤ: {}
│ ＴＲＫ: {}
│ ＴＩＭ: {}
└ ＰＯＳ: #{}""",

    10: """⚡ 【﻿ＱＵＥＵＥ　ＵＰＤＡＴＥ】 ⚡
▀▀▀▀▀▀▀▀▀▀▀▀▀
➺ Ｍｏｄｅ : {}
➺ Ｔｒａｃｋ : {}
➺ Ｌｅｎｇｔｈ : {}
➺ Ｏｒｄｅｒ : #{}""",

    11: """🔮 **Tʀᴀᴄᴋ Aᴅᴅᴇᴅ ᴛᴏ Qᴜᴇᴜᴇ** 🔮
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• **Mᴏᴅᴇ** » {}
• **Tɪᴛʟᴇ** » {}
• **Dᴜʀᴀᴛɪᴏɴ** » {}
• **Pᴏsɪᴛɪᴏɴ** » #{}""",

    12: """✧･ﾟ: *✧･ﾟ 𝗔𝗱𝗱𝗲𝗱 𝘁𝗼 𝗤𝘂𝗲𝘂𝗲 ･ﾟ*:･ﾟ✧
━━━━━━━━━━━━━
〃 𝗠𝗼𝗱𝗲 » {}
〃 𝗧𝗶𝘁𝗹𝗲 » {}
〃 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 » {}
〃 𝗢𝗿𝗱𝗲𝗿 » #{}""",
}


play_styles = {
    1: """🌈 𝗡𝗢𝗪 𝗣𝗟𝗔𝗬𝗜𝗡𝗚 »✨
┏━━━━━━━━━━━━
┣ 𝗠𝗼𝗱𝗲 » {}
┣ 𝗧𝗶𝘁𝗹𝗲 » {}
┣ 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 » {}
┗ 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗯𝘆 » {}""",

    2: """✧･ﾟ 𝓝𝓸𝔀 𝓟𝓵𝓪𝔂𝓲𝓷𝓰 ･ﾟ✧
━━━━━━━━━━━━━
♪ 𝓜𝓸𝓭𝓮 » {}
♪ 𝓣𝓲𝓽𝓵𝓮 » {}
♪ 𝓛𝓮𝓷𝓰𝓽𝓱 » {}
♪ 𝓡𝓮𝓺𝓾𝓮𝓼𝓽𝓮𝓭 𝓫𝔂 » {}""",

    3: """⋆｡°✩ 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 ✩°｡⋆
┏━━━━━━━━━━━━
┣ 𝐌𝐨𝐝𝐞 » {}
┣ 𝐓𝐫𝐚𝐜𝐤 » {}
┣ 𝐓𝐢𝐦𝐞 » {}
┗ 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐛𝐲 » {}""",

    4: """⚡ ℕ𝕠𝕨 ℙ𝕝𝕒𝕪𝕚𝕟𝕘 ⚡
╔════════════
║ 𝕄𝕠𝕕𝕖: {}
║ 𝕋𝕚𝕥𝕝𝕖: {}
║ 𝔻𝕦𝕣𝕒𝕥𝕚𝕠𝕟: {}
╚ ℝ𝕖𝕢𝕦𝕖𝕤𝕥𝕖𝕕 𝕓𝕪: {}""",

    5: """<blockquote>⋆｡°✩ **𝐒ρɛᴄιᴧƖ-𝐃яʋɢ**  ✩°｡⋆</blockquote>
<blockquote>┏━━━━━━━━━━━━━━━
┣✰ **𝐏σιƨσи** ➥ {}
┣✰ **𝐑єᴧᴄтƨ** ➥ {}
┗━━━✰**𝐅ᴄʋκɛ∂-𝐁ʏ**✰━━━━
 \n{}</blockquote>\n<blockquote>☆ . * ● ¸ . ✦ .★° :. ★ * • ○ ° ★</blockquote>""",
    

    6: """🌊 𝙉𝙤𝙬 𝙋𝙡𝙖𝙮𝙞𝙣𝙜 🌊
┏━━━━━━━━━━━━
┣ 𝙈𝙤𝙙𝙚 » {}
┣ 𝙏𝙞𝙩𝙡𝙚 » {}
┣ 𝙇𝙚𝙣𝙜𝙩𝙝 » {}
┗ 𝘿𝙅 » {}""",

    7: """👑 𝕽𝖔𝖞𝖆𝖑 𝕻𝖑𝖆𝖞𝖇𝖆𝖈𝖐 👑
▰▰▰▰▰▰▰▰▰▰▰▰▰
◈ 𝕸𝖔𝖉𝖊: {}
◈ 𝕿𝖎𝖙𝖑𝖊: {}
◈ 𝕯𝖚𝖗𝖆𝖙𝖎𝖔𝖓: {}
◈ 𝕽𝖊𝖖𝖚𝖊𝖘𝖙𝖊𝖉 𝖇𝖞: {}""",

    8: """✦ 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐌𝐮𝐬𝐢𝐜 ✦
═════════════
★ Mode: {}
★ Title: {}
★ Duration: {}
★ Requester: {}""",

    9: """🎧 ＮＯＷ ＰＬＡＹＩＮＧ 🎧
┌───────────┐
│ ＭＯＤ: {}
│ ＴＲＫ: {}
│ ＴＩＭ: {}
└ ＵＳＲ: {}""",

    10: """⚡ 【﻿ＮＯＷ　ＰＬＡＹＩＮＧ】 ⚡
▀▀▀▀▀▀▀▀▀▀▀▀
➺ Ｍｏｄｅ : {}
➺ Ｔｒａｃｋ : {}
➺ Ｌｅｎｇｔｈ : {}
➺ Ｒｅｑｕｅｓｔｅｄ ｂｙ : {}""",

    11: """🔮 **Nᴏᴡ Pʟᴀʏɪɴɢ** 🔮
⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯
• **Mᴏᴅᴇ** » {}
• **Tɪᴛʟᴇ** » {}
• **Dᴜʀᴀᴛɪᴏɴ** » {}
• **Rᴇǫᴜᴇsᴛᴇᴅ ʙʏ** » {}""",

    12: """✧･ﾟ: *✧･ﾟ 𝗡𝗼𝘄 𝗣𝗹𝗮𝘆𝗶𝗻𝗴 ･ﾟ*:･ﾟ✧
━━━━━━━━━━━━━━━━
〃 𝗠𝗼𝗱𝗲 » {}
〃 𝗧𝗶𝘁𝗹𝗲 » {}
〃 𝗗𝘂𝗿𝗮𝘁𝗶𝗼𝗻 » {}
〃 𝗥𝗲𝗾𝘂𝗲𝘀𝘁𝗲𝗱 𝗯𝘆 » {}""",
}

def convert_bytes(size: float) -> str:
    """humanize size"""
    if not size:
        return ""
    power = 1024
    t_n = 0
    power_dict = {0: " ", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        t_n += 1
    return "{:.2f} {}B".format(size, power_dict[t_n])


async def int_to_alpha(user_id: int) -> str:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    text = ""
    user_id = str(user_id)
    for i in user_id:
        text += alphabet[int(i)]
    return text


async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
    user_id = ""
    for i in user_id_alphabet:
        index = alphabet.index(i)
        user_id += str(index)
    user_id = int(user_id)
    return user_id


def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))


def seconds_to_min(seconds):
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            return "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        elif h > 0:
            return "{:02d}:{:02d}:{:02d}".format(h, m, s)
        elif m > 0:
            return "{:02d}:{:02d}".format(m, s)
        elif s > 0:
            return "00:{:02d}".format(s)
    return "-"


def speed_converter(seconds, speed):
    if str(speed) == str("0.5"):
        seconds = seconds * 2
    if str(speed) == str("0.75"):
        seconds = seconds + ((50 * seconds) // 100)
    if str(speed) == str("1.5"):
        seconds = seconds - ((25 * seconds) // 100)
    if str(speed) == str("2.0"):
        seconds = seconds - ((50 * seconds) // 100)
    collect = seconds
    if seconds is not None:
        seconds = int(seconds)
        d, h, m, s = (
            seconds // (3600 * 24),
            seconds // 3600 % 24,
            seconds % 3600 // 60,
            seconds % 3600 % 60,
        )
        if d > 0:
            convert = "{:02d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
            return convert, collect
        elif h > 0:
            convert = "{:02d}:{:02d}:{:02d}".format(h, m, s)
            return convert, collect
        elif m > 0:
            convert = "{:02d}:{:02d}".format(m, s)
            return convert, collect
        elif s > 0:
            convert = "00:{:02d}".format(s)
            return convert, collect
    return "-"


def check_duration(file_path):
    command = [
        "ffprobe",
        "-loglevel",
        "quiet",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        file_path,
    ]

    pipe = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out, err = pipe.communicate()
    _json = json.loads(out)

    if "format" in _json:
        if "duration" in _json["format"]:
            return float(_json["format"]["duration"])

    if "streams" in _json:
        for s in _json["streams"]:
            if "duration" in s:
                return float(s["duration"])

    return "Unknown"

formats = [
    "webm",
    "mkv",
    "flv",
    "vob",
    "ogv",
    "ogg",
    "rrc",
    "gifv",
    "mng",
    "mov",
    "avi",
    "qt",
    "wmv",
    "yuv",
    "rm",
    "asf",
    "amv",
    "mp4",
    "m4p",
    "m4v",
    "mpg",
    "mp2",
    "mpeg",
    "mpe",
    "mpv",
    "m4v",
    "svi",
    "3gp",
    "3g2",
    "mxf",
    "roq",
    "nsv",
    "flv",
    "f4v",
    "f4p",
    "f4a",
    "f4b",
]

async def convert_to_image(message, client) -> [None, str]:
    """Convert Most Media Formats To Raw Image"""
    if not message:
        return None
    if not message.reply_to_message:
        return None
    final_path = None
    if not (
        message.reply_to_message.video
        or message.reply_to_message.photo
        or message.reply_to_message.sticker
        or message.reply_to_message.media
        or message.reply_to_message.animation
        or message.reply_to_message.audio
    ):
        return None
    if message.reply_to_message.photo:
        final_path = await message.reply_to_message.download()
    elif message.reply_to_message.sticker:
        if message.reply_to_message.sticker.mime_type == "image/webp":
            final_path = "webp_to_png_s_proton.png"
            path_s = await message.reply_to_message.download()
            im = Image.open(path_s)
            im.save(final_path, "PNG")
        else:
            path_s = await client.download_media(message.reply_to_message)
            final_path = "lottie_proton.png"
            cmd = (
                f"lottie_convert.py --frame 0 -if lottie -of png {path_s} {final_path}"
            )
            await run_cmd(cmd)
    elif message.reply_to_message.audio:
        thumb = message.reply_to_message.audio.thumbs[0].file_id
        final_path = await client.download_media(thumb)
    elif message.reply_to_message.video or message.reply_to_message.animation:
        final_path = "fetched_thumb.png"
        vid_path = await client.download_media(message.reply_to_message)
        await run_cmd(f"ffmpeg -i {vid_path} -filter:v scale=500:500 -an {final_path}")
    return final_path                                                                                     




async def resize_media(media: str, video: bool, fast_forward: bool) -> str:
    if video:
        info_ = Media_Info.data(media)
        width = info_["pixel_sizes"][0]
        height = info_["pixel_sizes"][1]
        sec = info_["duration_in_ms"]
        s = round(float(sec)) / 1000

        if height == width:
            height, width = 512, 512
        elif height > width:
            height, width = 512, -1
        elif width > height:
            height, width = -1, 512

        resized_video = f"{media}.webm"
        if fast_forward:
            if s > 3:
                fract_ = 3 / s
                ff_f = round(fract_, 2)
                set_pts_ = ff_f - 0.01 if ff_f > fract_ else ff_f
                cmd_f = f"-filter:v 'setpts={set_pts_}*PTS',scale={width}:{height}"
            else:
                cmd_f = f"-filter:v scale={width}:{height}"
        else:
            cmd_f = f"-filter:v scale={width}:{height}"
        fps_ = float(info_["frame_rate"])
        fps_cmd = "-r 30 " if fps_ > 30 else ""
        cmd = f"ffmpeg -i {media} {cmd_f} -ss 00:00:00 -to 00:00:03 -an -c:v libvpx-vp9 {fps_cmd}-fs 256K {resized_video}"
        _, error, __, ___ = await run_cmd(cmd)
        os.remove(media)
        return resized_video

    image = Image.open(media)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width * scale), int(image.height * scale))

    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = "sticker.png"
    image.save(resized_photo)
    os.remove(media)
    return resized_photo


import textwrap
async def add_text_img(image_path, text):
    font_size = 12
    stroke_width = 1

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="default.ttf",                                                                                       size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    char_width, char_height = draw.textbbox((0, 0), 'A', font=font)[2:4]
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            line_width, line_height = draw.textbbox((0, 0), line, font=font)[2:4]
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = draw.textbbox((0, 0), line, font=font)[2:4]
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="black",
                font=font,
                stroke_width=stroke_width,
            )
            y += line_height

    final_image = os.path.join("memify.webp")
    img.save(final_image, **img_info)
    return final_image




async def hd_stream_closed_kicked(client, update):
   logger.info(update)
   try:
       await remove_active_chat(update.chat_id)
       queues[update.chat_id].clear()
       playing[update.chat_id].clear()
   except Exception as e:
      logger.info(e)


async def end(client, update):

  try:
        collection.update_one(
            {"bot_id": clients["bot"].me.id},
           {"$push": {'dates': datetime.datetime.now()}},
            upsert=True
        )
  except Exception as e:
        logger.info(f"Error saving playtime: {e}")
  try:
    if update.chat_id in queues and queues[update.chat_id]:
      next_song = queues[update.chat_id].pop(0)
      if update.chat_id in playing:
       if update.stream_type == StreamEnded.Type.VIDEO:
         await client.leave_call(update.chat_id)
      playing[update.chat_id] = next_song
      await join_call(
          next_song['message'], 
          next_song['title'],
          next_song['yt_link'], 
          next_song['chat'], 
          next_song['by'], 
          next_song['duration'], 
          next_song['mode'], 
          next_song['thumb']
      )
    else:
      logger.info(f"Song queue for chat {update.chat_id} is empty.")
      await client.leave_call(update.chat_id)
      await remove_active_chat(update.chat_id)
      playing[update.chat_id].clear()
  except Exception as e:
    logger.info(f"Error in end function: {e}")

from yt_dlp import YoutubeDL
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton



async def join_call(message, title, youtube_link, chat, by, duration, mode, thumb):
    """Join voice call and start streaming"""
    try:
        chat_id = chat.id
        # Set audio flags based on mode
        audio_flags = MediaStream.Flags.IGNORE if mode == "audio" else None
        position = len(queues.get(chat_id)) if queues.get(chat_id) else 0
        print(youtube_link)
        # Create MediaStream with the appropriate URL
        await clients["call_py"].play(
            chat_id,
            MediaStream(
                youtube_link,
                AudioQuality.HIGH,
                VideoQuality.HD_720p,
                video_flags=audio_flags,
                ytdlp_parameters='--cookies-from-browser chrome',
            ),
        )
        
        # Update playing status and timestamp
        playing[chat_id] = {
            "message": message,
            "title": title,
            "yt_link": youtube_link,
            "chat": chat,
            "by": by,
            "duration": duration,
            "mode": mode,
            "thumb": thumb
        }
        played[chat_id] = int(time.time())
        
        # Add current time to database for statistics
        try:
            collection.update_one(
                {"bot_id": clients["bot"].me.id},
                {"$push": {"dates": datetime.datetime.now()}},
                upsert=True
            )
        except Exception as e:
            logger.info(f"Error saving playtime: {e}")
        
        # Creating the inline keyboard with buttons arranged in two rows
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(text="▷", callback_data="resume"),
                InlineKeyboardButton(text="II", callback_data="pause"),
                InlineKeyboardButton(text="‣‣I" if position <1 else f"‣‣I({position})", callback_data="skip"),
                InlineKeyboardButton(text="▢", callback_data="end"),
            ],
        [
            InlineKeyboardButton(
                text="🕹️ 𝐓яαᴘ 🕹️", url=f"https://t.me/HeartBeat_Offi"
            ),
            InlineKeyboardButton(
                text="🚀 𝐇ɛƖƖ 🚀", url=f"https://t.me/HeartBeat_Fam"
            )
        ],
        ])

        sent_message = await clients["bot"].send_photo(
            message.chat.id, thumb, play_styles[int(gvarstatus(OWNER_ID, "format") or 5)].format(

                f"[{lightyagami(title)[:15]}(https://t.me/{client.me.username}?start=vidid_{extract_video_id(youtube_link)})" if not os.path.exists(youtube_link) else  lightyagami(title)[:15], 
                duration, 
                by.mention()
            ),
            reply_markup=keyboard
        )
        
        asyncio.create_task(update_progress_button(sent_message, duration, chat))
        
        try:
            await message.delete()
        except Exception as e:
            logger.info(e)
            
        logger.info(f"Started streaming in chat {chat_id}: {title}")
        
    except NoActiveGroupCall:
        await clients["bot"].send_message(chat.id, "ERROR: No active group calls")
        return await remove_active_chat(chat.id)
    except GroupcallForbidden:
        await clients["bot"].send_message(chat.id, "ERROR: Telegram internal server error")
        return await remove_active_chat(chat.id)
    except Exception as e:
        await clients["bot"].send_message(chat.id, f"ERROR: {e}")
        return await remove_active_chat(chat.id)








from functools import wraps
from typing import Tuple, Optional

# Example usage:
async def is_active_chat(chat_id):
    if chat_id not in active:
        return False
    else:
        return True


def get_user_data(user_id, key):
    user_data = user_sessions.find_one({"user_id": user_id})
    if user_data and key in user_data:
        return user_data[key]
    return None

def gvarstatus(user_id, key):
    return get_user_data(user_id, key)




PLANS = {
    "standard": {"amount": 6900, "duration": 20, "merit": 0},   # ₹69 for 20 days
    "pro": {"amount": 17900, "duration": 60, "merit": 2}        # ₹180 for 60 days
}
