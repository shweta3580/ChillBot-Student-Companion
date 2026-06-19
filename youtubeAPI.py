from googleapiclient.discovery import build
from textblob import TextBlob

# YouTube API Key
api_key = "AIzaSyAiRuAyZ8cnMDWU1ekRrSYt9u5EqUiTQYc"
youtube = build("youtube", "v3", developerKey=api_key)

def get_sentiment(text):
    """Analyze sentiment of user input."""
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity  # Ranges from -1 to +1

    if sentiment_score < 0:  
        return "negative"
    else:
        return "positive"

def get_youtube_recommendations(mood):
    """Fetch YouTube videos based on mood."""
    search_query = "happy songs"  # Default

    if mood == "tired":
        search_query = "relaxing music"
    elif mood == "bored":
        search_query = "funny videos"
    elif mood == "sad":
        search_query = "motivational speech"

    # YouTube API Request
    request = youtube.search().list(
        q=search_query,
        part="snippet",
        maxResults=3  # Get 3 recommendations
    )
    response = request.execute()

    video_links = []
    for item in response["items"]:
        if item["id"]["kind"] == "youtube#video":
            video_id = item["id"]["videoId"]
            video_links.append(f"https://www.youtube.com/watch?v={video_id}")

    return video_links

# Example Usage
user_input = input("How do you feel? ")  # User types their mood
sentiment = get_sentiment(user_input)

if sentiment == "negative":
    print("You seem down. Here are some YouTube videos for you:")
    recommendations = get_youtube_recommendations(user_input)
    for link in recommendations:
        print(link)
else:
    print("Glad you're feeling good! 😊")
