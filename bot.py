import requests
import telebot
import json
import urllib.request
import shutil

secret = "BOT_TOKEN"

bot = telebot.TeleBot(secret)

class Downlaod:
	def __init__(self,message):
		self.message = message
		head, mid, tail = self.message.text.partition("?")
		self.url = head + "?__a=1"
		self.req()

	def req(self):
		try:
			self.response = requests.get(self.url)
			data = json.loads(self.response.text)
		except:
			bot.send_message(self.message.chat.id, "Invalid url!")
			return False

		self.execute(data)

	def execute(self, data):
		arr = []
		temp = {}
			
		if "graphql" in data:
			head_of_data = data["graphql"]["shortcode_media"]
		else:
			bot.send_message(self.message.chat.id, "Something went wrong!")
			return False

		if "edge_sidecar_to_children" in head_of_data.keys():

			for edge in head_of_data["edge_sidecar_to_children"]["edges"]:

				if edge["node"]["is_video"]:
					temp["display_url"] = edge["node"]["display_url"]
					temp["video_url"] = edge["node"]["video_url"]
					temp["is_video"] = True
				else:
					temp["display_url"] = edge["node"]["display_url"]
					temp["is_video"] = False

				arr.append(temp)
				temp = {}
		else:
			if data["graphql"]["shortcode_media"]["is_video"]:
				temp["display_url"] = head_of_data["display_url"]
				temp["video_url"] = head_of_data["video_url"]
				temp["is_video"] = True
			else:
				temp["display_url"] = head_of_data["display_url"]
				temp["is_video"] = False
			arr.append(temp)

		shortcode = head_of_data["shortcode"]
		
		for i,img in enumerate(arr):
			if img["is_video"]:
				source_url = img["video_url"]
				bot.send_video(self.message.chat.id, source_url)

			else:
				source_url = img["display_url"]
				bot.send_photo(self.message.chat.id, source_url)


def main():
	@bot.message_handler(func=lambda message: True)
	def send_back(message):
		download = Downlaod(message)

if __name__ == "__main__":
	main()
	bot.polling()