import requests
import json

r = requests.get('http://shanxiunicom.livehot.wasu.tv/weekhot_cs2/interfaces/liveChannel.do')

tv = json.loads(r.text)


for channel in tv['data']['items']:
    print(channel['channelName'] + ',' + channel['playUrl'])