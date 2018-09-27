import praw
import re
import json
import os
import requests

BOT_USERNAME = "/u/headline_checker_bot"
SUBREDDIT = "news"

def lambda_handler(event, context):
    print("initializing reddit instance")
    reddit = praw.Reddit(client_id=os.environ['CLIENT_ID'],
                         client_secret = os.environ['CLIENT_SECRET'],
                         user_agent = os.environ['USER_AGENT'],
                         username = os.environ['USERNAME'],
                         password = os.environ['PASSWORD'])

    print("success")
    handled_request = find_mentions(reddit)
    print("terminating lambda session")
    return {
        "statusCode": 200,
        "handled_request": handled_request,
    }


def find_mentions(reddit):
    for mention_comment in reddit.inbox.mentions(limit=5):
        if not already_replied(mention_comment):
            print("Found new mention, from user " + mention_comment.author)
            handle_request(mention_comment)
            return True
    print("No new mentions found")
    return False


def handle_request(comment):
    index = comment.body.index(BOT_USERNAME) + len(BOT_USERNAME)
    query = comment.body[index:]
    headlines = fetch_headlines(query)
    response = build_response(query, headlines)
    comment.reply(response)
    print("replied")


def build_response(query, headlines):
    response = "Here are some relevant recent headlines for: " + query + "\n\n"
    headline_count = 0
    for headline in headlines:
        headline_count += 1
        response += "[" + headline["name"] + "](" + headline["url"] + ")\n\n"
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
    print("success")
    return articles
