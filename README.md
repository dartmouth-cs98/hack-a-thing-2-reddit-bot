# /u/headliner_checker_bot

Chris Bertasi - September 2018

### Description
I built a Reddit bot that automatically links relevant recent news articles from a given query whenever the bot is pinged. I used Reddit APIs (PRAW), Microsoft Azure's Bing News API, and AWS Lambda.

### What we learned
I'd never actually learned or coded in Python before (never took CS 1), so I learned a good chunk of Python syntax for this project. 
I also learned how to use the reddit API to build bots to automatically interact with Reddit. 
I'd be interested in using AWS Lambda before but had never actually tried, so I signed up for an AWS account and used it for hosting the bot. 
Finally, I signed up for an Azure account to use their Bing News API, which I had also never used before.

### What didn't work
The Reddit API was fairly frustrating to work with. PRAW uses lazy objects, which means information isnt retrieved until it is specifically requested.
In addition, comment chains don't load all the comments, and when iterating through comments you may need to make multiple new API calls to load more comments.