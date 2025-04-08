import os
import re
import tkinter
import customtkinter
import shutil
import subprocess
import sys
import threading
from pytubefix import YouTube, Channel, Playlist
from pytubefix.cli import on_progress
from PIL import Image
from functions import (AppConfig, COLORS, CcConfig, JSONConfig, load_config, find_file_by_string, count_files, format_time,
                       get_free_space, clean_string_regex, string_to_list, load_image_from_url, grid_remove_elements)


# dropdown with int for loop mode exit after int loops
# copy video id field
# delete partly converted file in channel target dir if aborted during conversion
# update channel config only restart configuration build from channel config file, not YT channel fetch again

app_title = "YTDL.video"
entry_width = 460
padding_x = 6
padding_y = 3
padding_y_factor = 2
tn_width = 14 * 16
tn_height = 14 * 9
video_title_width = 84
log_default = "    "
total_channel_videos = 0
total_channel_name = ""

video_list = []
video_list_restricted = []
video_watch_urls = []
elements_to_destroy = []
elements_to_destroy_loop = []


def update_channel_config(default_max_res, limit_resolution_to, default_min_duration_in_minutes, min_duration,
                           default_max_duration_in_minutes, max_duration, default_minimum_year, min_year,
                           default_maximum_year, max_year, default_only_restricted, only_restricted_videos,
                           default_skip_restricted, skip_restricted, default_minimum_views, min_video_views,
                           default_year_subfolders, year_subfolders_temp, default_exclude_videos, exclude_video_ids,
                           default_include_videos, include_video_ids, default_filter_words, video_name_filter) -> None:
    if (default_max_res != limit_resolution_to or default_min_duration_in_minutes != min_duration or
            default_max_duration_in_minutes != max_duration or default_minimum_year != min_year or
            default_maximum_year != max_year or default_only_restricted != only_restricted_videos or
            default_skip_restricted != skip_restricted or default_minimum_views != min_video_views or
            default_year_subfolders != year_subfolders_temp or default_exclude_videos != exclude_video_ids or
            default_include_videos != include_video_ids or default_filter_words != video_name_filter):

        app.focus_set()

        if default_max_res != limit_resolution_to:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_max_resolution", limit_resolution_to)
        if default_min_duration_in_minutes != min_duration:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_min_duration_in_minutes",
                               int(min_duration))
        if default_max_duration_in_minutes != max_duration:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_max_duration_in_minutes",
                               int(max_duration))
        if default_minimum_year != min_year:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_minimum_year", int(min_year))
        if default_maximum_year != max_year:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_maximum_year", int(max_year))
        if default_only_restricted != only_restricted_videos:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_only_restricted",
                               only_restricted_videos)
        if default_skip_restricted != skip_restricted:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_skip_restricted", skip_restricted)
        if default_minimum_views != min_video_views:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_minimum_views", int(min_video_views))
        if default_year_subfolders != year_subfolders_temp:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_year_subfolders", year_subfolders_temp)
        if default_exclude_videos != exclude_video_ids:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_exclude_video_ids", exclude_video_ids)
        if default_include_videos != include_video_ids:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_include_video_ids", include_video_ids)
        if default_filter_words != video_name_filter:
            JSONConfig.update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, "c_filter_words", video_name_filter)
        get_information()


def create_channel_config(default_max_res, limit_resolution_to, default_min_duration_in_minutes, min_duration,
                              default_max_duration_in_minutes, max_duration, default_minimum_year, min_year,
                              default_maximum_year, max_year, default_only_restricted, only_restricted_videos,
                              default_skip_restricted, skip_restricted, default_minimum_views, min_video_views,
                              default_year_subfolders, year_subfolders_temp, default_exclude_videos, exclude_video_ids,
                              default_include_videos, include_video_ids, default_filter_words,
                              video_name_filter) -> None:
    if (default_max_res != limit_resolution_to or default_min_duration_in_minutes != min_duration or
            default_max_duration_in_minutes != max_duration or default_minimum_year != min_year or
            default_maximum_year != max_year or default_only_restricted != only_restricted_videos or
            default_skip_restricted != skip_restricted or default_minimum_views != min_video_views or
            default_year_subfolders != year_subfolders_temp or default_exclude_videos != exclude_video_ids or
            default_include_videos != include_video_ids or default_filter_words != video_name_filter):
        json_max_res = ""
        if default_max_res != limit_resolution_to:
            json_max_res = limit_resolution_to
        json_min_duration_in_minutes = 0
        if default_min_duration_in_minutes != min_duration:
            json_min_duration_in_minutes = min_duration
        json_max_duration_in_minutes = 0
        if default_max_duration_in_minutes != max_duration:
            json_max_duration_in_minutes = max_duration
        json_min_year = 0
        if default_minimum_year != min_year:
            json_min_year = min_year
        json_max_year = 0
        if default_maximum_year != max_year:
            json_max_year = max_year
        json_only_restricted_videos = ""
        if default_only_restricted != only_restricted_videos:
            json_only_restricted_videos = only_restricted_videos
        json_skip_restricted = ""
        if default_skip_restricted != skip_restricted:
            json_skip_restricted = skip_restricted
        json_min_video_views = 0
        if default_minimum_views != min_video_views:
            json_min_video_views = min_video_views
        json_year_subfolders_temp = ""
        if default_year_subfolders != year_subfolders_temp:
            json_year_subfolders_temp = year_subfolders_temp
        json_exclude_video_ids = ""
        if default_exclude_videos != exclude_video_ids:
            json_exclude_video_ids = exclude_video_ids
        json_include_video_ids = ""
        if default_include_videos != include_video_ids:
            json_include_video_ids = include_video_ids
        json_video_name_filter = ""
        if default_filter_words != video_name_filter:
            json_video_name_filter = video_name_filter
        custom_values = {
            "c_max_resolution": json_max_res,
            "c_min_duration_in_minutes": int(json_min_duration_in_minutes),
            "c_max_duration_in_minutes": int(json_max_duration_in_minutes),
            "c_minimum_year": int(json_min_year),
            "c_maximum_year": int(json_max_year),
            "c_only_restricted": json_only_restricted_videos,
            "c_skip_restricted": json_skip_restricted,
            "c_minimum_views": int(json_min_video_views),
            "c_year_subfolders": json_year_subfolders_temp,
            "c_exclude_video_ids": json_exclude_video_ids,
            "c_include_video_ids": json_include_video_ids,
            "c_filter_words": json_video_name_filter
        }
        JSONConfig.create_json_config(ytchannel_path.get() + AppConfig.channel_config_path, custom_values)

        channel_config_label.configure(text="Channel config file found!", text_color=COLORS.green)
        # create_channel_config_button.grid_remove()
        create_channel_config_button.configure(text="Update channel config")


def on_closing():
    delete_temp_files()
    app.destroy()  # Ensures the window closes properly


def abort_download() -> None:
    sys.exit(0)


def clean_youtube_urls(to_clean_video_list: list) -> list[str]:
    prefix = youtube_watch_url
    return [to_clean_video.replace(prefix, "") for to_clean_video in to_clean_video_list]


def add_url_in_order(filename: str, a_url: str) -> None:
    global elements_to_destroy
    elements_to_destroy.remove(video_info_channel_button)
    video_info_channel_button.destroy()
    try:
        # Read existing URLs and remove empty lines
        with open(filename, "r", encoding="utf-8") as file:
            urls = sorted(set(line.strip() for line in file if line.strip()))  # Remove duplicates and sort

        # Check if the URL already exists
        if a_url in urls:
            # print("✅ URL already exists in the file.")
            return

        # Insert the new URL and sort again
        urls.append(a_url)
        urls.sort()

        # Write back the sorted list
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join(urls) + "\n")

        # print("✅ URL added to channels.txt.")
        after_adding_to_channels_txt_label.configure(text="URL added to channels.txt")
        after_adding_to_channels_txt_label.grid(row=3, column=3, padx=padding_x, pady=padding_y, sticky="nw")
        elements_to_destroy.append(after_adding_to_channels_txt_label)

        channel_dropdown.configure(values=read_channel_txt_lines("channels.txt"))

    except FileNotFoundError:
        print("⚠️ File not found. Creating a new one and adding the URL.")
        with open(filename, "w", encoding="utf-8") as file:
            file.write(a_url + "\n")


