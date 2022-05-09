from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
blackList=[]
list=[]
#for video_id in ["rBY2Dzej03A"]:
#	try:
#		ctent=YouTubeTranscriptApi.get_transcript(video_id)
#		list.append({"content":ctent,"id":video_id})
#	except TranscriptsDisabled as t:
#		print("data not found "+t)
Afailed=0
Asuccess=0
def think(videolist):
	global Afailed
	global Asuccess
	blackList=loadBlackList()
	print("::::"+str(blackList))
	for video_id in videolist:
		if video_id in blackList:
			pass
		else:
			try:
				list.append({"content":YouTubeTranscriptApi.get_transcript(video_id),"id":video_id})
				#Asuccess=Asuccess+1
			except (TranscriptsDisabled, NoTranscriptFound):
				blackList.append(video_id)
				#Afailed=Afailed+1
				saveBlackList(blackList)
				print("data not found "+video_id)
	links=[]
	for listItem in list:
		#print("checking in "+listItem["id"])
		success=False
		for text in listItem["content"]:
#			print(text["text"])
			#print(text['duration'])
			#print(text['start'])
			if "discord" in text["text"]:
				link="https://www.youtube.com/watch?v="+listItem["id"]+"&t="+str(text['start'])
				print(link)
				links.append(link)
				print(text["text"])
				print(text['start']/60)
				success=True

		if success:
			Asuccess=Asuccess+1
		else:
			Afailed=Afailed+1
	print(links)
	print(Afailed)
	print(Asuccess)
	#saveBlinkslackList()pickle.dump(blackList,open("blacklist.pickle","wb"))
# -*- coding: utf-8 -*-

# Sample Python code for youtube.videos.list
# See insthttps://developers.google.com/explorer-help/code-samples#pythonructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import glob,pickle
scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
def loadBlackList():
	f=glob.glob('blacklist.pickle')
	print("data"+str(len(f)))
	if len(f)==0:
		pickle.dump([],open("blacklist.pickle","wb"))
	return pickle.load(open("blacklist.pickle","rb"))
def saveBlackList(blackListe):
	pickle.dump(blackListe,open("blacklist.pickle","wb"))
def loadCredentials(flow):
	f=glob.glob('cred.pickle')
	c="" #flow.run_console()c=flow.run_console()
	print(f)
	blackList=loadBlackList()
	print(blackList)
	if len(f)==0:
		print("saving")
		c=flow.run_console()
		pickle.dump(c,open("cred.pickle","wb"))
		print("done saving")
	else:
		c=pickle.load(open("cred.pickle","rb"))
	return c
def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets_file.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    #input("name")
    credentials = loadCredentials(flow)
    #credentials = flow.run_console()


    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request = youtube.videos().list(
        part="snippet,contentDetails,statistics",
        myRating="like",
	maxResults=50
    )
    response = request.execute()

    print(response.keys())
    print(response["items"][0].keys())
    print(response["items"][0]["id"])
    videos=[]
    for item in response["items"]:
        videos.append(item["id"])
    print(len(videos))
    think(videos)
if __name__ == "__main__":
    main()
