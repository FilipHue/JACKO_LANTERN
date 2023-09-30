import urllib.request
import re


def find_url(name):
    """
    Finds and returns a URL based on the provided name.

    If the provided name is a URL, it will simply return it

    Args:
        name:   :class:`str`: The name or URL to search for or use as-is.

    Returns:
        str: The generated or provided URL.

    """
    if "https" not in name:
        words_list = name.split()
        full_name = ''
        for i in range(0, len(words_list)):
            full_name = full_name + words_list[i] + '+'
        full_name = full_name[:-1]
        name = full_name
        html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(name))
        video_ids = re.findall(r'watch\?v=(\S{11})', html.read().decode())
        url = 'https://www.youtube.com/watch?v=' + str(video_ids[0])
    else:
        url = name
    return url
