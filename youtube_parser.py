import requests
import re

HEADERS = {}

def extract_video_info(url):
    """
    Extracts video title and view count (might be unreliable) from a Youtube webpage using regular expressions.

    Args:
        url: The URL of the Youtube video webpage.

    Returns:
        A dictionary containing extracted information or None if data not found.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise exception for unsuccessful requests
        html_content = response.content.decode("utf-8")
        # print(html_content)
        # Extract video title (might be unreliable)
        title_match = re.search(
            r'"title":{"runs":\[\{"text":"([^"]+)"', 
            html_content
        )
        if title_match:
            video_title = title_match.group(1).strip()
        else:
            video_title = None

        # Extract view count (might be unreliable)
        view_count_match = re.search(
            r',"views":{"simpleText":"(.*?) рет',
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
        query: The search query for Youtube.

    Returns:
        A dictionary containing video titles and links or None if data not found.
    """
    try:
        link = "https://www.youtube.com/results"
        response = requests.get(link, params={"search_query": query})
        response.raise_for_status()  # Raise exception for unsuccessful requests
        html_content = response.content.decode("utf-8")
        # print(html_content)
        # Extract video titles (might be unreliable)
        titles_match = re.findall(
            r"<title>(.*?) - YouTube</title>", html_content, re.DOTALL
        )

        # Create a dictionary to store results
        video_data = {}
        if titles_match:
            for i, title_match in enumerate(titles_match):
                video_data[i + 1] = title_match.group(1).strip()  # Use index as key

        # Return video data dictionary
        return video_data

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None


# Example usage
video_info = extract_video_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
if video_info:
    print(f"Video Title: {video_info['title']}")
    print(f"View Count: {video_info['view_count']}")
else:
    print("Failed to extract video information.")


video_info = extract_search_results("rauan")
print(video_info)