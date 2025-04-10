import customtkinter
import os
import subprocess
import threading
from pytubefix import Channel
from PIL import Image
from functions import (AppConfig, COLORS, CcConfig, Tooltip, load_config, find_file_by_string, count_files, format_time,
                       get_free_space, clean_string_regex, string_to_list, destroy_elements)


app_title = "YTDL.channels"
row_height = 23
padding_x = 5
padding_y = 1
padding_y_factor = 2

elements_to_destroy = []


def checkbox_latest_clicked():
    if var_latest.get():
        var_filter_on.set(False)


def checkbox_filter_on_clicked():
    if var_filter_on.get():
        var_latest.set(False)


def update_app_title():
    app.title(app_title + AppConfig.VERSION + " - Free disk space: " + get_free_space(output_dir))


def read_channel_txt_lines(filename: str) -> list[str]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            rc_lines = [line.strip() for line in file if not line.lstrip().startswith("#")]
        return rc_lines
    except FileNotFoundError:
        print("❌ Error: File not found.")
        return []


def format_view_count(number: int) -> str:
    if number >= 1_000_000_000:  # Billions
        return f"{number / 1_000_000_000:.1f}B"
    elif number >= 1_000_000:  # Millions
        return f"{number / 1_000_000:.1f}M"
    elif number >= 1_000:  # Thousands
        return f"{number / 1_000:.0f}K"
    else:
        return str(number)


def update_log(text: str) -> None:
    log_label.configure(text=text)
    log_label.update()


def remove_button_and_checkboxes():
    start_button.grid_remove()
    c_filters_on_in_channels_list.grid_remove()
    c_show_latest_video_date.grid_remove()
    log_label.grid(row=0, column=1, columnspan=18, padx=padding_x, pady=padding_y, sticky="w")


def add_button_and_checkboxes():
    start_button.grid(row=0, column=0, padx=padding_x, pady=padding_y + 3, sticky="e")
    c_show_latest_video_date.grid(row=0, column=2, columnspan=6, padx=padding_x, pady=padding_y, sticky="w")
    c_filters_on_in_channels_list.grid(row=0, column=2, columnspan=6, padx=padding_x, pady=padding_y, sticky="e")
    log_label.grid(row=0, column=9, columnspan=8, padx=padding_x, pady=padding_y, sticky="w")


def list_channels():
    update_log("Listing channels from channels.txt...")
    update_app_title()
    destroy_elements(elements_to_destroy)
    remove_button_and_checkboxes()
    threading.Thread(target=list_channels_work, daemon=True).start()


