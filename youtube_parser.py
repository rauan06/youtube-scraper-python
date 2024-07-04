import requests
import re

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0'
}

def extract_video_info(url):
    """
    Extracts video title and view count from a Youtube webpage using regular expressions.

    Args:
        str url: The URL of the Youtube video webpage.

    Returns:
        A dictionary containing extracted information or None if data not found.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        html_content = response.content.decode("utf-8")

        title_match = re.search(
            r'"title":{"runs":\[\{"text":"([^"]+)"', 
            html_content
        )
        if title_match:
            video_title = title_match.group(1).strip()
        else:
            video_title = None

        view_count_match = re.search(
            r'"views":{"simpleText":"(.*?) views',
            html_content
        )
        if view_count_match:
            view_count = view_count_match.group(1).strip()
        else:
            view_count = None

        # Return extracted information
        return {"title": video_title, "view_count": view_count}

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


def extract_search_results(query):
    """
    Extracts video titles and links from a Youtube search results page using regular expressions.

    Args:
        str query: The search query for Youtube.

    Returns:
        A dictionary containing video titles and links.
    """
    try:
        link = "https://www.youtube.com/results"
        response = requests.get(link, params={"search_query": query}, headers=HEADERS)
        response.raise_for_status()
        html_content = response.content.decode("utf-8")

        titles_match = re.findall(
            r"<title>(.*?) - YouTube</title>", html_content, re.DOTALL
        )

        video_data = {}
        if titles_match:
            for i, title_match in enumerate(titles_match):
                video_data[i + 1] = title_match.group(1).strip()

        return video_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# Example usage
print(extract_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ"))



video_info = extract_search_results("rauan")
print(video_info)