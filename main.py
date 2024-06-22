import json
import requests
import re

from discord_webhook import DiscordWebhook

#Enter Webhook Url Here
WebhookUrl = ''

def checkforvideos():
  with open("youtubedata.json", "r") as f:
    data=json.load(f)
  
  print("Now Checking!")

  #checking for all the channels in youtubedata.json file
  for youtube_channel in data:
    print(f"Now Checking For {data[youtube_channel]['channel_name']}")
    #getting youtube channel's url
    channel = f"https://www.youtube.com/channel/{youtube_channel}"

    #getting html of the /videos page
    html = requests.get(channel+"/videos").text

    #getting the latest video's url
    #put this line in try and except block cause it can give error some times if no video is uploaded on the channel
    try:
      latest_video_url = "https://www.youtube.com/watch?v=" + re.search('(?<="videoId":").*?(?=")', html).group()
    except:
      pass

    #checking if url in youtubedata.json file is not equals to latest_video_url
    if not str(data[youtube_channel]["latest_video_url"]) == latest_video_url:

      #changing the latest_video_url
      data[str(youtube_channel)]['latest_video_url'] = latest_video_url

      #dumping the data
      with open("youtubedata.json", "w") as f:
        json.dump(data, f)


      #sending the msg
      msg = f"@everyone {data[str(youtube_channel)]['channel_name']} Just Uploaded A Video Or He is Live Go Check It Out: {latest_video_url}"
      webhook = DiscordWebhook(url=WebhookUrl, content=msg)

      webhook.execute()
      checkforvideos()

checkforvideos()