def list_channels_work():
    row_factor = 1
    separator1.grid(row=row_factor, column=0, columnspan=18, sticky="ew", padx=0, pady=padding_y * padding_y_factor)

    for i, channel in enumerate(channel_lines, start=1):
        update_log("Scanning channel... " + channel.replace(youtube_url, "")[1:])
        channel_object = Channel(channel)

        # Channel Name
        button_channel_name = customtkinter.CTkButton(app, text=channel.replace(youtube_url, "")[1:], height=row_height,
                                                      width=180, fg_color=COLORS.log_bg,
                                                      command=lambda i=channel: open_script(i))
        button_channel_name.grid(row=i + row_factor, column=0, padx=padding_x, pady=padding_y, sticky="w")
        elements_to_destroy.append(button_channel_name)

        if os.path.exists(output_dir + "/" + clean_string_regex(
                channel_object.channel_name).rstrip() + AppConfig.CHANNEL_CONFIG_PATH):
            channel_config = load_config(output_dir + "/" + clean_string_regex(
                channel_object.channel_name).rstrip() + AppConfig.CHANNEL_CONFIG_PATH)

            # Resolution
            label_config_resolution = customtkinter.CTkLabel(app, text="max", height=row_height, text_color=COLORS.gray)
            label_config_resolution.grid(row=i + row_factor, column=1, padx=padding_x, pady=padding_y, sticky="nswe")
            elements_to_destroy.append(label_config_resolution)
            if channel_config["c_max_resolution"] != "":
                label_config_resolution.configure(text=channel_config["c_max_resolution"], text_color=COLORS.orange)

            # Min duration
            label_config_min_duration = customtkinter.CTkLabel(app, text="0m", height=row_height,
                                                               text_color=COLORS.gray)
            label_config_min_duration.grid(row=i + row_factor, column=2, padx=padding_x, pady=padding_y, sticky="e")
            elements_to_destroy.append(label_config_min_duration)
            if int(channel_config["c_min_duration_in_minutes"]) != 0:
                label_config_min_duration.configure(text=str(channel_config["c_min_duration_in_minutes"]) + "m",
                                                    text_color=COLORS.yellow)

            # Max duration
            label_config_max_duration = customtkinter.CTkLabel(app, text="0m", height=row_height,
                                                               text_color=COLORS.gray)
            label_config_max_duration.grid(row=i + row_factor, column=3, padx=padding_x, pady=padding_y, sticky="e")
            elements_to_destroy.append(label_config_max_duration)
            if int(channel_config["c_max_duration_in_minutes"]) != 0:
                label_config_max_duration.configure(text=str(channel_config["c_max_duration_in_minutes"]) + "m",
                                                    text_color=COLORS.yellow)

            # Skip restricted
            label_config_skip_restricted = customtkinter.CTkLabel(app, text="S", height=row_height,
                                                                  text_color=COLORS.gray)
            label_config_skip_restricted.grid(row=i + row_factor, column=4, padx=padding_x, pady=padding_y,
                                              sticky="nswe")
            elements_to_destroy.append(label_config_skip_restricted)
            if channel_config["c_skip_restricted"] == "y":
                label_config_skip_restricted.configure(text_color=COLORS.red)

            # Restricted
            label_config_only_restricted = customtkinter.CTkLabel(app, text="R", height=row_height,
                                                                  text_color=COLORS.gray)
            if channel_config["c_skip_restricted"] != "y":
                label_config_only_restricted.grid(row=i + row_factor, column=5, padx=padding_x, pady=padding_y,
                                                  sticky="nswe")
                elements_to_destroy.append(label_config_only_restricted)
            if channel_config["c_only_restricted"] == "y":
                label_config_only_restricted.configure(text_color=COLORS.dark_red)

            # Min views
            label_config_min_views = customtkinter.CTkLabel(app, text="0", height=row_height,
                                                            text_color=COLORS.gray)
            label_config_min_views.grid(row=i + row_factor, column=6, padx=padding_x, pady=padding_y, sticky="e")
            elements_to_destroy.append(label_config_min_views)
            if int(channel_config["c_minimum_views"]) != 0:
                label_config_min_views.configure(text=format_view_count(int(channel_config["c_minimum_views"])),
                                                 text_color=COLORS.yellow)

            # Year subs
            label_config_year_subs = customtkinter.CTkLabel(app, text="Y", height=row_height, text_color=COLORS.gray)
            label_config_year_subs.grid(row=i + row_factor, column=7, padx=padding_x, pady=padding_y, sticky="nswe")
            elements_to_destroy.append(label_config_year_subs)
            if channel_config["c_year_subfolders"] == "y":
                label_config_year_subs.configure(text_color=COLORS.green)

            # Min year
            label_config_min_year = customtkinter.CTkLabel(app, text="-", height=row_height, text_color=COLORS.gray)
            label_config_min_year.grid(row=i + row_factor, column=8, padx=padding_x, pady=padding_y, sticky="e")
            elements_to_destroy.append(label_config_min_year)
            if int(channel_config["c_minimum_year"]) != 0:
                label_config_min_year.configure(text=str(channel_config["c_minimum_year"]),
                                                text_color=COLORS.dark_green)

            # Max year
            label_config_max_year = customtkinter.CTkLabel(app, text="-", height=row_height, text_color=COLORS.gray)
            label_config_max_year.grid(row=i + row_factor, column=9, padx=padding_x, pady=padding_y, sticky="e")
            elements_to_destroy.append(label_config_max_year)
            if int(channel_config["c_maximum_year"]) != 0:
                label_config_max_year.configure(text=str(channel_config["c_maximum_year"]),
                                                text_color=COLORS.dark_green)

            # excludes
            label_config_excludes = customtkinter.CTkLabel(app, text="excl", height=row_height, text_color=COLORS.gray)
            label_config_excludes.grid(row=i + row_factor, column=10, padx=padding_x, pady=padding_y, sticky="nswe")
            elements_to_destroy.append(label_config_excludes)
            if channel_config["c_exclude_video_ids"] != "":
                label_config_excludes.configure(text_color=COLORS.pink)
                Tooltip(label_config_excludes, channel_config["c_exclude_video_ids"])

            # includes
            label_config_includes = customtkinter.CTkLabel(app, text="incl", height=row_height, text_color=COLORS.gray)
            label_config_includes.grid(row=i + row_factor, column=11, padx=padding_x, pady=padding_y, sticky="nswe")
            elements_to_destroy.append(label_config_includes)
            if channel_config["c_include_video_ids"] != "":
                label_config_includes.configure(text_color=COLORS.cyan)
                Tooltip(label_config_includes, channel_config["c_include_video_ids"])

            # Filter words
            label_config_filter_words = customtkinter.CTkLabel(app, text="", height=row_height)
            if channel_config["c_filter_words"] != "":
                word_length = 17
                label_config_filter_words.configure(text=channel_config["c_filter_words"][:word_length] +
                                                         "..." if len(
                    channel_config["c_filter_words"]) > word_length else channel_config["c_filter_words"],
                                                    text_color=COLORS.blue)
                if len(channel_config["c_filter_words"]) > word_length:
                    Tooltip(label_config_filter_words, channel_config["c_filter_words"])
            label_config_filter_words.grid(row=i + row_factor, column=12, padx=padding_x, pady=padding_y, sticky="w")
            elements_to_destroy.append(label_config_filter_words)

        update_log("Fetching channel... " + channel.replace(youtube_url, "")[1:])

        label_video_count = customtkinter.CTkLabel(app, text="", height=row_height, text_color=COLORS.gray)
        state_show_latest_video_checkbox = False
        counter_color = COLORS.gray
        if c_show_latest_video_date.get() == 1 or c_filters_on_in_channels_list.get() == 1:
            state_show_latest_video_checkbox = True
            channel_video_count = str(len(channel_object.video_urls))
            count_files_from_channel_dir = count_files(output_dir + "/" +
                                                       clean_string_regex(channel_object.channel_name).rstrip(),
                                                       [".mp4", ".mp3"])
            if count_files_from_channel_dir >= int(channel_video_count):
                counter_color = COLORS.dark_green
            label_video_count.configure(text=str(count_files_from_channel_dir) + " / " + channel_video_count)
        else:
            # Video count
            label_video_count.configure(text=str(count_files(output_dir + "/" +
                                                             clean_string_regex(channel_object.channel_name).rstrip(),
                                                             [".mp4", ".mp3"])) + " / ...")

        label_video_count.grid(row=i + row_factor, column=13, padx=padding_x, pady=padding_y, sticky="e")
        elements_to_destroy.append(label_video_count)

        channel_last_updated = channel_object.last_updated

        state_filters_on_checkbox = False
        if c_filters_on_in_channels_list.get() == 1:
            state_filters_on_checkbox = True

        got_it = False

        ch_config_filter_words = ""
        ch_config_min_duration = 0
        ch_config_max_duration = 9999
        ch_config_min_year = 2000
        ch_config_max_year = 2099
        ch_config_restricted = {True, False}
        ch_config_min_views = 0
        ch_config_exclude_list = string_to_list("")

        if os.path.exists(
                output_dir + "/" + clean_string_regex(
                    channel_object.channel_name).rstrip() + AppConfig.CHANNEL_CONFIG_PATH):
            ch_config = load_config(
                output_dir + "/" + clean_string_regex(
                    channel_object.channel_name).rstrip() + AppConfig.CHANNEL_CONFIG_PATH)

            ch_config_filter_words = ch_config["c_filter_words"]
            if str(ch_config["c_min_duration_in_minutes"]).strip():
                ch_config_min_duration = int(ch_config["c_min_duration_in_minutes"])
            if str(ch_config["c_max_duration_in_minutes"]).strip() and int(ch_config["c_max_duration_in_minutes"] > 0):
                ch_config_max_duration = int(ch_config["c_max_duration_in_minutes"])
            if str(ch_config["c_minimum_year"]).strip():
                ch_config_min_year = int(ch_config["c_minimum_year"])
            if str(ch_config["c_maximum_year"]).strip() and int(ch_config["c_maximum_year"] > 0):
                ch_config_max_year = int(ch_config["c_maximum_year"])
            if str(ch_config["c_minimum_views"]).strip():
                ch_config_min_views = int(ch_config["c_minimum_views"])
            if ch_config["c_only_restricted"] == "y":
                ch_config_restricted.remove(False)
            if ch_config["c_skip_restricted"] == "y":
                ch_config_restricted.remove(True)
            ch_config_exclude_list = string_to_list(ch_config["c_exclude_video_ids"])

        update_log("Filtering videos...")
        if state_filters_on_checkbox:
            counter = 0
            color_else = COLORS.gray
            color_video_id = COLORS.gray
            color_video_date = COLORS.gray
            latest_video_title_text = ""
            latest_date = ""
            # yt_video_thumbnail = ""
            size = channel_object.video_urls
            for video_iter in channel_object.videos:
                counter += 1
                youtube_video_object = video_iter
                youtube_vo_video_id = youtube_video_object.video_id
                youtube_vo_title = youtube_video_object.title
                youtube_vo_vid_info = youtube_video_object.vid_info
                youtube_vo_length = youtube_video_object.length
                youtube_vo_views = youtube_video_object.views
                youtube_vo_age_restricted = youtube_video_object.age_restricted
                youtube_vo_publish_date = youtube_video_object.publish_date

                update_log("Find match:  " + str(counter) + " / " + str(len(size)) + "     |     " +
                           str(youtube_vo_publish_date.strftime(AppConfig.DATE_FORMAT_DISPLAY)) + "     |     " +
                                                    format_time(youtube_vo_length) + "     |     " +
                                        ("R" if youtube_vo_age_restricted else "_") + "     |     " + youtube_vo_title)
                # update_download_log("Find match:  " + str(v_counter) + "/" + str(len(video_watch_urls)) + "  |  " +
                #                     ("R" if video.age_restricted else "_") + "  |  " +
                #                     str(video.publish_date.strftime(AppConfig.date_format_display)) + "  |  " +
                #                     format_time(video.length) + "  |  " +
                #                     v_title, (COLORS.violet if do_not_download == 1 else COLORS.green))

                if (youtube_vo_vid_info.get('playabilityStatus', {}).get('status') != 'UNPLAYABLE' and
                        youtube_vo_vid_info.get('playabilityStatus', {}).get(
                            'status') != 'LIVE_STREAM_OFFLINE' and
                        any(word.lower() in youtube_vo_title.lower() for word in
                            string_to_list(ch_config_filter_words))
                        and youtube_vo_video_id not in ch_config_exclude_list
                        and ch_config_min_duration * 60 <= int(youtube_vo_length) <= ch_config_max_duration * 60
                        and ch_config_min_year <= int(str(youtube_vo_publish_date.strftime("%Y"))) <= ch_config_max_year
                        and youtube_vo_views >= ch_config_min_views
                        and youtube_vo_age_restricted in ch_config_restricted):

                    # yt_video_thumbnail = load_image_from_url(youtube_video_object.thumbnail_url, size=(32, 18))

                    latest_video_title_text = youtube_vo_title
                    latest_date_math = youtube_vo_publish_date.strftime(AppConfig.DATE_FORMAT_MATH)
                    latest_date = youtube_vo_publish_date.strftime(AppConfig.DATE_FORMAT_DISPLAY)
                    latest_video_id_text = youtube_vo_video_id

                    if youtube_vo_age_restricted:
                        color_video_id = COLORS.dark_red

                    got_it = find_file_by_string(output_dir + "/" +
                                                 clean_string_regex(channel_object.channel_name).rstrip(),
                                                 latest_date_math, "", False)
                    if not got_it:
                        color_video_date = COLORS.red
                        if color_video_id != COLORS.dark_red:
                            color_video_id = COLORS.white
                        color_else = COLORS.white
                    break
            if got_it:
                if color_video_id != COLORS.dark_red:
                    color_video_id = COLORS.gray
                color_else = COLORS.gray

            button_channel_name.configure(text_color=color_else)

            if color_video_date == COLORS.red:
                button_latest_video_date = customtkinter.CTkButton(app, text=latest_date, height=row_height, width=70,
                                                                   fg_color=COLORS.log_bg,
                                                                   text_color=COLORS.red,
                                                                   command=lambda i=latest_video_id_text: open_script(
                                                                       i))
                button_latest_video_date.grid(row=i + row_factor, column=14, padx=padding_x, pady=padding_y,
                                              sticky="nswe")
                elements_to_destroy.append(button_latest_video_date)
            else:
                label_latest_video_date = customtkinter.CTkLabel(app, text=latest_date, text_color=color_video_date,
                                                                 height=row_height)
                label_latest_video_date.grid(row=i + row_factor, column=14, padx=padding_x, pady=padding_y,
                                             sticky="nswe")
                elements_to_destroy.append(label_latest_video_date)

            # video_thumbnail_label = customtkinter.CTkLabel(app, text="")
            # video_thumbnail_label.configure(image=yt_video_thumbnail, text="")
            # video_thumbnail_label.grid(row=i + row_factor, column=15, padx=int(padding_x / 3), pady=0, sticky="nswe")
            # elements_to_destroy.append(video_thumbnail_label)

            label_latest_video_id = customtkinter.CTkLabel(app, text=latest_video_id_text, text_color=color_video_id,
                                                           height=row_height)
            label_latest_video_id.grid(row=i + row_factor, column=16, padx=padding_x, pady=padding_y, sticky="w")
            elements_to_destroy.append(label_latest_video_id)

            title_width = 27
            label_latest_video_title = customtkinter.CTkLabel(app,
                                                              text=latest_video_title_text[:title_width] + "..." if len(
                                                                  latest_video_title_text) > title_width else latest_video_title_text,
                                                              text_color=color_else, height=row_height)
            label_latest_video_title.grid(row=i + row_factor, column=17, padx=padding_x, pady=padding_y, sticky="w")
            elements_to_destroy.append(label_latest_video_title)
            # if len(str(latest_video_title_text)) > title_width:
            #     Tooltip(label_latest_video_title, latest_video_title_text)

            label_video_count.configure(text_color=color_else)
            if counter_color != COLORS.gray:
                label_video_count.configure(text_color=counter_color)

        if state_show_latest_video_checkbox and not state_filters_on_checkbox:
            # Latest updated
            label_last_updated = customtkinter.CTkLabel(app, text=channel_last_updated, width=160, height=row_height,
                                                        text_color=COLORS.gray)
            elements_to_destroy.append(label_last_updated)

            label_last_updated.grid(row=i + row_factor, column=0, padx=padding_x, pady=padding_y, sticky="w")
            elements_to_destroy.append(label_last_updated)

        row_factor += 1
        separator_label = customtkinter.CTkFrame(app, height=2, fg_color=COLORS.separator)
        separator_label.grid(row=i + row_factor, column=0, columnspan=18, sticky="ew", padx=0, pady=padding_y)
        elements_to_destroy.append(separator_label)

        update_log("")
    update_app_title()

    add_button_and_checkboxes()