def organize_files_by_year(base_directory: str) -> None:
    if not os.path.exists(base_directory):
        print(f"Error: The directory '{base_directory}' does not exist.")
        return

    for file_name in os.listdir(base_directory):
        file_path = os.path.join(base_directory, file_name)

        # Ensure it's a file (not a folder)
        if os.path.isfile(file_path):
            # Extract year from filename (expects format: YYYY-...)
            parts = file_name.split("-")
            if parts[0].isdigit() and len(parts[0]) == 4:
                year = parts[0]
                year_folder = os.path.join(base_directory, year)

                # Create the year folder if it doesn't exist
                os.makedirs(year_folder, exist_ok=True)

                # Move the file to the corresponding year folder
                shutil.move(file_path, os.path.join(year_folder, file_name))
    # print(print_colored_text("Created year sub folder structure!", BCOLORS.ORANGE))


def contains_folder_starting_with_2(path: str) -> bool:
    if os.path.exists(path):
        return any(name.startswith("20") and os.path.isdir(os.path.join(path, name)) for name in os.listdir(path))
    else:
        return False


def make_year_subfolder_structure(path: str) -> None:
    if os.path.exists(path):
        if (not contains_folder_starting_with_2(path) and
                any(file.endswith((".mp4", ".mp3")) for file in os.listdir(path)
                    if os.path.isfile(os.path.join(path, file)))):
            organize_files_by_year(path)


def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent_completed = bytes_downloaded / total_size * 100
    percent = str(int(percent_completed))
    progress_percent.configure(text=percent + "%")
    progress_bar.set(float(percent_completed) / 100)
    progress_percent.update()


def delete_temp_files() -> None:
    video_file, audio_file = find_media_files(".")
    if video_file and os.path.exists(video_file):
        os.remove(video_file)
    if audio_file and os.path.exists(audio_file):
        os.remove(audio_file)


def format_view_count(number: int) -> str:
    if number >= 1_000_000_000:  # Billions
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:  # Millions
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:  # Thousands
        return f"{number / 1_000:.1f}K"
    else:
        return str(number)


def find_media_files(fmf_path: str) -> tuple[str | None, str | None]:
    video_file = None
    audio_file = None
    for file in os.listdir(fmf_path):
        if file.endswith((".mp4", ".webm")) and video_file is None:
            video_file = file
        elif file.endswith(".m4a") and audio_file is None:
            audio_file = file

        if video_file and audio_file:
            break  # Stop searching once both files are found

    return video_file, audio_file


def rename_files_in_temp_directory() -> None:
    """Removes ':' from filenames in a given directory."""
    directory = os.getcwd()
    if not os.path.exists(directory):
        print("Error: Directory does not exist!")
        return

    for filename in os.listdir(directory):
        if ":" in filename:  # Check if filename contains ':'
            sanitized_name = filename.replace(":", "")
            old_path = os.path.join(directory, filename)
            new_path = os.path.join(directory, sanitized_name)
            os.rename(old_path, new_path)


def create_directories(restricted: bool, year: str) -> None:
    if restricted:
        if not os.path.exists(ytchannel_path.get() + f"{str(year)}/restricted"):
            os.makedirs(ytchannel_path.get() + f"{str(year)}/restricted")
    else:
        if not os.path.exists(ytchannel_path.get() + f"{str(year)}"):
            os.makedirs(ytchannel_path.get() + f"{str(year)}")


def read_channel_txt_lines(filename: str) -> list[str]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            rc_lines = [line.strip() for line in file if not line.lstrip().startswith("#")]
        rc_lines.insert(0, "")
        return rc_lines
    except FileNotFoundError:
        print("❌ Error: File not found.")
        return []


def check_channels_txt(filename: str, c_url: str) -> bool:
    try:
        # Read existing URLs and remove empty lines
        with open(filename, "r", encoding="utf-8") as file:
            urls = sorted(set(line.strip() for line in file if line.strip()))  # Remove duplicates and sort

        if c_url in urls:
            # print("✅ URL already exists in the file.")
            return True
        else:
            return False
    except FileNotFoundError:
        # print("⚠️ File not found. Creating a new one and adding the URL.")
        # with open(filename, "w", encoding="utf-8") as file:
        #     file.write(url + "\n")
        return False


def update_download_log(text: str, color: str) -> None:
    download_log_label.configure(text=text, text_color=color)
    download_log_label.grid(row=23, column=2, columnspan=2, padx=padding_x, pady=padding_y, sticky="w")
    download_log_label.update()


def update_app_title():
    app.title(app_title + AppConfig.version + " - Free disk space: " + get_free_space(output_dir))


def update_video_counts(text: str):
    ytchannel_video_count.configure(text=text)


def get_yt_channel(channel_url) -> Channel:
    if web_client:
        channel = Channel(channel_url, 'WEB')
    else:
        channel = Channel(channel_url)
    return channel


def disable_buttons():
    video_button.configure(state="disabled")
    audio_button.configure(state="disabled")
    skip_videos.configure(state="disabled")
    get_information_button.configure(state="disabled")
    video_info_channel_button.configure(state="disabled")
    create_channel_config_button.configure(state="disabled")
    channel_dropdown.configure(state="disabled")
    link.configure(state="disabled")
    ytchannel_path.configure(state="disabled")
    # configuration_resolution.configure(state="disabled")
    # configuration_min_duration.configure(state="disabled")
    # configuration_max_duration.configure(state="disabled")
    # configuration_min_year.configure(state="disabled")
    # configuration_max_year.configure(state="disabled")
    # configuration_only_restricted.configure(state="disabled")
    # configuration_skip_restricted.configure(state="disabled")
    # configuration_min_views.configure(state="disabled")
    # configuration_year_subs.configure(state="disabled")
    # configuration_excludes.configure(state="disabled")
    # configuration_includes.configure(state="disabled")
    # configuration_filter_words.configure(state="disabled")


def enable_buttons():
    video_button.configure(state="normal")
    audio_button.configure(state="normal")
    skip_videos.configure(state="normal")
    get_information_button.configure(state="normal")
    video_info_channel_button.configure(state="normal")
    create_channel_config_button.configure(state="normal")
    channel_dropdown.configure(state="normal")
    link.configure(state="normal")
    ytchannel_path.configure(state="normal")
    # configuration_resolution.configure(state="normal")
    # configuration_min_duration.configure(state="normal")
    # configuration_max_duration.configure(state="normal")
    # configuration_min_year.configure(state="normal")
    # configuration_max_year.configure(state="normal")
    # configuration_only_restricted.configure(state="normal")
    # configuration_skip_restricted.configure(state="normal")
    # configuration_min_views.configure(state="normal")
    # configuration_year_subs.configure(state="normal")
    # configuration_excludes.configure(state="normal")
    # configuration_includes.configure(state="normal")
    # configuration_filter_words.configure(state="normal")


def get_information():
    if channel_dropdown.get() == "" and link.get() == "":
        update_download_log("Empty selection", COLORS.red)
    else:
        disable_buttons()
        update_download_log("", COLORS.gray)
        threading.Thread(target=get_information_work, daemon=True).start()


