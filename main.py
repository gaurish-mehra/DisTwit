import discord
import tweepy

consumer_key = "YOUR_CONSUMER_KEY"
consumer_secret = "YOUR_CONSUMER_SECRET"
access_token = "YOUR_ACCESS_TOKEN"
access_token_secret = "YOUR_ACCESS_TOKEN_SECRET"

client = discord.Client()


def get_tweets(username):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    tweets = api.user_timeline(screen_name=username, count=1)

    return tweets


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!tweet '):
        username = message.content[7:]
        tweets = get_tweets(username)

        for tweet in tweets:
            await message.channel.send(tweet.text)

    elif message.content.startswith('!notify '):
        username = message.content[8:]

        class TweetStreamListener(tweepy.StreamListener):
            def on_status(self, status):
                if status.user.screen_name == username:
                    message.channel.send(status.text)
                    stream.disconnect()

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream_listener = TweetStreamListener()
        stream = tweepy.Stream(auth=auth, listener=stream_listener)
        stream.filter(follow=[api.get_user(screen_name=username).id_str])

client.run('YOUR_DISCORD_BOT_TOKEN')
