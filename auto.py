import re
import os
import subprocess
import json
import random



chanels=[]
uploaded=[]
turn=int


def get_shorts_urls_from_channel(channel_url, output_file):
    # Run yt-dlp with filters to get only Shorts (videos under 60 seconds)
    result = subprocess.run(
        ["yt-dlp", "-J", "--flat-playlist", "--match-filter", "duration < 80", channel_url], 
        capture_output=True, text=True
    )
    
    if result.returncode == 0:
        metadata = json.loads(result.stdout)
        
        # Save metadata to a JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
    else:
        print(f"Error fetching {channel_url}: {result.stderr}")


##############


def populate():
    with open("source_urls",'r') as f:
            for line in f:
                chanel_name=re.search( r"@(\w+)/?",line).group(1)   
                if not chanel_name:
                    continue
                if os.path.exists(f"vedios/{chanel_name}"):
                    # chanels.append(chanel_name)
                    continue
                else:
                    os.mkdir(f"vedios/{chanel_name}")
                    get_shorts_urls_from_channel(line,f"vedios/{chanel_name}/{chanel_name}.json")
                    chanels.append(chanel_name)


def choose():
    global turn
    turn = turn % len(chanels)
    chanel=chanels[turn]
    with open(f"vedios/{chanel}/{chanel}.json") as f:
        jsn_shorts=json.loads(f.read())
        if jsn_shorts["entries"]:
            rand = random.randint(0,int(len(jsn_shorts["entries"])/4))
            turn = turn+1
            return jsn_shorts["entries"][rand]




def main():
    global chanels
    global turn
    with open("persist_data.json", "r") as f:
        persist_data = json.loads(f.read())
        chanels = persist_data["chanels"]
        turn = persist_data["turn"]
        uploaded = persist_data["uploaded"]

    populate()
    video = choose()
    while video.get("id") in uploaded:
        video = choose

    # video = json.loads(
    #     """{
    #         "title": "Peter has big thighs🤣🦵 || #familyguy #shorts",
    #         "view_count": 1100000,
    #         "thumbnails": [
    #             {
    #                 "url": "https://i.ytimg.com/vi/br4rCxTFRMU/oar2.jpg?sqp=-oaymwEdCJUDENAFSFWQAgHyq4qpAwwIARUAAIhCcAHAAQY=&rs=AOn4CLCMgeJLGTfKusqRnKerQ_AgTsAVUQ",
    #                 "height": 720,
    #                 "width": 405
    #             }
    #         ],
    #         "ie_key": "Youtube",
    #         "id": "br4rCxTFRMU",
    #         "_type": "url",
    #         "url": "https://www.youtube.com/shorts/br4rCxTFRMU",
    #         "__x_forwarded_for_ip": null
    #     }"""
    #     )
   


    ##downloaad te video
    subprocess.run(
        ["yt-dlp","-o",f"vedios/__downs__/{video.get("id")}",video.get("url"),"--merge-output-format", "webm",]
    )
    # uploading 
    description="""

 Family Guy Season 20 Episode 7 - Family Guy Full Episode NoCuts #1080p 
#familyguy #petergriffin #briangriffin  
 #funny #familyguy #shorts
#Luck #Angelo #IQ #Principal #April #Fools #prank #Animation #Kidsproblem

    """
    #tags
    tags=["#shorts", "#familyguy","#funny", "#simpsons"]
    if video["title"]:
        for tag in tags:
            if not tag in video.get("title"):
                video["title"] = video["title"]+" "+tag
          
           
    subprocess.run(
        ["python3", "upload.py" , 
        f"--file=vedios/__downs__/{video.get("id")}.webm",
        "--keywords= Family Guy \n petergriffin cartoon "
        f"--description={description}",
        "--category=22",
        f"--title={video.get("title")}",
        "--privacyStatus=public"]
    )





    uploaded.append(video.get("id"))


    persist_data["chanels"]=chanels
    persist_data["turn"]=turn
    persist_data["uploaded"]=uploaded
    with open("persist_data.json", "w") as f:
        json.dump(persist_data,f)



if __name__=="__main__":
    main()