def open_script(video_id):
    args = video_id
    subprocess.Popen(["venv/scripts/python", "gui.py", args])



output_dir = ""
youtube_url = ""
youtube_watch_url = ""
web_client = ""

# Load config
config = load_config("config.json")
try:
    # Access settings
    output_dir = config["output_directory"]
    youtube_url = config["youtube_url"]
    youtube_watch_url = config["youtube_watch_url"]
    web_client = config["web_client"]

except Exception as e:
    print("An error occurred, incomplete config file:", str(e))
    CcConfig.cc_check_and_update_json_config("config.json", AppConfig.REQUIRED_APP_CONFIG)

# System settings
customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")

# App frame
app = customtkinter.CTk()
app.iconbitmap(AppConfig.ICON_PATH)
# Get screen width & height
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

# Calculate x, y for bottom-right position
x_offset = screen_width - AppConfig.WIN_WIDTH - 10  # Align to right
y_offset = screen_height - AppConfig.WIN_HEIGHT - 72  # Align to bottom

app.geometry(f"{AppConfig.WIN_WIDTH}x{AppConfig.WIN_HEIGHT}+{x_offset}+{y_offset}")
update_app_title()
app.configure(bg_color=COLORS.black)
# app.protocol("WM_DELETE_WINDOW", on_closing)

