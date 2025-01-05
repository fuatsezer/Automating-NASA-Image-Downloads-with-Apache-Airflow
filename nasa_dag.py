import json
import pathlib
import airflow
import requests
import requests.exceptions as request_exceptions
from datetime import date,datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.decorators import task
from datetime import datetime, timedelta
import re
import requests
from urllib.parse import urlparse, parse_qs


dag_owner = "airflow"


def get_youtube_thumbnail(video_url):
    """
    Given a YouTube video URL, fetch and save the thumbnail image.

    :param video_url: The URL of the YouTube video.
    :param save_path: The path to save the thumbnail image (default: "thumbnail.jpg").
    """
    # Extract video ID from the URL
    video_id = extract_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    # Construct the thumbnail URL
    thumbnail_url = f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

    # Download the thumbnail
    response = requests.get(thumbnail_url, stream=True)
    if response.status_code == 200:
        return response.content
    else:
        print("Failed to fetch thumbnail. The video might not have a high-resolution thumbnail.")
def extract_video_id(video_url):
    """
    Extract the video ID from a YouTube URL, including embed URLs.

    :param video_url: The URL of the YouTube video.
    :return: The video ID as a string, or None if extraction fails.
    """
    # Parse the URL and query parameters
    parsed_url = urlparse(video_url)
    if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
        # For standard YouTube URLs
        return parsed_url.path.split("/embed/")[-1]
    elif parsed_url.hostname in ("youtu.be",):
        # For shortened YouTube URLs
        return parsed_url.path.lstrip("/")
    elif parsed_url.hostname in ("www.youtube.com", "youtube.com") and "/embed/" in parsed_url.path:
        # For embed URLs
        return parsed_url.path.split("/embed/")[-1]
    return None

def _get_pictures():
    api_key = "6im4bXKxXrPgvcmuq64F1sXErIUQMgKcLALAMQQp"
    url = f"http://api.nasa.gov/planetary/apod?api_key={api_key}"
    response = requests.get(url).json()
    today_image = response["url"]
    response_content = get_youtube_thumbnail(today_image)
    with open(f"todays_image_{date.today()}.png", "wb") as f:
        f.write(response_content)

default_args = {"owner": dag_owner,
                "retries": 2,
                "retry_delay": timedelta(minutes=5)}

with DAG(dag_id="nasa_dag",
         default_args= default_args,
         description= "download and notify ",
         start_date = datetime(2025, 1, 1),
         schedule_interval = '@daily',
         catchup=False,
         tags=["None"]):
    get_pictures = PythonOperator(
        task_id = "get_pictures",
        python_callable=_get_pictures
    )
    notify = BashOperator(
        task_id="notify",
        bash_command='echo f"Image for today has been added!"',
    )

    get_pictures >> notify