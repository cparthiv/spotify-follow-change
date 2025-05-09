# Spotify Follower Change Tracker

## Program flow

1. Authenticates you through the Spotify API
2. Looks up your follower count
3. If it exists, checks the stored follower count (last time you ran the program) and compares it to the current count
4. Posts to a Discord webhook to notify you about the change
5. Saves current following count to storage so it can be compared next time

## Tutorial

Copy `.env.example` to `.env` and put your credentials in.

To get the client ID and client secret come from the [Spotify Developer Portal](https://developer.spotify.com/). When creating your app, add the callback URL in as a redirect. You can keep it the same as from the example env. We aren't building any sort of web app, so it doesn't matter because the url is only used internally.

Generate a discord webhook link so that you can get discord notifications.

Run the script!

## My setup

After running this for the first time, the program doesn't need to authenticate you _usually_ unless access is revoked. On one of my servers, I set up a [Cron job](https://en.wikipedia.org/wiki/Cron) to run this every hour, so that I get notified timely when someone unfollows or follows me. Most people using this will probably be on Windows, so just use task scheduler! Create a batch file if necessary.

## Pictures
![image](https://github.com/user-attachments/assets/2609a91f-3b24-492b-af99-6ad376b8ca75)
![image](https://github.com/user-attachments/assets/8b368803-169f-4327-9c44-1fab6f49b988)