header_frame = customtkinter.CTkFrame(app, fg_color=COLORS.frame_bg)
header_frame.grid(row=0, column=0, columnspan=18, padx=0, pady=padding_y, sticky="nw")

logo = customtkinter.CTkImage(light_image=Image.open(AppConfig.LOGO_PATH), size=(60, 40)) # 180x120
logo_label = customtkinter.CTkLabel(header_frame, text="", image=logo)
logo_label.grid(row=0, column=0, padx=padding_x, pady=padding_y, sticky="nw")

channel_lines = read_channel_txt_lines("channels.txt")

start_button = customtkinter.CTkButton(header_frame, text="Start", command=list_channels, width=95)
start_button.grid(row=0, column=0, padx=padding_x, pady=padding_y + 3, sticky="e")

var_latest = customtkinter.BooleanVar()
var_filter_on = customtkinter.BooleanVar()

c_show_latest_video_date = customtkinter.CTkCheckBox(header_frame, text="Latest Video", variable=var_latest, command=checkbox_latest_clicked)
c_show_latest_video_date.grid(row=0, column=2, columnspan=6, padx=padding_x, pady=padding_y, sticky="w")

c_filters_on_in_channels_list = customtkinter.CTkCheckBox(header_frame, text="Filters On", variable=var_filter_on, command=checkbox_filter_on_clicked)
c_filters_on_in_channels_list.grid(row=0, column=2, columnspan=6, padx=padding_x, pady=padding_y, sticky="e")

