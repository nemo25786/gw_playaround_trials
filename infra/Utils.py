import string

def format_filename(s):
    s = s.split("[")[0]
    valid_chars = "-_()%s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')  # I don't like spaces in filenames.

    return filename

def str2bool(v):
  return v.lower() in ("yes", "true", "t", "1")
