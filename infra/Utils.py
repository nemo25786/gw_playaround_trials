import string
import json
from logging import Logger
def format_filename(s:str) -> str:
    s = s.split("[")[0]
    valid_chars = "-_()%s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.

    return filename

def str2bool(v) -> bool:
  return v.lower() in ("yes", "true", "t", "1")


def read_from_json_config(get_log: Logger, config_file_location: str) -> dict:
    try:
        with open(config_file_location, 'r') as config_file:
            config_data = json.load(config_file)
    except Exception as e:
        get_log.error(f"unable to find config file with msg: {str(e)}")
        raise e

    return config_data