log_label = customtkinter.CTkLabel(header_frame, text="", text_color=COLORS.violet, anchor="w")
log_label.grid(row=0, column=9, columnspan=8, padx=padding_x, pady=padding_y, sticky="w")

separator1 = customtkinter.CTkFrame(app, height=2, fg_color=COLORS.separator)

header_frame.grid_columnconfigure(0, minsize=210)    # Channel Name
header_frame.grid_columnconfigure(1, minsize=50)     # Resolution
header_frame.grid_columnconfigure(2, minsize=50)     # Min duration
header_frame.grid_columnconfigure(3, minsize=50)     # Max duration
header_frame.grid_columnconfigure(4, minsize=25)     # Skip restricted
header_frame.grid_columnconfigure(5, minsize=25)     # Restricted
header_frame.grid_columnconfigure(6, minsize=60)     # Min views
header_frame.grid_columnconfigure(7, minsize=25)     # Year subs
header_frame.grid_columnconfigure(8, minsize=50)     # Min year
header_frame.grid_columnconfigure(9, minsize=50)     # Max year
header_frame.grid_columnconfigure(10, minsize=50)     # excludes
header_frame.grid_columnconfigure(11, minsize=50)     # includes
header_frame.grid_columnconfigure(12, minsize=90)    # Filter words
header_frame.grid_columnconfigure(13, minsize=80)     # Video count
header_frame.grid_columnconfigure(14, minsize=100)    # Latest updated 160 / Latest video date
header_frame.grid_columnconfigure(15, minsize=0)    # Thumbnail 40
header_frame.grid_columnconfigure(16, minsize=110)    # Latest video ID
header_frame.grid_columnconfigure(17, minsize=210)    # Latest video title 164

app.grid_columnconfigure(0, minsize=210)    # Channel Name
app.grid_columnconfigure(1, minsize=50)     # Resolution
app.grid_columnconfigure(2, minsize=50)     # Min duration
app.grid_columnconfigure(3, minsize=50)     # Max duration
app.grid_columnconfigure(4, minsize=25)     # Skip restricted
app.grid_columnconfigure(5, minsize=25)     # Restricted
app.grid_columnconfigure(6, minsize=60)     # Min views
app.grid_columnconfigure(7, minsize=25)     # Year subs
app.grid_columnconfigure(8, minsize=50)     # Min year
app.grid_columnconfigure(9, minsize=50)     # Max year
app.grid_columnconfigure(10, minsize=50)     # excludes
app.grid_columnconfigure(11, minsize=50)     # includes
app.grid_columnconfigure(12, minsize=90)    # Filter words
app.grid_columnconfigure(13, minsize=80)     # Video count
app.grid_columnconfigure(14, minsize=100)    # Latest updated 160 / Latest video date
app.grid_columnconfigure(15, minsize=0)    # Thumbnail 40
app.grid_columnconfigure(16, minsize=110)    # Latest video ID
app.grid_columnconfigure(17, minsize=200)    # Latest video title 164

app.mainloop()