def get_information_work():
    global total_channel_videos
    global total_channel_name
    global elements_to_destroy

    update_app_title()
    looper = False
    if channel_dropdown.get() != "":
        channel_url = channel_dropdown.get()
        looper = True
    else:
        channel_url = link.get()

    after_adding_to_channels_txt_label.grid_remove()
    # destroy_elements()

    yt_channel = channel_url
    video_id_from_single_video = ""
    # ytv = ""
    if youtube_watch_url in yt_channel:
        if web_client:
            ytv = YouTube(yt_channel, 'WEB', on_progress_callback=on_progress)
        else:
            ytv = YouTube(yt_channel)
        yt_channel = ytv.channel_url
        video_id_from_single_video = ytv.video_id
    elif "https://" not in yt_channel:
        if web_client:
            ytv = YouTube(youtube_watch_url + yt_channel, 'WEB', on_progress_callback=on_progress)
        else:
            ytv = YouTube(youtube_watch_url + yt_channel)
        yt_channel = ytv.channel_url
        video_id_from_single_video = ytv.video_id
    elif "list=" in yt_channel:
        if web_client:
            playlist = Playlist(yt_channel, 'WEB')
        else:
            playlist = Playlist(yt_channel)
        yt_channel = playlist.owner_url
        for p_video in playlist.videos:
            video_id_from_single_video += p_video.video_id + ","
        video_id_from_single_video = video_id_from_single_video[:-1]
    else:
        looper = True

    channel_info = get_yt_channel(yt_channel)

    channel_info_name = channel_info.channel_name
    channel_info_url = channel_info.channel_url
    channel_info_video_urls = channel_info.video_urls
    count_files_from_channel_dir = count_files(output_dir + "/" +
                                               clean_string_regex(channel_info_name).rstrip(),
                                               ".mp4")
    update_video_counts(str(count_files_from_channel_dir) + " / " + str(len(channel_info.video_urls)) + " Videos downloaded")
    total_channel_videos = len(channel_info.video_urls)
    total_channel_name = channel_info_name
    channel_info_thumbnail = channel_info.thumbnail_url

    channel_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=0, pady=padding_y * padding_y_factor)
    elements_to_destroy.append(channel_frame)

    # separator1.grid(row=2, column=0, columnspan=4, sticky="ew", padx=padding_x, pady=padding_y * padding_y_factor)
    # elements_to_destroy.append(separator1)

    separator2.grid(row=6, column=0, columnspan=4, sticky="ew", padx=padding_x, pady=padding_y)
    elements_to_destroy.append(separator2)

    # separator3.grid(row=14, column=0, columnspan=4, sticky="ew", padx=padding_x, pady=padding_y)
    # elements_to_destroy.append(separator3)

    video_info_channel.grid(row=3, column=1, padx=padding_x, pady=padding_y * padding_y_factor, sticky="nw")
    elements_to_destroy.append(video_info_channel)
    video_info_channel.configure(text=channel_info_name[:29] + "..." if len(channel_info_name) > 29 else channel_info_name)
    video_info_channel_url.grid(row=3, column=2, padx=padding_x, pady=padding_y * padding_y_factor, sticky="nw")
    elements_to_destroy.append(video_info_channel_url)
    video_info_channel_url.configure(text=channel_info_url)
    if not check_channels_txt("channels.txt", channel_info_url):
        video_info_channel_button.configure(command=lambda: add_url_in_order("channels.txt", channel_info_url))
        video_info_channel_button.grid(row=3, column=3, padx=padding_x, pady=padding_y * padding_y_factor, sticky="nw")
        elements_to_destroy.append(video_info_channel_button)

    ytchannel_video_count.grid(row=4, column=1, padx=padding_x, pady=padding_y, sticky="nw")
    elements_to_destroy.append(ytchannel_video_count)

    ytchannel_path_label.grid(row=4, column=1, padx=padding_x, pady=padding_y, sticky="ne")
    elements_to_destroy.append(ytchannel_path_label)
    ytchannel_path.grid(row=4, column=2, padx=padding_x, pady=padding_y, sticky="nw")
    elements_to_destroy.append(ytchannel_path)
    ytchannel_path_var = tkinter.StringVar(value=output_dir + "/" + clean_string_regex(channel_info_name).rstrip())
    ytchannel_path.configure(textvariable=ytchannel_path_var)

    channel_config_label.grid(row=5, column=2, padx=padding_x, pady=padding_y, sticky="sw")
    elements_to_destroy.append(channel_config_label)

    yt_channel_thumbnail = load_image_from_url(channel_info_thumbnail, size=(tn_height, tn_height))
    channel_thumbnail_label.configure(image=yt_channel_thumbnail)
    channel_thumbnail_label.grid(row=3, column=0, rowspan=3, padx=padding_x, pady=padding_y * padding_y_factor * 2, sticky="ne")
    elements_to_destroy.append(channel_thumbnail_label)

    default_max_res = "max"
    default_min_duration_in_minutes = 0
    default_max_duration_in_minutes = 0
    default_minimum_year = 0
    default_maximum_year = 0
    default_only_restricted = ""
    default_skip_restricted = ""
    default_minimum_views = 0
    default_year_subfolders = ""
    default_exclude_videos = ""
    default_include_videos = ""
    default_filter_words = ""

    year_subfolders = False
    only_restricted = False
    skip_restricted = False
    min_duration_bool = False
    max_duration_bool = False

    if os.path.exists(ytchannel_path.get() + AppConfig.channel_config_path):
        incomplete_config = False
        incomplete_string = []
        # Load channel config
        channel_config = load_config(ytchannel_path.get() + AppConfig.channel_config_path)
        # Access and set settings
        if "c_max_resolution" in channel_config:
            if channel_config["c_max_resolution"] != "":
                default_max_res = channel_config["c_max_resolution"]
        else:
            incomplete_config = True
            incomplete_string.append("c_max_resolution")

        if "c_min_duration_in_minutes" in channel_config:
            if int(channel_config["c_min_duration_in_minutes"]) != 0:
                default_min_duration_in_minutes = channel_config["c_min_duration_in_minutes"]
                min_duration_bool = True
        else:
            incomplete_config = True
            incomplete_string.append("c_min_duration_in_minutes")

        if "c_max_duration_in_minutes" in channel_config:
            if int(channel_config["c_max_duration_in_minutes"]) != 0:
                default_max_duration_in_minutes = channel_config["c_max_duration_in_minutes"]
                max_duration_bool = True
        else:
            incomplete_config = True
            incomplete_string.append("c_max_duration_in_minutes")

        if "c_minimum_year" in channel_config:
            if int(channel_config["c_minimum_year"]) != 0:
                default_minimum_year = channel_config["c_minimum_year"]
        else:
            incomplete_config = True
            incomplete_string.append("c_minimum_year")

        if "c_maximum_year" in channel_config:
            if int(channel_config["c_maximum_year"]) != 0:
                default_maximum_year = channel_config["c_maximum_year"]
        else:
            incomplete_config = True
            incomplete_string.append("c_maximum_year")

        if "c_only_restricted" in channel_config:
            if channel_config["c_only_restricted"] != "":
                default_only_restricted = channel_config["c_only_restricted"]
                if default_only_restricted == "y":
                    only_restricted = True
        else:
            incomplete_config = True
            incomplete_string.append("c_only_restricted")

        if "c_skip_restricted" in channel_config:
            if channel_config["c_skip_restricted"] != "":
                default_skip_restricted = channel_config["c_skip_restricted"]
                if default_skip_restricted == "y":
                    skip_restricted = True
        else:
            incomplete_config = True
            incomplete_string.append("c_skip_restricted")

        if "c_minimum_views" in channel_config:
            if int(channel_config["c_minimum_views"]) != 0:
                default_minimum_views = channel_config["c_minimum_views"]
        else:
            incomplete_config = True
            incomplete_string.append("c_minimum_views")

        if "c_year_subfolders" in channel_config:
            if channel_config["c_year_subfolders"] != "":
                default_year_subfolders = channel_config["c_year_subfolders"]
                if default_year_subfolders == "y":
                    year_subfolders = True
        else:
            incomplete_config = True
            incomplete_string.append("c_year_subfolders")

        if "c_exclude_video_ids" in channel_config:
            if channel_config["c_exclude_video_ids"] != "":
                default_exclude_videos = channel_config["c_exclude_video_ids"]
        else:
            incomplete_config = True
            incomplete_string.append("c_exclude_video_ids")

        if "c_include_video_ids" in channel_config:
            if channel_config["c_include_video_ids"] != "":
                default_include_videos = channel_config["c_include_video_ids"]
        else:
            incomplete_config = True
            incomplete_string.append("c_include_video_ids")

        if "c_filter_words" in channel_config:
            if channel_config["c_filter_words"] != "":
                default_filter_words = channel_config["c_filter_words"]
        else:
            incomplete_config = True
            incomplete_string.append("c_filter_words")

        if incomplete_config:
            channel_config_label.configure(text=("Incomplete channel config file! --> Adding missing key(s) to file " +
                                                 str(incomplete_string)), text_color=COLORS.red)
            CcConfig.cc_check_and_update_json_config(ytchannel_path.get() + AppConfig.channel_config_path, AppConfig.REQUIRED_VIDEO_CHANNEL_CONFIG)
        else:
            channel_config_label.configure(text="Channel config file found!", text_color=COLORS.green)

        # create_channel_config_button.grid_remove()
        create_channel_config_button.configure(text="Update channel config")
        create_channel_config_button.configure(command=lambda: update_channel_config(default_max_res, "" if configuration_resolution.get() == "max" else configuration_resolution.get() ,
                                              default_min_duration_in_minutes, configuration_min_duration.get(),
                                              default_max_duration_in_minutes, configuration_max_duration.get(),
                                              default_minimum_year, configuration_min_year.get(),
                                              default_maximum_year, configuration_max_year.get(),
                                              default_only_restricted,
                                              "y" if configuration_only_restricted.get() == 1 else "",
                                              default_skip_restricted,
                                              "y" if configuration_skip_restricted.get() == 1 else "",
                                              default_minimum_views, configuration_min_views.get(),
                                              default_year_subfolders,
                                              "y" if configuration_year_subs.get() == 1 else "",
                                              default_exclude_videos, configuration_excludes.get("0.0", "end").strip(),
                                              default_include_videos, configuration_includes.get("0.0", "end").strip(),
                                              default_filter_words, configuration_filter_words.get("0.0", "end").strip()))

    else:
        channel_config_label.configure(text="No channel config file found!", text_color=COLORS.gray)
        create_channel_config_button.configure(command=lambda: create_channel_config(default_max_res, configuration_resolution.get(),
                                        default_min_duration_in_minutes, configuration_min_duration.get(),
                                        default_max_duration_in_minutes, configuration_max_duration.get(),
                                        default_minimum_year, configuration_min_year.get(),
                                        default_maximum_year, configuration_max_year.get(),
                                        default_only_restricted, "y" if configuration_only_restricted.get() == 1 else "",
                                        default_skip_restricted, "y" if configuration_skip_restricted.get() == 1 else "",
                                        default_minimum_views, configuration_min_views.get(),
                                        default_year_subfolders, "y" if configuration_year_subs.get() == 1 else "",
                                        default_exclude_videos, configuration_excludes.get("0.0", "end").strip(),
                                        default_include_videos, configuration_includes.get("0.0", "end").strip(),
                                        default_filter_words, configuration_filter_words.get("0.0", "end").strip()))
        create_channel_config_button.configure(text="Create channel config")

    create_channel_config_button.grid(row=5, column=3, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(create_channel_config_button)

    # channel config settings
    configuration_resolution_label = customtkinter.CTkLabel(channel_frame, text="Max. Resolution:")
    configuration_resolution_label.grid(row=7, column=0, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_resolution_label)
    res_values = ["max", "2160p", "1440p", "1080p", "720p", "480p"]
    configuration_resolution.configure(values=res_values, width=100)
    configuration_resolution.set(default_max_res)
    configuration_resolution.grid(row=7, column=1, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_resolution)

    configuration_min_views_label = customtkinter.CTkLabel(channel_frame, text="Min. Views:")
    configuration_min_views_label.grid(row=7, column=1, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_min_views_label)
    min_views_value = tkinter.StringVar(value=default_minimum_views)
    # min_views_value.trace_add("write", on_change)
    configuration_min_views.configure(width=100, textvariable=min_views_value)
    configuration_min_views.grid(row=7, column=2, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_min_views)

    configuration_year_subs_label = customtkinter.CTkLabel(channel_frame, text="Year sub dir structure:")
    configuration_year_subs_label.grid(row=7, column=2, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_year_subs_label)
    configuration_year_subs.configure(text="")
    if year_subfolders:
        configuration_year_subs.select()
    else:
        configuration_year_subs.deselect()
    configuration_year_subs.grid(row=7, column=3, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_year_subs)

    configuration_min_duration_label = customtkinter.CTkLabel(channel_frame, text="Min. duration (m):")
    configuration_min_duration_label.grid(row=8, column=0, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_min_duration_label)
    min_duration_value = tkinter.StringVar(value=default_min_duration_in_minutes)
    # min_duration_value.trace_add("write", on_change)
    configuration_min_duration.configure(width=100, textvariable=min_duration_value)
    configuration_min_duration.grid(row=8, column=1, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_min_duration)

    configuration_max_duration_label = customtkinter.CTkLabel(channel_frame, text="Max. duration (m):")
    configuration_max_duration_label.grid(row=8, column=1, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_max_duration_label)
    max_duration_value = tkinter.StringVar(value=default_max_duration_in_minutes)
    configuration_max_duration.configure(width=100, textvariable=max_duration_value)
    configuration_max_duration.grid(row=8, column=2, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_max_duration)

    configuration_skip_restricted_label = customtkinter.CTkLabel(channel_frame, text="Skip restricted:")
    configuration_skip_restricted_label.grid(row=8, column=2, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_skip_restricted_label)
    configuration_skip_restricted.configure(text="")
    if skip_restricted:
        configuration_skip_restricted.select()
    else:
        configuration_skip_restricted.deselect()
    configuration_skip_restricted.grid(row=8, column=3, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_skip_restricted)

    configuration_only_restricted_label = customtkinter.CTkLabel(channel_frame, text="Only restricted:")
    configuration_only_restricted_label.grid(row=9, column=2, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_only_restricted_label)
    configuration_only_restricted.configure(text="")
    if only_restricted:
        configuration_only_restricted.select()
    else:
        configuration_only_restricted.deselect()
    configuration_only_restricted.grid(row=9, column=3, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_only_restricted)

    # min year
    configuration_min_year_label = customtkinter.CTkLabel(channel_frame, text="Min. year:")
    configuration_min_year_label.grid(row=9, column=0, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_min_year_label)
    min_year_value = tkinter.StringVar(value=default_minimum_year)
    configuration_min_year.configure(width=100, textvariable=min_year_value)
    configuration_min_year.grid(row=9, column=1, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_min_year)

    # max year
    configuration_max_year_label = customtkinter.CTkLabel(channel_frame, text="Max. year:")
    configuration_max_year_label.grid(row=9, column=1, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy.append(configuration_max_year_label)
    max_year_value = tkinter.StringVar(value=default_maximum_year)
    configuration_max_year.configure(width=100, textvariable=max_year_value)
    configuration_max_year.grid(row=9, column=2, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy.append(configuration_max_year)

    # filter words
    configuration_filter_words_label = customtkinter.CTkLabel(channel_frame, text="Filter words:")
    configuration_filter_words_label.grid(row=10, column=0, padx=padding_x, pady=padding_y, sticky="en")
    elements_to_destroy.append(configuration_filter_words_label)
    configuration_filter_words.configure(width=170, height=50, fg_color=("white", "gray20"),  # Match Entry background color
                                                        border_color=("gray60", "gray40"),  # Match Entry border color
                                                        border_width=2, corner_radius=6)
    configuration_filter_words.delete("0.0", "end")
    configuration_filter_words.insert("0.0", default_filter_words)
    configuration_filter_words.grid(row=10, column=1, padx=padding_x, pady=padding_y, sticky="wn")
    elements_to_destroy.append(configuration_filter_words)

    # excludes
    configuration_excludes_label = customtkinter.CTkLabel(channel_frame, text="Excludes:")
    configuration_excludes_label.grid(row=10, column=1, padx=padding_x, pady=padding_y, sticky="en")
    elements_to_destroy.append(configuration_excludes_label)
    configuration_excludes.configure(width=300, height=50, fg_color=("white", "gray20"),  # Match Entry background color
                                                        border_color=("gray60", "gray40"),  # Match Entry border color
                                                        border_width=2, corner_radius=6)
    configuration_excludes.delete("0.0", "end")
    configuration_excludes.insert("0.0", default_exclude_videos)
    configuration_excludes.grid(row=10, column=2, padx=padding_x, pady=padding_y, sticky="wn")
    elements_to_destroy.append(configuration_excludes)

    # includes
    configuration_includes_label = customtkinter.CTkLabel(channel_frame, text="Includes:")
    configuration_includes_label.grid(row=10, column=2, padx=padding_x, pady=padding_y, sticky="en")
    elements_to_destroy.append(configuration_includes_label)
    configuration_includes.configure(width=170, height=50, fg_color=("white", "gray20"),  # Match Entry background color
                                                        border_color=("gray60", "gray40"),  # Match Entry border color
                                                        border_width=2, corner_radius=6)
    configuration_includes.delete("0.0", "end")
    configuration_includes.insert("0.0", default_include_videos)
    configuration_includes.grid(row=10, column=3, padx=padding_x, pady=padding_y, sticky="wn")
    elements_to_destroy.append(configuration_includes)

    # fill here channel config settings
    exclude_list = []
    if default_exclude_videos != "":
        exclude_list = clean_youtube_urls(string_to_list(default_exclude_videos))

    include_list = []
    if default_include_videos != "":
        include_list = clean_youtube_urls(string_to_list(default_include_videos))

    only_restricted_videos_bool = False
    if configuration_only_restricted.get() == 1:
        only_restricted_videos_bool = True

    skip_restricted_bool = False
    if configuration_skip_restricted.get() == 1:
        skip_restricted_bool = True

    count_total_videos = 0

    # Create empty lists
    global video_list
    global video_list_restricted
    video_list.clear()
    video_list_restricted.clear()

    global video_watch_urls
    video_watch_urls.clear()

    if len(include_list) > 0:
        for include in include_list:
            video_watch_urls.append(youtube_watch_url + include)
    else:
        for url in channel_info_video_urls:
            count_total_videos += 1
            if url.video_id not in exclude_list:
                if len(include_list) > 0:
                    if url.video_id in include_list:
                        video_watch_urls.append(url.watch_url)
                # else:
                video_watch_urls.append(url.watch_url)
    video_math = customtkinter.CTkLabel(channel_frame, text=str(len(video_watch_urls)) + " (total videos minus excludes)", text_color=COLORS.gray)
    video_math.grid(row=5, column=1, padx=padding_x, pady=padding_y, sticky="sw")
    elements_to_destroy.append(video_math)

    # channel_videos_combobox = customtkinter.CTkComboBox(app, values=video_watch_urls)
    # channel_videos_combobox.grid(row=10, column=2, columnspan=2, padx=padding_x, pady=padding_y, sticky="se")
    # elements_to_destroy.append(channel_videos_combobox)

    restricted_video = False

    if video_id_from_single_video != "":
        yt_video_title_label.configure(text="Title:", text_color=COLORS.gray)
        yt_video_title_label.grid(row=15, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy.append(yt_video_title_label)
        yt_video_title.configure(text=str(ytv.title)[:video_title_width] +
                        "..." if len(str(ytv.title)) > video_title_width else str(ytv.title), font=("Arial", 15, "bold"))
        if ytv.age_restricted:
            yt_video_title.configure(text_color=COLORS.red)
            restricted_video = True
            # log_label.configure(text="Restricted Video!", text_color=COLORS.red)
        yt_video_title.grid(row=15, column=2, columnspan=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy.append(yt_video_title)

        yt_video_views_label.configure(text="Views:", text_color=COLORS.gray)
        yt_video_views_label.grid(row=16, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy.append(yt_video_views_label)
        yt_video_views.configure(text=format_view_count(ytv.views))
        yt_video_views.grid(row=16, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy.append(yt_video_views)

        yt_video_date_label.configure(text="Date:", text_color=COLORS.gray)
        yt_video_date_label.grid(row=17, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy.append(yt_video_date_label)
        yt_video_date.configure(text=ytv.publish_date.strftime(AppConfig.date_format_display))
        yt_video_date.grid(row=17, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy.append(yt_video_date)

        yt_video_length_label.configure(text="Length:", text_color=COLORS.gray)
        yt_video_length_label.grid(row=18, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy.append(yt_video_length_label)
        yt_video_length.configure(text=format_time(ytv.length))
        yt_video_length.grid(row=18, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy.append(yt_video_length)

        yt_video_thumbnail = load_image_from_url(ytv.thumbnail_url, size=(tn_width, tn_height))
        video_thumbnail_label.configure(image=yt_video_thumbnail, text="")
        video_thumbnail_label.grid(row=15, column=0, rowspan=4, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy.append(video_thumbnail_label)

        yt_video_id_value = tkinter.StringVar(value=ytv.video_id)
        yt_video_id.configure(textvariable=yt_video_id_value)
        yt_video_id.grid(row=20, column=0, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy.append(yt_video_id)



    audio_button.grid(row=13, column=1, padx=padding_x, pady=padding_y * padding_y_factor * 2, sticky="e")
    elements_to_destroy.append(audio_button)

    if looper:
        audio_button.configure(command=lambda: loop_download(True, configuration_resolution.get(),
                                                                configuration_filter_words.get("0.0", "end").strip(),
                                                                only_restricted_videos_bool, skip_restricted_bool,
                                                                True if configuration_year_subs.get() == 1 else False,
                                                                min_duration_bool, configuration_min_duration.get(),
                                                                max_duration_bool, configuration_max_duration.get(),
                                                                configuration_min_year.get(), configuration_max_year.get(),
                                                                configuration_min_views.get()))
        video_button.configure(command=lambda: loop_download(False, configuration_resolution.get(),
                                                                configuration_filter_words.get("0.0", "end").strip(),
                                                                only_restricted_videos_bool, skip_restricted_bool,
                                                                True if configuration_year_subs.get() == 1 else False,
                                                                min_duration_bool, configuration_min_duration.get(),
                                                                max_duration_bool, configuration_max_duration.get(),
                                                                configuration_min_year.get(), configuration_max_year.get(),
                                                                configuration_min_views.get()))
    else:
        audio_button.configure(command=lambda: start_download(True, restricted_video, ytv.video_id,
                                                              False, True if configuration_year_subs.get() == 1 else False))
        video_button.configure(command=lambda: start_download(False, restricted_video, ytv.video_id,
                                                              False, True if configuration_year_subs.get() == 1 else False))
    video_button.grid(row=13, column=2, padx=padding_x, pady=padding_y * padding_y_factor * 2, sticky="w")
    elements_to_destroy.append(video_button)

    skip_videos_value.set("0")
    skip_videos.configure(fg_color=COLORS.violet, width=20)
    skip_videos.grid(row=13, column=3, padx=padding_x, pady=padding_y * padding_y_factor * 2, sticky="w")
    elements_to_destroy.append(skip_videos)

    ##### AUDIO OR VIDEO BUTTON ##### AUDIO OR VIDEO BUTTON ##### AUDIO OR VIDEO BUTTON ##### AUDIO OR VIDEO BUTTON
    ##### AUDIO OR VIDEO BUTTON #####                             AUDIO OR VIDEO BUTTON ##### AUDIO OR VIDEO BUTTON
    ##### AUDIO OR VIDEO BUTTON ##### AUDIO OR VIDEO BUTTON ##### AUDIO OR VIDEO BUTTON ##### AUDIO OR VIDEO BUTTON

    # if count_files_from_channel_dir >= len(video_watch_urls):
    #     video_button.grid_remove()
    #     audio_button.grid_remove()

    enable_buttons()


def print_resolutions(yt: YouTube) -> list[str]:
    streams = yt.streams.filter(file_extension='mp4')  # StreamQuery object
    # Convert StreamQuery to a formatted string
    stream_string = "\n".join([str(stream) for stream in streams])
    # Extract resolutions using regex
    resolutions = re.findall(r'res="(\d+p)"', stream_string)
    # Remove duplicates and sort in descending order
    unique_resolutions = sorted(set(resolutions), key=lambda x: int(x[:-1]), reverse=True)

    return unique_resolutions


def limit_resolution(resolution: str, limit: str) -> str:
    num_resolution = int(''.join(filter(str.isdigit, resolution)))  # Extract number from first resolution
    num_limit: int = 0
    if limit!="max":
        num_limit = int(''.join(filter(str.isdigit, limit)))  # Extract number from second resolution
    if limit=="max" or num_resolution < num_limit:
        max_resolution = resolution
    else:
        max_resolution = limit

    return max_resolution


def loop_download(audio_or_video_bool, default_max_res, default_filter_words, only_restricted_videos_bool,
                        skip_restricted_bool, year_subfolders, min_duration_bool, min_duration, max_duration_bool, max_duration,
                        min_year, max_year, min_video_views):
    disable_buttons()
    t_loop_download = threading.Thread(target=lambda: loop_download_work(audio_or_video_bool, default_max_res, default_filter_words, only_restricted_videos_bool,
                        skip_restricted_bool, year_subfolders, min_duration_bool, min_duration, max_duration_bool, max_duration,
                        min_year, max_year, min_video_views), daemon=True)
    t_loop_download.start()
    # t_loop_download.join()


def reset_config_entry_box_colors():
    configuration_min_duration.configure(fg_color="gray20")
    configuration_max_duration.configure(fg_color="gray20")
    configuration_filter_words.configure(fg_color="gray20")
    configuration_min_year.configure(fg_color="gray20")
    configuration_max_year.configure(fg_color="gray20")
    configuration_min_views.configure(fg_color="gray20")


def loop_download_work(audio_or_video_bool, default_max_res, default_filter_words, only_restricted_videos_bool,
                        skip_restricted_bool, year_subfolders, min_duration_bool, min_duration, max_duration_bool, max_duration,
                        min_year, max_year, min_video_views):
    count_restricted_videos = 0
    count_ok_videos = 0
    count_this_run = 0
    count_skipped = 0
    v_counter = 0
    skip_count = int(skip_videos.get())

    global video_watch_urls
    global elements_to_destroy_loop

    for url in video_watch_urls:
        only_video_id = str(url).split("=")[1]
        v_counter += 1
        # only_video_id = pytubefix.extract.video_id(url)

        if v_counter >= skip_count:
            if find_file_by_string(ytchannel_path.get(), only_video_id, default_max_res, audio_or_video_bool) is not None:
                count_ok_videos += 1
                count_skipped += 1
                update_download_log("Skipping   " + str(count_skipped) + "   already downloaded Video(s)", COLORS.violet)
                reset_config_entry_box_colors()
            else:
                do_not_download = 0
                grid_remove_elements(elements_to_destroy_loop)
                if web_client:
                    video = YouTube(youtube_watch_url + only_video_id, 'WEB', on_progress_callback=on_progress)
                else:
                    video = YouTube(youtube_watch_url + only_video_id, on_progress_callback=on_progress)

                v_title_text_length = 42
                v_title = video.title[:v_title_text_length] + "..." if len(video.title) > v_title_text_length else video.title
                v_title_update_full = (str(v_counter) + "/" + str(len(video_watch_urls)) + "  |  " +
                                     str(video.publish_date.strftime(AppConfig.date_format_display)) + "  |  " +
                                     format_time(video.length) + "  |  " +
                                     ("R" if video.age_restricted else "_") + "  |  " +
                                     format_view_count(video.views) + "  |  " +
                                     v_title)
                update_download_log("Searching match:  " + v_title_update_full, COLORS.violet)

                # configuration_min_year.configure(fg_color="gray20")
                # configuration_max_year.configure(fg_color="gray20")
                # configuration_min_views.configure(fg_color="gray20")

                if default_filter_words != "":
                    configuration_filter_words.configure(fg_color=COLORS.dark_red)

                if default_filter_words == "" or any(
                        word.lower() in video.title.lower() for word in string_to_list(default_filter_words)):
                    if default_filter_words != "":
                        configuration_filter_words.configure(fg_color=COLORS.dark_green)
                    if min_duration_bool:
                        video_duration = int(video.length)
                        configuration_min_duration.configure(fg_color=COLORS.dark_green)
                        if video_duration <= int(min_duration) * 60:
                            do_not_download = 1
                            configuration_min_duration.configure(fg_color=COLORS.dark_red)
                    if max_duration_bool and max_duration > min_duration:
                        video_duration = int(video.length)
                        configuration_max_duration.configure(fg_color=COLORS.dark_green)
                        if video_duration >= int(max_duration) * 60:
                            do_not_download = 1
                            configuration_max_duration.configure(fg_color=COLORS.dark_red)
                        # separator2.update()
                    if int(min_year) > 0:
                        configuration_min_year.configure(fg_color=COLORS.dark_green)
                        if int(video.publish_date.strftime("%Y")) <= int(min_year):
                            configuration_min_year.configure(fg_color=COLORS.dark_red)
                            # do_not_download = 1
                            break
                    if int(max_year) > 0:
                        configuration_max_year.configure(fg_color=COLORS.dark_green)
                        if int(video.publish_date.strftime("%Y")) >= int(max_year):
                            do_not_download = 1
                            configuration_max_year.configure(fg_color=COLORS.dark_red)
                    if int(min_video_views) > 0:
                        configuration_min_views.configure(fg_color=COLORS.dark_green)
                        if video.views <= int(min_video_views):
                            do_not_download = 1
                            configuration_min_views.configure(fg_color=COLORS.dark_red)

                    # v_title_text_length = 42
                    v_title = video.title[:v_title_text_length] + "..." if len(video.title) > v_title_text_length else video.title
                    update_download_log(("Searching match:  " if do_not_download == 1 else "Found match!  ") +
                                        v_title_update_full, COLORS.violet)

                    if (not video.age_restricted and
                            video.vid_info.get('playabilityStatus', {}).get('status') != 'UNPLAYABLE' and
                            video.vid_info.get('playabilityStatus', {}).get('status') != 'LIVE_STREAM_OFFLINE' and
                            do_not_download == 0 and not only_restricted_videos_bool):
                        count_ok_videos += 1
                        count_this_run += 1
                        # count_skipped = 0
                        video_list.append(video.video_id)

                        start_download_work(audio_or_video_bool, False, video.video_id, True, year_subfolders)
                    else:
                        if not skip_restricted_bool:
                            if (video.age_restricted and video.vid_info.get('playabilityStatus', {}).get(
                                    'status') != 'UNPLAYABLE' and
                                    video.vid_info.get('playabilityStatus', {}).get(
                                        'status') != 'LIVE_STREAM_OFFLINE' and
                                    do_not_download == 0):
                                count_restricted_videos += 1
                                count_ok_videos += 1
                                count_this_run += 1
                                video_list_restricted.append(video.video_id)

                                start_download_work(audio_or_video_bool, True, video.video_id, True, year_subfolders)


                update_video_counts(
                    str(count_files(output_dir + "/" + clean_string_regex(total_channel_name).rstrip(), ".mp4")) +
                    " / " + str(total_channel_videos) + " Videos downloaded")

        channel_frame.update()

    if count_this_run == 0:
        update_download_log("Nothing to do...", COLORS.green)
    else:
        enable_buttons()
        update_download_log("DONE!", COLORS.green)



def start_download(audio_or_video_bool: bool, restricted: bool, video_id: str, looper: bool, year_subfolders: bool):
    disable_buttons()
    t_start_download_b = threading.Thread(target=lambda: start_download_work(audio_or_video_bool, restricted, video_id, looper, year_subfolders), daemon=True)
    t_start_download_b.start()
    # t_start_download_b.join()


def start_download_work(audio_or_video_bool: bool, restricted: bool, video_id: str, looper: bool, year_subfolders: bool):
    global elements_to_destroy_loop
    update_app_title()
    if restricted:
        if web_client:
            y_tube = YouTube(youtube_watch_url + video_id, 'WEB', use_oauth=True, allow_oauth_cache=True,
                     on_progress_callback=on_progress)
        else:
            y_tube = YouTube(youtube_watch_url + video_id, use_oauth=True, allow_oauth_cache=True,
                             on_progress_callback=on_progress)
    else:
        if web_client:
            y_tube = YouTube(youtube_watch_url + video_id, 'WEB', on_progress_callback=on_progress)
        else:
            y_tube = YouTube(youtube_watch_url + video_id, on_progress_callback=on_progress)

    if looper:
        yt_video_thumbnail = load_image_from_url(y_tube.thumbnail_url, size=(tn_width, tn_height))
        video_thumbnail_label.configure(image=yt_video_thumbnail, text="")
        video_thumbnail_label.grid(row=15, column=0, rowspan=4, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy_loop.append(video_thumbnail_label)

        yt_video_id_value = tkinter.StringVar(value=y_tube.video_id)
        yt_video_id.configure(textvariable=yt_video_id_value)
        yt_video_id.grid(row=20, column=0, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy_loop.append(yt_video_id)

        yt_video_title_label.configure(text="Title:", text_color=COLORS.gray)
        yt_video_title_label.grid(row=15, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy_loop.append(yt_video_title_label)
        yt_video_title.configure(text=str(y_tube.title)[:video_title_width] +
                        "..." if len(str(y_tube.title)) > video_title_width else str(y_tube.title), text_color=COLORS.white, font=("Arial", 15, "bold"))
        if restricted:
            yt_video_title.configure(text_color=COLORS.red)
            # log_label.configure(text="Restricted Video!", text_color=COLORS.red)
        yt_video_title.grid(row=15, column=2, columnspan=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy_loop.append(yt_video_title)

        yt_video_views_label.configure(text="Views:", text_color=COLORS.gray)
        yt_video_views_label.grid(row=16, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy_loop.append(yt_video_views_label)
        yt_video_views.configure(text=format_view_count(y_tube.views))
        yt_video_views.grid(row=16, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy_loop.append(yt_video_views)

        yt_video_date_label.configure(text="Date:", text_color=COLORS.gray)
        yt_video_date_label.grid(row=17, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy_loop.append(yt_video_date_label)
        yt_video_date.configure(text=y_tube.publish_date.strftime(AppConfig.date_format_display))
        yt_video_date.grid(row=17, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy_loop.append(yt_video_date)

        yt_video_length_label.configure(text="Length:", text_color=COLORS.gray)
        yt_video_length_label.grid(row=18, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy_loop.append(yt_video_length_label)
        yt_video_length.configure(text=format_time(y_tube.length))
        yt_video_length.grid(row=18, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy_loop.append(yt_video_length)

    res = ""
    if not audio_or_video_bool:
        res = max(print_resolutions(y_tube), key=lambda x: int(x.rstrip('p')))
        if str(configuration_resolution.get()) != "max":
            res = limit_resolution(res, str(configuration_resolution.get()))
        video_resolution_label.configure(text="Resolution:", text_color=COLORS.gray)
        video_resolution_label.grid(row=19, column=1, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy_loop.append(video_resolution_label)
        video_resolution.configure(values=print_resolutions(y_tube))
        video_resolution.set(str(res))
        video_resolution.grid(row=19, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy_loop.append(video_resolution)
        avail_resolutions.configure(text=str(print_resolutions(y_tube)), text_color=COLORS.gray)
        avail_resolutions.grid(row=20, column=2, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy_loop.append(avail_resolutions)

    ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON
    ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON                       ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON
    ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON ##### DOWNLOAD BUTTON

    if looper:
        download_video(audio_or_video_bool, y_tube, res, restricted, year_subfolders, looper)
    else:
        # enable_buttons()
        download_button.configure(text="Download", command=lambda: download_video(audio_or_video_bool, y_tube,
                                                                                  video_resolution.get(),
                                                                                  restricted, year_subfolders, looper))
        download_button.grid(row=21, column=2, padx=padding_x, pady=padding_y * padding_y_factor, sticky="w")
        global elements_to_destroy
        elements_to_destroy.append(download_button)


def download_video(audio_or_video_bool: bool, y_tube: YouTube, res: str, restricted: bool, year_subfolders: bool, looper: bool):
    if not looper:
        # enable_buttons()
        t_download_video = threading.Thread(target=lambda: download_video_work(audio_or_video_bool, y_tube, res, restricted, year_subfolders), daemon=True)
        t_download_video.start()
    else:
        download_video_work(audio_or_video_bool, y_tube, res, restricted, year_subfolders)


def download_video_work(audio_or_video_bool: bool, y_tube: YouTube, res: str, restricted: bool, year_subfolders: bool):
    global elements_to_destroy_loop

    abort_button.configure(fg_color=COLORS.dark_red, command=abort_download)
    abort_button.grid(row=22, column=3, rowspan=2, padx=padding_x, pady=padding_y, sticky="nw")
    elements_to_destroy_loop.append(abort_button)

    progress_percent.configure(text="0%")
    progress_percent.grid(row=22, column=1, padx=padding_x, pady=padding_y, sticky="e")
    elements_to_destroy_loop.append(progress_percent)

    progress_bar.set(0)
    progress_bar.configure(progress_color=COLORS.green)
    progress_bar.grid(row=22, column=2, padx=padding_x, pady=padding_y, sticky="w")
    elements_to_destroy_loop.append(progress_bar)

    update_download_log("", COLORS.gray)

    y_tube_publish_date = y_tube.publish_date
    y_tube_title = y_tube.title
    restricted_path_snippet = ""
    if restricted:
        restricted_path_snippet = "restricted/"

    try:
        publishing_date = y_tube_publish_date.strftime(AppConfig.date_format_math)
    except Exception as eee:
        publishing_date = eee

    update_download_log("Starting download to " + ytchannel_path.get(), COLORS.gray)

    if year_subfolders:
        year = "/" + str(y_tube_publish_date.strftime("%Y"))
        make_year_subfolder_structure(ytchannel_path.get())
    else:
        year = ""

    if os.path.exists(
            ytchannel_path.get() + year + "/" + restricted_path_snippet + str(publishing_date) + " - " + res + " - " +
            clean_string_regex(y_tube_title) + " - " + y_tube.video_id + ".mp4"):
        update_download_log("Video already downloaded", COLORS.dark_green)
    else:
        if audio_or_video_bool:
            if os.path.exists(ytchannel_path.get() + year + "/" + restricted_path_snippet +
                              str(publishing_date) + " - " + clean_string_regex(
                y_tube_title) + " - " + y_tube.video_id + ".mp3"):
                update_download_log("MP3 already downloaded", COLORS.dark_green)

        more_than1080p = False

        if res == "2160p" or res == "1440p":
            more_than1080p = True
            video_file_tmp, audio_file_tmp = find_media_files("tmp")
            if video_file_tmp is not None:
                path = (ytchannel_path.get() + str(year) + "/" + restricted_path_snippet + str(
                    publishing_date) + " - " + res + " - "
                        + clean_string_regex(os.path.splitext(video_file_tmp)[0]) + " - " + y_tube.video_id + ".mp4")
                update_download_log("Merged file still available!", COLORS.gray)
                convert_webm_to_mp4("tmp/" + video_file_tmp, path, year, restricted)
            else:
                download_video_process(audio_or_video_bool, y_tube, res, more_than1080p, publishing_date, year, restricted)
        else:
            download_video_process(audio_or_video_bool, y_tube, res, more_than1080p, publishing_date, year, restricted)


def download_video_process(audio_or_video_bool: bool, yt: YouTube, res: str, more_than1080p: bool, publishing_date: str, year: str,
                           restricted: bool) -> None:
    if not audio_or_video_bool:
        update_download_log("Downloading VIDEO...", COLORS.gray)
        for idx, i in enumerate(yt.streams):
            if i.resolution == res:
                break
        yt.streams[idx].download()

    update_download_log("Downloading AUDIO...", COLORS.gray)
    for idx, i in enumerate(yt.streams):
        if i.bitrate == "128kbps":
            break
    yt.streams[idx].download()

    rename_files_in_temp_directory()

    if audio_or_video_bool:
        convert_m4a_to_mp3(yt.video_id, publishing_date, year, restricted)
    else:
        if more_than1080p:
            convert_m4a_to_opus_and_merge(yt.video_id, publishing_date, res, year, restricted)
        else:
            merge_video_audio(yt.video_id, publishing_date, res, year, restricted)


def convert_m4a_to_mp3(video_id: str, publish_date: str, year: str, restricted: bool) -> None:
    video_file, audio_file = find_media_files(".")
    if not audio_file:
        print("❌ No M4A files found in the current directory.")
        return

    restricted_path = "/"
    if restricted:
        restricted_path = "/restricted/"

    create_directories(restricted, year)
    output_file = (ytchannel_path.get() + str(year) + restricted_path + publish_date +
                   " - " + clean_string_regex(os.path.splitext(audio_file)[0]) + " - " + video_id + ".mp3")
    update_download_log("Converting to MP3...", COLORS.gray)
    try:
        command = [
            "ffmpeg", "-loglevel", "quiet", "-stats",
            "-i", audio_file,  # Input file
            "-acodec", "libmp3lame",  # Use MP3 codec
            "-q:a", "2",  # Quality setting (lower is better)
            output_file
        ]
        subprocess.run(command, check=True)

    except Exception as ee:
        print(f"❌ Error merging files: {ee}")
        sys.exit(1)

    update_download_log("MP3 downloaded", COLORS.green)
    delete_temp_files()

    reset_config_entry_box_colors()


def merge_video_audio(video_id: str, publish_date: str, vid_res: str, year: str, restricted: bool) -> None:
    video_file, audio_file = find_media_files(".")

    if not video_file or not audio_file:
        print("❌ No MP4 or M4A files found in the current directory.")
        return

    restricted_path = "/"
    if restricted:
        restricted_path = "/restricted/"

    create_directories(restricted, year)
    output_file = (ytchannel_path.get() + str(year) + restricted_path + publish_date + " - " + vid_res
                   + " - " + clean_string_regex(os.path.splitext(video_file)[0]) + " - " + video_id + ".mp4")

    try:
        update_download_log("Merging to MP4...", COLORS.gray)
        abort_button.grid_remove()
        command = [
            "ffmpeg", "-loglevel", "quiet", "-stats", "-i", video_file, "-i", audio_file,
            "-c:v", "copy", "-c:a", "aac", output_file
        ]
        subprocess.run(command, check=True)

        if restricted:
            update_download_log("Restricted Video downloaded", COLORS.green)
        else:
            update_download_log("Video downloaded", COLORS.green)

        abort_button.grid_remove()
        enable_buttons()
        update_video_counts(
            str(count_files(output_dir + "/" + clean_string_regex(total_channel_name).rstrip(), ".mp4")) +
            " / " + str(total_channel_videos) + " Videos downloaded")

        reset_config_entry_box_colors()

        delete_temp_files()

    except Exception as ee:
        print(f"❌ Error merging files: {ee}")
        sys.exit(1)


def convert_m4a_to_opus_and_merge(video_id: str, publish_date: str, vid_res: str, year: str,
                                  restricted: bool) -> None:
    video_file, audio_file = find_media_files(".")
    update_download_log("Convert M4A audio to Opus format (WebM compatible)...", COLORS.gray)
    command = [
        "ffmpeg", "-loglevel", "quiet", "-stats", "-i", audio_file, "-c:a", "libopus", "audio.opus"
    ]
    subprocess.run(command, check=True)
    merge_webm_opus(video_id, publish_date, vid_res, year, restricted)


def merge_webm_opus(video_id: str, publish_date: str, vid_res: str, year: str, restricted: bool) -> None:
    video_file, audio_file = find_media_files(".")
    output_file = "tmp/" + video_file
    update_download_log("Merging WebM video with Opus audio...", COLORS.gray)
    command = [
        "ffmpeg", "-loglevel", "quiet", "-stats", "-i", video_file, "-i", "audio.opus",
        "-c:v", "copy", "-c:a", "copy", output_file
    ]
    subprocess.run(command, check=True)

    delete_temp_files()
    os.remove("audio.opus")
    restricted_string = "/"
    if restricted:
        restricted_string = "/restricted/"

    path = (ytchannel_path.get() + str(year) + restricted_string + publish_date + " - " + vid_res + " - "
            + clean_string_regex(os.path.splitext(video_file)[0]) + " - " + video_id + ".mp4")
    convert_webm_to_mp4(output_file, path, year, restricted)


def convert_webm_to_mp4(input_file: str, output_file: str, year: str, restricted: bool) -> None:
    create_directories(restricted, year)
    update_download_log("Converting WebM to MP4... (this may take a while)", COLORS.gray)
    abort_button.grid_remove()
    command = [
        "ffmpeg", "-loglevel", "quiet", "-stats", "-i", input_file,
        "-c:v", "libx264", "-preset", "fast", "-crf", "23",  # H.264 video encoding
        "-c:a", "aac", "-b:a", "128k",  # AAC audio encoding
        "-movflags", "+faststart",  # Optimize MP4 for streaming
        output_file
    ]
    subprocess.run(command, check=True)
    os.remove(input_file)
    if restricted:
        update_download_log("Restricted Video downloaded", COLORS.green)
    else:
        update_download_log("Video downloaded", COLORS.green)

    abort_button.grid_remove()
    enable_buttons()
    update_video_counts(
        str(count_files(output_dir + "/" + clean_string_regex(total_channel_name).rstrip(), ".mp4")) +
        " / " + str(total_channel_videos) + " Videos downloaded")

    reset_config_entry_box_colors()



# Load config
config = load_config("config.json")
output_dir = ""
youtube_url = ""
youtube_watch_url = ""
web_client = ""
try:
    # Access settings
    output_dir = config["output_directory"]
    youtube_url = config["youtube_url"]
    youtube_watch_url = config["youtube_watch_url"]
    web_client = config["web_client"]

except Exception as e:
    print("An error occurred, incomplete config file:", str(e))
    CcConfig.cc_check_and_update_json_config("config.json", AppConfig.REQUIRED_APP_CONFIG)

delete_temp_files()

# System settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.iconbitmap(AppConfig.icon_path)
# app.geometry(app_resolution + "+0+0")
app.geometry(f"{AppConfig.win_width}x{AppConfig.win_height}" + "+0+0")
update_app_title()
app.configure(bg_color=COLORS.black)
app.protocol("WM_DELETE_WINDOW", on_closing)
app.grid_columnconfigure(0, minsize=250)
app.grid_columnconfigure(1, minsize=300)
app.grid_columnconfigure(2, minsize=480)
app.grid_columnconfigure(3, minsize=250)

# Add UI elements
logo = customtkinter.CTkImage(light_image=Image.open(AppConfig.logo_path), size=(87, 58)) # 180x120
logo_label = customtkinter.CTkLabel(app, text="", image=logo)
logo_label.grid(row=0, column=0, rowspan=2, padx=padding_x, pady=padding_y, sticky="nw")

# log_label = customtkinter.CTkLabel(app, text=log_default, width=235 , fg_color=COLORS.log_bg, text_color=COLORS.violet)
# log_label.grid(row=0, column=1, padx=padding_x, pady=padding_y, sticky="w")

channel_dropdown = customtkinter.CTkComboBox(app, values=read_channel_txt_lines("channels.txt"), width=350)
channel_dropdown.grid(row=0, column=2, padx=padding_x, pady=padding_y, sticky="w")

title = customtkinter.CTkLabel(app, text="YouTube Channel, Video-, or Playlist URL:", text_color=COLORS.gray)
title.grid(row=1, column=1, padx=padding_x, pady=padding_y, sticky="se")

if len(sys.argv) > 1 and not youtube_url in str(sys.argv[1]):
    url_var = tkinter.StringVar(value=sys.argv[1])
else:
    url_var = tkinter.StringVar(value="")

link = customtkinter.CTkEntry(app, width=entry_width, textvariable=url_var)
link.grid(row=1, column=2, padx=padding_x, pady=padding_y, sticky="sw")

get_information_button = customtkinter.CTkButton(app, text="Get Information", command=get_information)
get_information_button.grid(row=1, column=3, padx=padding_x, pady=padding_y, sticky="sw")

# separator1 = customtkinter.CTkFrame(app, height=2, fg_color=COLORS.separator)
# separator1.grid(row=2, column=0, columnspan=4, sticky="ew", padx=padding_x, pady=padding_y)

channel_frame = customtkinter.CTkFrame(app, fg_color=COLORS.frame_bg)

channel_frame.grid_columnconfigure(0, minsize=250)
channel_frame.grid_columnconfigure(1, minsize=300)
channel_frame.grid_columnconfigure(2, minsize=480)
channel_frame.grid_columnconfigure(3, minsize=250)

separator2 = customtkinter.CTkFrame(channel_frame, height=2, fg_color=COLORS.separator)
# separator3 = customtkinter.CTkFrame(app, height=2, fg_color=COLORS.separator)

video_info_channel = customtkinter.CTkLabel(channel_frame, text="", font=("Arial", 16, "bold"))
video_info_channel_url = customtkinter.CTkLabel(channel_frame, text="", text_color=COLORS.gray)
video_info_channel_button = customtkinter.CTkButton(channel_frame, text="Add to channels.txt")
after_adding_to_channels_txt_label = customtkinter.CTkLabel(channel_frame, text="", text_color=COLORS.gray)

ytchannel_path_label = customtkinter.CTkLabel(channel_frame, text="Save Path:", text_color=COLORS.gray)
ytchannel_path = customtkinter.CTkEntry(channel_frame, width=entry_width)

ytchannel_video_count = customtkinter.CTkLabel(channel_frame, text="")

channel_config_label = customtkinter.CTkLabel(channel_frame, text="")
create_channel_config_button = customtkinter.CTkButton(channel_frame)

channel_thumbnail_label = customtkinter.CTkLabel(channel_frame, text="")

configuration_resolution = customtkinter.CTkComboBox(channel_frame)
configuration_min_duration = customtkinter.CTkEntry(channel_frame)
configuration_min_views = customtkinter.CTkEntry(channel_frame)
configuration_year_subs = customtkinter.CTkCheckBox(channel_frame)
configuration_max_duration = customtkinter.CTkEntry(channel_frame)
configuration_skip_restricted = customtkinter.CTkCheckBox(channel_frame)
configuration_only_restricted = customtkinter.CTkCheckBox(channel_frame)
configuration_min_year = customtkinter.CTkEntry(channel_frame)
configuration_max_year = customtkinter.CTkEntry(channel_frame)
configuration_filter_words = customtkinter.CTkTextbox(channel_frame)
configuration_excludes = customtkinter.CTkTextbox(channel_frame)
configuration_includes = customtkinter.CTkTextbox(channel_frame)

audio_button = customtkinter.CTkButton(channel_frame, text="Audio (mp3)")
video_button = customtkinter.CTkButton(channel_frame, text="Video (mp4)")

skip_videos_value = tkinter.StringVar(value="")
skip_videos = customtkinter.CTkEntry(channel_frame, textvariable=skip_videos_value)

yt_video_id = customtkinter.CTkEntry(app)
yt_video_title_label = customtkinter.CTkLabel(app, text="")
yt_video_views_label = customtkinter.CTkLabel(app, text="")
yt_video_date_label = customtkinter.CTkLabel(app, text="")
yt_video_length_label = customtkinter.CTkLabel(app, text="")
yt_video_title = customtkinter.CTkLabel(app, text="")
yt_video_views = customtkinter.CTkLabel(app, text="")
yt_video_date = customtkinter.CTkLabel(app, text="")
yt_video_length = customtkinter.CTkLabel(app, text="")
video_thumbnail_label = customtkinter.CTkLabel(app, text="")

abort_button = customtkinter.CTkButton(app, text="Abort")

video_resolution_label = customtkinter.CTkLabel(app, text="")
video_resolution = customtkinter.CTkComboBox(app)
avail_resolutions = customtkinter.CTkLabel(app, text="")

download_button = customtkinter.CTkButton(app, text="")

progress_percent = customtkinter.CTkLabel(app, text="")
progress_bar = customtkinter.CTkProgressBar(app, width=entry_width)

download_log_label = customtkinter.CTkLabel(app, text="")

if len(sys.argv) > 1 and youtube_url in str(sys.argv[1]):
    channel_dropdown.set(sys.argv[1])

app.mainloop()
