import praw
import re
import json
import os
import requests

BOT_USERNAME = "/u/soccer"
SUBREDDIT = "news"

def lambda_handler(event, context):
    # Create the Reddit instance and log in
    reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                         client_secret = os.environ['CLIENT_SECRET'],
                         user_agent = os.environ['USER_AGENT'],
                         username = os.environ['USERNAME'],
                         password = os.environ['PASSWORD'])

    handled_request = find_requests(reddit)

    return {
        "statusCode": 200,
        "handled_request": handled_request,
    }


def find_requests(reddit):
    subreddit = reddit.subreddit(SUBREDDIT)
    for submission in subreddit.new(limit=10):
        print(submission.title)
        submission.comments.replace_more(limit=0)
        for comment in submission.comments:
            if re.search(BOT_USERNAME, comment.body, re.IGNORECASE) and not already_replied(comment):
                handle_request(comment)
                return True
    return False


def handle_request(comment):
    index = comment.body.index(BOT_USERNAME) + len(BOT_USERNAME)
    query = comment.body[index:]
    headlines = fetch_headlines(query)
    response = build_response(query, headlines)
    print("replying to: " + comment.body)
    print("response: " + response)
    comment.reply(response)


def build_response(query, headlines):
    response = "Here are some relevant recent headlines for: " + query + "  "
    headline_count = 0
    for headline in headlines:
        headline_count += 1
        response += "[" + headline["name"] + "](" + headline["url"] + ")\n  "
        if headline_count >= 5:
            return response
    return response


def already_replied(comment):
    top_level_replies = comment.replies
    top_level_replies.replace_more(limit=None)
    for reply in top_level_replies:
        if reply.author.name.lower() == "headline_checker_bot":
            print("already replied to comment", comment.body)
            return True
    return False


def fetch_headlines(query):
    print("fetching headlines for: " + query)
    search_url = "https://api.cognitive.microsoft.com/bing/v7.0/news/search"
    headers = {"Ocp-Apim-Subscription-Key" : os.environ['SUBSCRIPTION_KEY']}
    params = {"q": query, "textDecorations": False, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    articles = search_results["value"]
    print("found articles: ")
    print(articles)
    return articles
