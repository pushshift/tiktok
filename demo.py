import api
import json

# Examples on how to use Tiktok API

# Initiate tiktok API object
tiktok = api.tiktok()

# Get all comments for a video ID (Generator function)
video_id = 6751947290048515333
comments = tiktok.fetch_all_comments(video_id=video_id)

for comment in comments:
    # Do something with each comment
    json_data = json.dumps(comment, indent=4)
    print(json_data)

# Fetch Trending list
trending = tiktok.fetch_all_items()

for item in trending:
    # Do something with each item
    json_data = json.dumps(item, indent=4)
    print(json_data)
