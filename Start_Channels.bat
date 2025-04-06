@echo off
venv\Scripts\activate
venv\Scripts\python.exe -m pip install pytubefix ffmpeg-python customtkinter pillow requests
venv\Scripts\python.exe main.py
