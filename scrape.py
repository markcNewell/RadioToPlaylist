from selenium import webdriver
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from spotipy import Spotify
from spotipy.scope import every
from autologin import prompt_for_user_token
from spotipy.util import request_client_token




#https://github.com/felix-hilden/spotipy
client_id = 'e92a76c6a42342c1a5cc7b0894a10845'
client_secret = '49d1415093d34253aa4b7f697a4ca36c'
redirect_uri = 'https://www.google.com'

user_token = prompt_for_user_token(
    client_id,
    client_secret,
    redirect_uri,
    scope=every
)

app_token = request_client_token(client_id, client_secret, redirect_uri)







def diff(x,date):
	"""
	Function to find the eucleadian distance between dates
	"""

	h = int(date.strftime("%H")) * 60
	m = int(date.strftime("%M"))

	x_h = int(x.split(":")[0]) * 60
	x_m = int(x.split(":")[1])

	return ((h-x_h + m-x_m)**2)**0.5







while True:
	#Get time to record from
	in_from = input("Enter the date you wanted to view e.g. 1/5/2005  17:33: ")



	#Get time to record to
	try:
		in_for_h = int(input("How long for (hrs): "))
		in_for_m = int(input("How long for (mins): "))
	except:
		print("Input integer not string")
		break;



	#Try convert the inputted time to a datetime object
	try:
		usr_date_from = datetime.strptime(in_from, '%d/%m/%Y %H:%M')
	except:
		print("Wrong date format used")
		break;


	#Calculate dates to use
	usr_date_till = usr_date_from + timedelta(hours=in_for_h,minutes=in_for_m)
	today = datetime.now()
	cut_off = today - timedelta(days=6)



	#If date inputted in the correct range (last 7 days)
	if (usr_date_from > cut_off):

		#Get page number
		page = int(today.strftime("%d")) - int(usr_date_from.strftime("%d"))



		#Get website data
		driver = webdriver.Firefox()
		driver.get("https://onlineradiobox.com/uk/bbcradio1/playlist/" + str(page))
		soup = BeautifulSoup(driver.page_source)

		
		
		#Get all times on the page
		times = []
		songs = []
		all_times = soup.findAll('span', attrs={'class':'time--schedule'})



		#Add the text of these times and their songs to lists
		for a in range(len(all_times)):
			p = all_times[a].parent
			songs.append(p.findNext('td').text)
			times.append(all_times[a].text)



		#Find the closest start and end times to use inputted
		start = min(times, key=lambda x:diff(x,usr_date_from))
		end = min(times, key=lambda x:diff(x,usr_date_till))



		#Find the index's of those times
		start_i = times.index(start)
		end_i = times.index(end)



		#Get the list of songs in the right order
		songs = songs[start_i:end_i:-1]



		#Close the webscraper
		driver.quit()



		#Setup spotify connection
		spotify = Spotify(app_token)
		spotify.token = user_token



		#Create playlist
		name = "Radio1 - " + usr_date_from.strftime("%H:%M") + " - " + usr_date_till.strftime("%H:%M")
		usr_id = spotify.current_user().id
		playlist = spotify.playlist_create(usr_id, name)



		#For each song name make a request to find the correct id
		ids = []
		for song in songs:
			song = song.split(" - ")[1]
			results = spotify.search(song, types=('track',), limit=1)
			ids.append(results[0].items[0].id)




		#Add all the tracks to the playlist you created
		spotify.playlist_tracks_add(playlist.id,ids)
		












