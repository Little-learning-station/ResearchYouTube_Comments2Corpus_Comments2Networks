from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
from csv import writer
import json

# Put your API key inside the quotation marks
youtube = build('youtube', 'v3', developerKey='')

#Full System (Multi‑Video + Full Reply Pagination + Titles + Separate & Combined Exports)
def get_video_title(video_id):
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )
    response = request.execute()
    items = response.get("items", [])
    if not items:
        return "Unknown Title"
    return items[0]["snippet"]["title"]
  
def fetch_all_replies(parent_comment_id, video_id, video_title):
    replies = []
    next_page_token = None

    while True:
        request = youtube.comments().list(
            part="snippet",
            parentId=parent_comment_id,
            maxResults=100,
            pageToken=next_page_token
        )
        response = request.execute()

        for reply in response.get("items", []):
            snip = reply["snippet"]
            replies.append({
                "video_id": video_id,
                "video_title": video_title,
                "commentId": reply["id"],
                "reply_count": None,
                "likeCount": snip.get("likeCount"),
                "date": snip.get("publishedAt"),
                "author_display_name": snip.get("authorDisplayName"),
                "author_channel_id": snip.get("authorChannelId", {}).get("value"),
                "author_channel_url": snip.get("authorChannelUrl"),
                "comment": snip.get("textDisplay"),
                "is_reply": True,
                "reply_to_comment_id": parent_comment_id,
                "reply_to_author_channel_id": snip.get("authorChannelId", {}).get("value"),
                "reply_to_author_name": snip.get("authorDisplayName")
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return replies

def fetch_comments_with_replies(video_id):
    video_title = get_video_title(video_id)
    all_data = []
    next_page_token = None

    while True:
        request = youtube.commentThreads().list(
            part="id,snippet",
            videoId=video_id,
            maxResults=100,
            moderationStatus="published",
            order="time",
            textFormat="plainText",
            pageToken=next_page_token
        )
        response = request.execute()

        for item in response.get("items", []):
            top = item["snippet"]["topLevelComment"]
            snip = top["snippet"]

            parent_id = top["id"]
            parent_author = snip.get("authorDisplayName")
            parent_channel_id = snip.get("authorChannelId", {}).get("value")

            # Top-level comment
            all_data.append({
                "video_id": video_id,
                "video_title": video_title,
                "commentId": parent_id,
                "reply_count": item["snippet"].get("totalReplyCount"),
                "likeCount": snip.get("likeCount"),
                "date": snip.get("publishedAt"),
                "author_display_name": parent_author,
                "author_channel_id": parent_channel_id,
                "author_channel_url": snip.get("authorChannelUrl"),
                "comment": snip.get("textDisplay"),
                "is_reply": False,
                "reply_to_comment_id": None,
                "reply_to_author_channel_id": None,
                "reply_to_author_name": None
            })

            # Fetch ALL replies (full pagination)
            if item["snippet"].get("totalReplyCount", 0) > 0:
                replies = fetch_all_replies(parent_id, video_id, video_title)
                all_data.extend(replies)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return all_data

def fetch_multiple_videos(video_ids):
    all_results = []
    for vid in video_ids:
        print(f"Fetching: {vid}")
        data = fetch_comments_with_replies(vid)
        all_results.extend(data)
    return all_results

def print_comments(data):
    for entry in data:
        if not entry["is_reply"]:
            print(f"\nVideo: {entry['video_title']} ({entry['video_id']})")
            print(f"{entry['author_display_name']} ({entry['author_channel_id']})")
            print(f"Comment ID: {entry['commentId']}")
            print(f"Likes: {entry['likeCount']}")
            print(f"Date: {entry['date']}")
            print(f"Comment: {entry['comment']}")

            for reply in data:
                if reply["is_reply"] and reply["reply_to_comment_id"] == entry["commentId"]:
                    print(f"  ↳ Reply from {reply['author_display_name']} ({reply['author_channel_id']})")
                    print(f"     {reply['comment']}")

import csv
from collections import defaultdict

def export_csv_separate_and_combined(data):
    grouped = defaultdict(list)

    for row in data:
        grouped[row["video_id"]].append(row)

    # Separate files
    for vid, rows in grouped.items():
        title = rows[0]["video_title"].replace("/", "_")
        filename = f"{title}_{vid}.csv"
        write_csv(rows, filename)

    # Combined file
    write_csv(data, "ALL_VIDEOS_COMMENTS.csv")


def write_csv(rows, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "video_id","video_title","commentId","is_reply",
            "reply_to_comment_id","reply_to_author_channel_id",
            "reply_to_author_name","reply_count","likeCount",
            "date","author_display_name","author_channel_id",
            "author_channel_url","comment"
        ])
        for r in rows:
            writer.writerow([
                r["video_id"], r["video_title"], r["commentId"], r["is_reply"],
                r["reply_to_comment_id"], r["reply_to_author_channel_id"],
                r["reply_to_author_name"], r["reply_count"], r["likeCount"],
                r["date"], r["author_display_name"], r["author_channel_id"],
                r["author_channel_url"], r["comment"]
            ])

# Replace the ID1, ID2... IDn with your  desired IDs inside the quotation marks.

video_list = [ "ID1","ID2"," ", " "," ",""]
data = fetch_multiple_videos(video_list)
export_csv_separate_and_combined(data)
