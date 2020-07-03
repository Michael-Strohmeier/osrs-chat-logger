import pandas as pd
import cv2
import pytesseract
import time
import os
from grabscreen import grab_screen

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

STRETCHED = False

BAD_TIME_CHARS = ["+", "-", "[", ":"]
BAD_NAME_CHARS = ["", "@"]

if not STRETCHED:
    GAME_REGION = (10, 400, 500, 484)
else:
    GAME_REGION = (10, 400, 500, 484)


def remove_bad_chars(timestamp, name, message):
    clean_time = ''.join(i for i in timestamp if not i in BAD_TIME_CHARS)
    clean_name = ''.join(i for i in name if not i in BAD_NAME_CHARS)

    if clean_time.isdigit():
        return [clean_time, clean_name, message]

    return None


def parse_screen(current_chat_log_window):
    window = current_chat_log_window

    unparsed_chat_text = pytesseract.image_to_string(window, config='--psm 6')
    unparsed_chat_text = unparsed_chat_text.split("\n")

    parsed_chat = []
    for line in unparsed_chat_text:
        try:
            timestamp, name_and_message = line.split("]")
            name, message = name_and_message.split(":", 1)

            clean_log = remove_bad_chars(timestamp, name, message)
            if clean_log is not None and clean_log[0] is not None:
                parsed_chat.append(clean_log)
        except:
            pass

    return parsed_chat


def update_chat_log(df: pd.DataFrame, parsed_chat_box: list):
    if not df.empty:
        # if chat log DataFrame NOT empty

        for row in parsed_chat_box:
            time, name, message = row

            if not ((df["time"] == time) & (df["name"] == name)).any():
                df = df.append(pd.DataFrame(parsed_chat_box, columns=["time", "name", "message"]))
        return df
    else:
        # if chat log DataFrame empty
        return pd.DataFrame(parsed_chat_box, columns=["time", "name", "message"])

def record_chat():
    start_time = str(time.time()).replace(".", "")

    chat_log_df = pd.DataFrame(columns=["time", "name", "message"])
    while True:
        screen = grab_screen(region=GAME_REGION)
        parsed_chat_box = parse_screen(screen)

        chat_log_df = update_chat_log(chat_log_df, parsed_chat_box)
        chat_log_df.to_csv('{}.csv'.format(start_time))

        time.sleep(3)

        os.system('CLS')

        cv2.imshow('window2', cv2.cvtColor(screen, cv2.COLOR_BGR2RGB))

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    record_chat()
