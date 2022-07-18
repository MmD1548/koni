from requests import get
from re import findall
import os
import glob
from rubika.client import Bot
import requests
from rubika.tools import Tools
from rubika.encryption import encryption
from gtts import gTTS
from mutagen.mp3 import MP3
import time
import random
import urllib
import io

bot = Bot("Raberto", auth="qfmqglhyhplvmxjrktcnjjpgwjavnphx")
target = "g0Bn49Q02cc042018ab0c35f74856ad2"
bot.sendMessage(target, 'را‌برتو فعال شد.✅')
# created By HiBye & ShayanHeidari(Snipe4Kill)(TG GAMES)(libs for Bahman Ahmadi)

def hasAds(msg):
	links = ["http://","https://",".ir",".com",".org",".net",".me"]
	for i in links:
		if i in msg:
			return True
			
def hasInsult(msg):
	swData = [False,None]
	for i in open("dontReadMe.txt").read().split("\n"):
		if i in msg:
			swData = [True, i]
			break
		else: continue
	return swData
	
# static variable
answered, sleeped, retries = [], False, {}

alerts, blacklist = [] , []

def alert(guid,user,link=False):
	alerts.append(guid)
	coun = int(alerts.count(guid))

	haslink = ""
	if link : haslink = "گذاشتن لینک در گروه ممنوع میباشد .\n\n"

	if coun == 1:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (1/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")
	elif coun == 2:
		bot.sendMessage(target, "💢 اخطار [ @"+user+" ] \n"+haslink+" شما (2/3) اخطار دریافت کرده اید .\n\nپس از دریافت 3 اخطار از گروه حذف خواهید شد !\nجهت اطلاع از قوانین کلمه (قوانین) را ارسال کنید .")

	elif coun == 3:
		blacklist.append(guid)
		bot.sendMessage(target, "🚫 کاربر [ @"+user+" ] \n (3/3) اخطار دریافت کرد ، بنابراین اکنون اخراج میشود .")
		bot.banGroupMember(target, guid)
		

while True:
	# time.sleep(15)
	try:
		admins = [i["member_guid"] for i in bot.getGroupAdmins(target)["data"]["in_chat_members"]]
		min_id = bot.getGroupInfo(target)["data"]["chat"]["last_message_id"]

		while True:
			try:
				messages = bot.getMessages(target,min_id)
				break
			except:
				continue

		for msg in messages:
			try:
				if msg["type"]=="Text" and not msg.get("message_id") in answered:
					if not sleeped:
						if hasAds(msg.get("text")) and not msg.get("author_object_guid") in admins :
							guid = msg.get("author_object_guid")
							user = bot.getUserInfo(guid)["data"]["user"]["username"]
							bot.deleteMessages(target, [msg.get("message_id")])
							alert(guid,user,True)

						elif msg.get("text") == "!stop" or msg.get("text") == "/stop" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "✅ ربات اکنون خاموش است", message_id=msg.get("message_id"))
							except:
								print("err off bot")
							
						elif msg.get("text") == "!restart" or msg.get("text") == "/restart" and msg.get("author_object_guid") in admins :
							try:
								sleeped = True
								bot.sendMessage(target, "در حال راه اندازی مجدد...", message_id=msg.get("message_id"))
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت مجددا راه اندازی شد!", message_id=msg.get("message_id"))
							except:
								print("err Restart bot")
										
						elif msg.get("text").startswith("حذف") and msg.get("author_object_guid") in admins :
							try:
								number = int(msg.get("text").split(" ")[1])
								answered.reverse()
								bot.deleteMessages(target, answered[0:number])

								bot.sendMessage(target, "✅ "+ str(number) +" پیام اخیر با موفقیت حذف شد", message_id=msg.get("message_id"))
								answered.reverse()

							except IndexError:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "✅ پیام با موفقیت حذف شد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))

						elif msg["text"].startswith("بن") or msg["text"].startswith("/ban") :
							try:
								guid = bot.getInfoByUsername(msg["text"].replace("بن","").replace("/ban ","")[1:])["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									bot.banGroupMember(target, guid)
									# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", msg["message_id"])
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
										
							except:
								try:
									guid = bot.getMessagesInfo(target, [msg["reply_to_message_id"]])[0]["author_object_guid"]
									if not guid in admins :
										bot.banGroupMember(target, guid)
										# bot.sendMessage(target, "✅ کاربر با موفقیت از گروه اخراج شد", msg["message_id"])
									else :
										bot.sendMessage(target, "❌ کاربر ادمین میباشد", msg["message_id"])
								except:
										bot.sendMessage(target, "❌ خطا در اجرای دستور", msg["message_id"])

						elif msg.get("text").startswith("افزودن") or msg.get("text").startswith("!add") :
							try:
								guid = bot.getInfoByUsername(msg.get("text").split(" ")[1][1:])["data"]["chat"]["object_guid"]
								if guid in blacklist:
									if msg.get("author_object_guid") in admins:
										alerts.remove(guid)
										alerts.remove(guid)
										alerts.remove(guid)
										blacklist.remove(guid)

										bot.invite(target, [guid])
									else:
										bot.sendMessage(target, "❌ کاربر محدود میباشد", message_id=msg.get("message_id"))
								else:
									bot.invite(target, [guid])
									# bot.sendMessage(target, "✅ کاربر اکنون عضو گروه است", message_id=msg.get("message_id"))

							except IndexError:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
							except:
								bot.sendMessage(target, "❌ دستور اشتباه", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "دستورات":
							try:
								rules = open("help.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")

						elif msg.get("text").startswith("آپدیت دستورات") and msg.get("author_object_guid") in admins:
							try:
								rules = open("help.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت دستورات")))
								bot.sendMessage(target, "دستورات با موفقیت آپدیت شد.✅", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg.get("text").startswith("آپدیت قوانین") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت قوانین")))
								bot.sendMessage(target, "قوانین با موفقیت آپدیت شد.✅", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "!iran":
							try:
								rules = open("safar.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "لینک":
							try:
								rules = open("leink.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت لینک") and msg.get("author_object_guid") in admins:
							try:
								rules = open("leink.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت لینک")))
								bot.sendMessage(target, "✅  لینک گروه آپدیت شد ", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
						
						elif msg.get("text") == "منو":
							try:
								rules = open("mno.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "!ins":
							try:
								rules = open("Insta.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "!boo":
							try:
								rules = open("boo.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "چی بلدی":
							try:
								rules = open("balad.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت چی بلدی") and msg.get("author_object_guid") in admins:
							try:
								rules = open("balad.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت چی بلدی")))
								bot.sendMessage(target, "چی بلدی با موفقیت آپدیت شد.✅", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "بخش آنلاین":
							try:
								rules = open("anlaen.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text") == "ویسکال" and msg.get("author_object_guid") in admins :
							try:
								bot.startVoiceChat(target)
								bot.sendMessage(target, "ویسکال آغاز شد.✅", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target,"ops",msg["message_id"])
								
						elif msg.get("text") == "درباره گروه":
							try:
								rules = open("help.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت درباره") and msg.get("author_object_guid") in admins:
							try:
								rules = open("rules.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت درباره")))
								bot.sendMessage(target, "درباره گروه آپدیت شد", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg["text"].startswith("!number") or msg["text"].startswith("بشمار"):
							try:
								response = get(f"http://api.codebazan.ir/adad/?text={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "متاسفانه نتیجه‌ای موجود نبود!", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "نتیجه برای شما ارسال شد.", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("زمان"):
							try:
								response = get("https://api.codebazan.ir/time-date/?td=all").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								print("err answer time")
								
						elif msg.get("text").startswith("رابرتو"):
							try:
								ans = ["بگو😒"," جونم😍💋","دیوونمون کردی😒","جونم عزیز دلم🙂💋","ای بابا چیه بگو😞"," چیههه😒😒😒"]
								bot.sendMessage(target,random.choice(ans),message_id=msg.get("message_id"))
							except:
								print("err code")
								
						elif msg.get("text").startswith("سلام"):
							try:
								ans = ["سلا‌‌‌‌‌‌‌‌‌‌م چطوری😍","سلا‌‌‌م زندگی🙃","سلا‌‌‌‌‌‌م خوبی؟😍","سلا‌‌‌م خوش اومدی😊","‌سلا‌‌‌‌‌م‌ عزیزم🙂","سلا‌‌‌م‌ جون دل😁"]
								bot.sendMessage(target,random.choice(ans),message_id=msg.get("message_id"))
							except:
								print("err code")
								
						elif msg.get("text").startswith("ربات"):
							try:
								ans = ["ر‌‌ا‌بر‌تو‌‌ صدام کن🥺🥺","من ربات نیستم را‌‌‌‌‌بر‌‌تو‌‌ هستم🥺‌‌","دیگه دوست ندارم چون ربا‌‌‌‌ت‌‌‌ صدام کردی😞"," ر‌‌با‌‌‌ت‌‌ عمته من ر‌ا‌بر‌‌‌‌‌‌تو هستم😒"]
								bot.sendMessage(target,random.choice(ans),message_id=msg.get("message_id"))
							except:
								print("err code")
						
						elif msg.get("text") == "تاریخ":
							try:
								bot.sendMessage(target, f"Date: {time.localtime().tm_year} / {time.localtime().tm_mon} / {time.localtime().tm_mday}", message_id=msg.get("message_id"))
							except:
								print("err date")
								
						elif msg.get("text") == "پاک" and msg.get("author_object_guid") in admins :
							try:
								bot.deleteMessages(target, [msg.get("reply_to_message_id")])
								bot.sendMessage(target, "پیام مورد نظر پاک شد...", message_id=msg.get("message_id"))
							except:
								print("err pak")
								
						elif msg.get("text").startswith("!cal") or msg.get("text").startswith("حساب"):
							msd = msg.get("text")
							if plus == True:
								try:
									call = [msd.split(" ")[1], msd.split(" ")[2], msd.split(" ")[3]]
									if call[1] == "+":
										try:
											am = float(call[0]) + float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
											plus = False
										except:
											print("err answer +")
										
									elif call[1] == "-":
										try:
											am = float(call[0]) - float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer -")
										
									elif call[1] == "*":
										try:
											am = float(call[0]) * float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer *")
										
									elif call[1] == "/":
										try:
											am = float(call[0]) / float(call[2])
											bot.sendMessage(target, "حاصل :\n"+"".join(str(am)), message_id=msg.get("message_id"))
										except:
											print("err answer /")
											
								except IndexError:
									bot.sendMessage(target, "متاسفانه دستور شما اشتباه میباشد!" ,message_id=msg.get("message_id"))
									plus= True
						
						elif hasInsult(msg.get("text"))[0] and not msg.get("author_object_guid") in admins :
							try:
								print("yek ahmagh fohsh dad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("fohsh pak shod")
							except:
								print("err del fohsh Bug")
								
						elif msg.get("text").startswith("خوبی") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "فدات تو خوبی😍", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						elif msg.get("text").startswith("نه") or msg.get("text").startswith("خبی"):
							try:
								bot.sendMessage(target, "چرا فدات شم😢", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						elif msg.get("text").startswith("مرسی") or msg.get("text").startswith("خوبم"):
							try:
								bot.sendMessage(target, "شکر😁", message_id=msg.get("message_id"))
							except:
								print("err answer hay")
								
						elif msg.get("text").startswith("چخبرا") or msg.get("text").startswith("چخبر"):
							try:
								bot.sendMessage(target, "صلامتیت از تو چخبر😍♥", message_id=msg.get("message_id"))
							except:
								print("err CheKhabar")
								
						elif msg.get("text") == "😐":
							try:
								bot.sendMessage(target, "چیه😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "عشقم":
							try:
								bot.sendMessage(target, "جونم😁💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "دوست دارم":
							try:
								bot.sendMessage(target, "منم دوست دارم عشقم😍♥", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "ایجان":
							try:
								bot.sendMessage(target, "ژون🤤", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "بخورمت":
							try:
								bot.sendMessage(target, "تموم میشم🥺", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "شبخیر":
							try:
								bot.sendMessage(target, "شبت پر ستاره خوب بخوابی😍✨", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "شب بخیر":
							try:
								bot.sendMessage(target, "شبت پر ستاره خوب بخوابی😍✨", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "😂":
							try:
								bot.sendMessage(target, "اوف خنده هاشو🤤", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "🥺":
							try:
								bot.sendMessage(target, "قیافشو😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "عجب":
							try:
								bot.sendMessage(target, "مش رجب", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "ممنون":
							try:
								bot.sendMessage(target, "خواهش میکنم😊", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "💔":
							try:
								bot.sendMessage(target, "نشکن😔💔", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
					
						elif msg.get("text") == "سلامتی":
							try:
								bot.sendMessage(target, "همیشه سلامت باشی😉", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "سلامتیت":
							try:
								bot.sendMessage(target, "همیشه سلامت باشی😉", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "صبخیر":
							try:
								bot.sendMessage(target, "صبتون بخیر خوشکلا😃✨", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "صبح بخیر":
							try:
								bot.sendMessage(target, "صبتون بخیر خوشکلا😃✨", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "هعی":
							try:
								bot.sendMessage(target, "نکش رابرتو فدات شه😔💔", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "هی":
							try:
								bot.sendMessage(target, "نکش میدونم سخته درکت میکنم😔💔", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "بخند":
							try:
								bot.sendMessage(target, "😒😂", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "عیجان":
							try:
								bot.sendMessage(target, "ژون🤤", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "هعب":
							try:
								bot.sendMessage(target, "اوفف خسته شدیم😞", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "بای":
							try:
								bot.sendMessage(target, "بسلامت بری برنگردی👋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "خدافظ":
							try:
								bot.sendMessage(target, "بسلامت خوش گذشت", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اره":
							try:
								bot.sendMessage(target, "آجر پاره", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "چند سالته":
							try:
								bot.sendMessage(target, "1 سالمه 🥺", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "بات":
							try:
								bot.sendMessage(target, "بات نگو من رابرتو هستم🥺🥺", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "عاشقتم":
							try:
								bot.sendMessage(target, "اوف کراش بزنم روت عشقم🤤♥", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "میخوام باهات رل بزنم":
							try:
								bot.sendMessage(target, "جون بیا پی وی باهم رل بزنیم شیطون😉", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "کراشم روت":
							try:
								bot.sendMessage(target, "همه روم کراش میزنن خوشکله😌", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اصل":
							try:
								bot.sendMessage(target, "‌رابرتو‌‌ ‌‌1 ساله از شهر ربات ها😁😁", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اصل بده":
							try:
								bot.sendMessage(target, "‌رابرتو‌‌ ‌‌1 ساله از شهر ربات ها😁😁", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "پدرت کجاست":
							try:
								bot.sendMessage(target, "‌خونتون😉👍", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "برلیم":
							try:
								bot.sendMessage(target, "‌آره چرا که نه عزیزم😉💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "بابات کجاست":
							try:
								bot.sendMessage(target, "‌خونتون😉👍", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "😍":
							try:
								bot.sendMessage(target, "‌چشاشو قربون چشات برم من😍💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "چطوری":
							try:
								bot.sendMessage(target, "‌فدات تو چطوری😌💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "روت کراشم":
							try:
								bot.sendMessage(target, "‌همه روم کراش میزنن خوشکله😌", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "دوسم داری":
							try:
								bot.sendMessage(target, "‌هم دوست دارم هم دیوونتم دلبر😌♥", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "ب ت چ":
							try:
								bot.sendMessage(target, "‌بیا برو گمشو😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "به تو چه":
							try:
								bot.sendMessage(target, "‌بیا برو گمشو😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "😒":
							try:
								bot.sendMessage(target, "‌قهر نکن دیگه😂😁", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "فدام میشی":
							try:
								bot.sendMessage(target, "‌چرا نشم خوشگله😁💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "فدام شو":
							try:
								bot.sendMessage(target, "‌چرا نشم خوشگله😁💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "فدام بشو":
							try:
								bot.sendMessage(target, "‌چرا نشم خوشگله😁💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "جون":
							try:
								bot.sendMessage(target, "‌بادمجون🤭😁", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اصل مدیر":
							try:
								bot.sendMessage(target, "‌دنی 16", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اصل مدیرت":
							try:
								bot.sendMessage(target, "‌دنی 16", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اصل سازنده":
							try:
								bot.sendMessage(target, "‌دنی 16", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اصل سازندت":
							try:
								bot.sendMessage(target, "‌محمد", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "سازنده":
							try:
								bot.sendMessage(target, "‌@Zn_MmD_Zn", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "س":
							try:
								bot.sendMessage(target, "‌معلمت بهت یاد نداده مثل آدم ‌سلا‌‌م‌‌ ‌‌کنی؟😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "😐😂":
							try:
								bot.sendMessage(target, "‌به چی میخندی شیطون🤨", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "😂😐":
							try:
								bot.sendMessage(target, "‌به چی میخندی شیطون🤨", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "افرین":
							try:
								bot.sendMessage(target, "‌مر‌سی‌🙂‌", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "فیلتری بلدی":
							try:
								bot.sendMessage(target, "آره پدرت بهم یاد داد😔😂", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "آفرین":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌م‍‌ر‌سی‌🙂‌‌", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "♥":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌فدای قلب مهربونت🙂", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "❤":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌فدای قلب مهربونت🙂", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "صلام":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌سلا‌م‌‌‍‍‌ جون دل‌😁", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "صلم":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌سلا‌م جون دل‌‌😁", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "سلم":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌سلا‌م جون دل😁", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "چش":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌چش نه چشم چ+ش+م=چشم😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "چشم":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌بی بلا عزیزم🙂💋", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "مدیر":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌@Traouton", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "قلب":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌💜🧡💛💚")
								bot.sendMessage(target, "‌‍‍‌‍‍‌🧡💜💛🧡")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💚🧡💜💛")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💛💚🧡💜")
								bot.sendMessage(target, "‌‍‍‌‍‍‌✅")
							except:
								print("err poker answer")
								
						elif msg.get("text") == "انفجار":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣_____🚶")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣____🚶")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣___🚶")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣__🚶")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣_🚶")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣🚶")
								bot.sendMessage(target, "‌‍‍‌‍‍‌🩸💥boom💥🩸")
							except:
								print("err poker answer")
								
						elif msg.get("text") == "ماشین":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣___🏎")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣__🏎")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣_🏎")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💣🏎")
								bot.sendMessage(target, "‌‍‍‌‍‍‌💥boom💥")
							except:
								print("err poker answer")
								
						elif msg.get("text") == "پازل":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌🏮-بخش پازل \n • پازل بلاکی \n ➖ https://b2n.ir/MC_rBOT5 \n • ساحل پاپ \n ➖ https://b2n.ir/MC_rBOT14 \n • جمع اعداد \n ➖ https://b2n.ir/MC_rBOT15 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اکشن":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌🥊- بخش اکشن \n • نینجای جاذبه  \n ➖ https://b2n.ir/MC_rBOT3 \n • رانندگی کن یا بمیر \n ➖ https://b2n.ir/MC_rBOT9 \n • کونگ فو \n ➖ https://b2n.ir/MC_rBOT11 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "ورزشی":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌🏀- بخش ورزشی  \n • فوتبال استار  \n ➖ https://b2n.ir/MC_rBOT2 \n • بسکتبال \n ➖ https://b2n.ir/MC_rBOT24 \n • پادشاه شوت کننده \n ➖ https://b2n.ir/MC_rBOT255 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "پرتحرک":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌💥- بخش پرتحرک \n • گربه دیوانه  \n ➖ https://b2n.ir/MC_rBOT4 \n • ماهی بادکنکی \n ➖ https://b2n.ir/MC_rBOT13 \n • دینگ دانگ \n ➖ https://b2n.ir/MC_rBOT12 \n 🔴 راهنمایی: یکی از لینک ها را انتخاب کرده و کلیک کنید ؛ گزینه PLAY رو بزنید.", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.pin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "پیام مورد نظر با موفقیت سنجاق شد!", message_id=msg.get("message_id"))
							except:
								print("err pin")
								
						elif msg.get("text") == "برداشتن سنجاق" and msg.get("author_object_guid") in admins :
							try:
								bot.unpin(target, msg["reply_to_message_id"])
								bot.sendMessage(target, "پیام مورد نظر از سنجاق برداشته شد!", message_id=msg.get("message_id"))
							except:
								print("err unpin")
								
						elif msg.get("text").startswith("trans"):
							try:
								responser = get(f"https://api.codebazan.ir/translate/?type=json&from=en&to=fa&text={msg.get('text').split()[1:]}").json()
								al = [responser["result"]]
								bot.sendMessage(msg.get("author_object_guid"), "پاسخ به ترجمه:\n"+"".join(al)).text
								bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("gold"):
						    try:
							    responser = get(f"https://www.wirexteam.ga/gold").text
							    bot.sendMessage(target, responser,message_id=msg["message_id"])
						    except:
							    bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("font"):
							try:
								response = get(f"https://api.codebazan.ir/font/?text={msg.get('text').split()[1]}").json()
								bot.sendMessage(msg.get("author_object_guid"), "\n".join(list(response["result"].values())[:110])).text
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "نتیجه رو برات ارسال کردم😘", message_id=msg["message_id"])
						
						elif msg.get("text").startswith("جوک") or msg.get("text").startswith("jok") or msg.get("text").startswith("!jok"):
							try:
								response = get("https://api.codebazan.ir/jok/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("ذکر") or msg.get("text").startswith("zekr") or msg.get("text").startswith("!zekr"):
							try:
								response = get("http://api.codebazan.ir/zekr/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی پیش اومد!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("حدیث") or msg.get("text").startswith("hadis") or msg.get("text").startswith("!hadis"):
							try:
								response = get("http://api.codebazan.ir/hadis/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی تو ارسال پیش اومد!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("بیو") or msg.get("text").startswith("bio") or msg.get("text").startswith("!bio"):
							try:
								response = get("https://api.codebazan.ir/bio/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "ببخشید، خطایی تو ارسال پیش اومد!", message_id=msg["message_id"])
								
						elif msg["text"].startswith("!weather"):
							try:
								response = get(f"https://api.codebazan.ir/weather/?city={msg['text'].split()[1]}").json()
								bot.sendMessage(msg["author_object_guid"], "\n".join(list(response["result"].values())[:20])).text
								bot.sendMessage(target, "نتیجه بزودی برای شما ارسال خواهد شد...", message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "متاسفانه نتیجه‌ای موجود نبود!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("دیالوگ"):
							try:
								response = get("http://api.codebazan.ir/dialog/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "متاسفانه تو ارسال مشکلی پیش اومد!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("دانستنی"):
							try:
								response = get("http://api.codebazan.ir/danestani/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "دستورت رو اشتباه وارد کردی", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("پ ن پ") or msg.get("text").startswith("!pa-na-pa") or msg.get("text").startswith("په نه په"):
							try:
								response = get("http://api.codebazan.ir/jok/pa-na-pa/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "شرمنده نتونستم بفرستم!", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("الکی مثلا") or msg.get("text").startswith("!alaki-masalan"):
							try:
								response = get("http://api.codebazan.ir/jok/alaki-masalan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "نشد بفرستم:(", message_id=msg["message_id"])
								
						elif msg.get("text").startswith("داستان") or msg.get("text").startswith("!dastan"):
							try:
								response = get("http://api.codebazan.ir/dastan/").text
								bot.sendMessage(target, response,message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "مشکلی پیش اومد!", message_id=msg["message_id"])
							
						elif msg.get("text").startswith("پینگ"):
							try:
								responser = get(f"https://api.codebazan.ir/ping/?url={msg.get('text').split()[1]}").text
								bot.sendMessage(target, responser,message_id=msg["message_id"])
							except:
								bot.sendMessage(target, "دستور رو درست وارد کن دیگه😁", message_id=msg["message_id"])
								
						elif "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
							try:
								print("Yek ahmagh forwared Zad")
								bot.deleteMessages(target, [str(msg.get("message_id"))])
								print("tabligh forearedi pak shod")
							except:
								print("err delete forwared")
						
						elif msg.get("text") == "قوانین":
							try:
								rules = open("rules.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
								
						elif msg.get("text") == "1":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اسم رلتو بگو", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "2":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌میوه مورد علاقت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "3":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌برو پی وی یک نفر درخواست رل کن", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "4":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌سفیدی یا برنز یا سبزه یا سیاه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "5":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌کون یا کس یا کیر؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "6":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگه دختری با نفر بعد س... کن اگه پسری به نفر بعدی کون بده", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "7":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ای خرشانس شانس اوردی اندفه سوال نمیپرسم ازت نفر بعدی عدد بفرست برام", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "8":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌روزی چند بار بهش فک میکنی ؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "9":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تیکه کلامت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "10":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌حاضری در برابر صد میلیون پول شب با همجنست بخابی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "11":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا حالا خاستگار داشتی یا رفتی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "12":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌رقاص خوبی هستی تو عروسیا؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "13":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اخرین باری که فیلم سوپر دیدی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "14":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌قد و وزنت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "15":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌نفر بعدی رو واسه 1 روز بلاک کن", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "16":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ویس بده آروق بزن", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "17":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌معدل پارسالت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "18":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ویس بده و بگو هایاهههههه", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "19":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌خوشگلترین دختر گپ؟ 😂‌‌", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "20":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌چشم بسته یه چیزی تایپ کن بفرس ", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "21":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌خوشگلترین پسر گپ😂", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "22":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اسم کراشت/رلت چیه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "23":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ از پیامای رلت یا کراشت شات بده", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "24":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌فامیلیت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "25":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌آهنگ مورد علاقت", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "26":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگه یه جنس مخالف که نسبتی باهات نداشته باشه بت بگه بیا بیرون باهاش میری؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "27":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌خواهر برادر داری؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "28":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌28 تو کونت 😐", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "29":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌دوس داری با کی ازدواج کنی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "30":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌برو پی یه نفر فش بده", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "31":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا حالا دوس دختر یا دوس پسرت رو از ته دل دوست داشتی و ولش کرده باشی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "32":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌چند بار رل زدی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "33":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌لخت جنس مخالفتو دیدی تا حالا ؟کی بوده ؟توضیح بده", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "34":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا حالا عاشق شدی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "35":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌رو کی کراشی تو گپ؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "36":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌دوس داری بری کجا؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "37":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌نفر بعدی بهت سوال جرعت بگه", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "38":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌مادرتو بیشتر دوس داری یا پدرتو؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "39":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌احساسات نسبت به خانوادت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "40":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ویس بده صدا یکی از این حیون ها رو در بیار(خر، گاو، سگ،گوسفند)", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "41":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا حالا دخانیات مصرف کردی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "42":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌چقدر حقوق میگیری ماهیانه؟ اگر حقوق نمیگیری، چقدر خرجته واس ی ماه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "43":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌دوس داری دهن کیو بگایی", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "44":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگه نامرئی بشی چیکار میکنی", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "45":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ت دسشویی ب چی فک میکنی", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "46":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌از نتایج گوگل اسکرین شات بده", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "47":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگ بچه دار شی اسمشو چی میزاری", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "48":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا حالا پیش کسی گوزیدی سوتی بدی😂 یا کسی پیشت گوزیده؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "49":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌آخرین باری که خودتو خیس کردی کی بوده؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "50":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اصلی‌ترین چیزی که توی جنس مقابل برای تو جذابه چیه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "51":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌از یکی تو گپ درخواست ازدواج کن", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "52":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا حالا ت حموم دسشویی کردی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "53":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌دوس داری کی از گپ ریم شه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "54":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌رنگ چشات؟رنگ موهات؟رنگ پوستت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "55":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌پشمالو دوست داری یا صافو صیغعلی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "56":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌کسی تا به حال تورو لخت دیده؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "57":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌میخوری یا میبــری؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "58":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌کدومش بدتره؟(تو دسشویی یهو اب داغ شه _ تو حموم یهو اب سرد شه)", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "59":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌از گالریت شات بده", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "60":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا به حال شده (پسری_دختری) که دوستش داری بفهمه، و بهت جواب منفی بده؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "61":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ی سوتی ک توی کلاس دادی چیه", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "62":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌دوستاتو انگولک کردی یا اونا تورو؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "63":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تا حالا لباسای مامان یا باباتو پوشیدی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "64":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگه عاشق رل دوستت باشی ب دوستت ی دستی میزنی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "65":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌کیو انتخاب میکنی؟(اونی که دوست داره یا اونی که دوسش داری)", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "66":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اخرین باری ک حشری شدی کی بوده و چطور؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "67":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌😂😋کیرم رو چقدر می مکی", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "68":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌روی ی صندلی کیره روی ی صندلی کیک رو کدوم میشینی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "69":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تاحالا به خودکشی فکر کردی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "70":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ تو فامیل از کی متنفری", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "71":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگه از خواب بیدار شی و ببینی جنسیتت عوض شده چیکار میکنی", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "72":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌شب با لباس راحتی میخابی یا لخت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "73":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌س.س خشن یا آروم؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "74":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌(دختر یا پسر) رویاهات چه شکلیه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "75":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌با تف جق میزنی یا با کرم؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "76":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگه۱۰میلیارد پول داشته باشی چیکار میکنی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "77":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌کبود کردن لب یا گردن؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "78":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اسم دوست صمیمیت چیه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "79":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌عشق یا پول؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "80":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌برو پیوی مامانت پیام بده بهش بگو مامان من رل زدم😂👍", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "81":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ویس بده بگو من خرم", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "82":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌(دختر)حاضری کیر عشقتو بخوری؟/(پسر)حاضری کسشو بلیسی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "83":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌بدترین خاطره زندگیت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "84":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌حاضری بخاطر پول موهاتو بزنی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "85":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌لز یا گی داشتی", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "86":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌بعد نفر بعدی بگو عاشقتم😂🤍", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "87":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌چخبر؟😐😂", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "88":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌برو به رلت بگو کات اسکرین بفرس، البته اگه رل داری!", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "89":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌رنگ شرتت؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "90":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌شمارتو بفرست", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "91":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌کسیو از لب بوسیدی؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "92":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌با نفر بعدی 1 روز رل بزن", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "93":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌خوشتیپ هستی یا خوش قیافه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "94":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌لباس زیر چه رنگ حشریت میکنه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "95":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌غذا های مامانتو دوس داری یا فست فود؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "96":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌ اسم سه نفر تو مجازی ک دوسشون داری", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "97":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تاریخ تولدت", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "98":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌خجالتی هستی یا پرو؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "99":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌تو جذابتری یا بهترین دوست", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "100":
							try:
								bot.sendMessage(target, "‌‍‍‌‍‍‌اگه همین الان بهت بگم دوست دارم واکنشت چیه؟", message_id=msg.get("message_id"))
							except:
								print("err poker answer")
								
						elif msg.get("text") == "اسم فامیل":
							try:
								rules = open("smf.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err ghanon")
								
						elif msg.get("text") == "بخش بازی":
							try:
								rules = open("byb.txt","r",encoding='utf-8').read()
								bot.sendMessage(target, str(rules), message_id=msg.get("message_id"))
							except:
								print("err dastorat")
								
						elif msg.get("text").startswith("آپدیت بخش بازی") and msg.get("author_object_guid") in admins:
							try:
								rules = open("byb.txt","w",encoding='utf-8').write(str(msg.get("text").strip("آپدیت بخش بازی")))
								bot.sendMessage(target, "بخش بازی با موفقیت آپدیت شد.✅", message_id=msg.get("message_id"))
								# rules.close()
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
							
						elif msg.get("text") == "حالت ارام فعال" and msg.get("author_object_guid") in admins:
							try:
								number = 5
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام برای "+str(number)+"ثانیه فعال شد", message_id=msg.get("message_id"))
								
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))
								
						elif msg.get("text") == "!speak" or msg.get("text") == "speak" or msg.get("text") == "Speak" or msg.get("text") == "بگو":
							try:
								if msg.get('reply_to_message_id') != None:
									msg_reply_info = bot.getMessagesInfo(target, [msg.get('reply_to_message_id')])[0]
									if msg_reply_info['text'] != None:
										text = msg_reply_info['text']
										speech = gTTS(text)
										changed_voice = io.BytesIO()
										speech.write_to_fp(changed_voice)
										b2 = changed_voice.getvalue()
										changed_voice.seek(0)
										audio = MP3(changed_voice)
										dur = audio.info.length
										dur = dur * 1000
										f = open('sound.ogg','wb')
										f.write(b2)
										f.close()
										bot.sendVoice(target , 'sound.ogg', dur,message_id=msg["message_id"])
										os.remove('sound.ogg')
										print('sended voice')
								else:
									bot.sendMessage(target, 'پیام شما متن یا کپشن ندارد',message_id=msg["message_id"])
							except:
								print('server gtts bug')
							
						elif msg.get("text") == "حالت ارام غیر فعال" and msg.get("author_object_guid") in admins:
							try:
								number = 0
								bot.setGroupTimer(target,number)

								bot.sendMessage(target, "✅ حالت آرام غیرفعال شد", message_id=msg.get("message_id"))

							except:
								bot.sendMessage(target, "لطفا دستور رو صحیح وارد کنید!", message_id=msg.get("message_id"))


						elif msg.get("text").startswith("اخطار") and msg.get("author_object_guid") in admins:
							try:
								user = msg.get("text").split(" ")[1][1:]
								guid = bot.getInfoByUsername(user)["data"]["chat"]["abs_object"]["object_guid"]
								if not guid in admins :
									alert(guid,user)
									
								else :
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
									
							except IndexError:
								guid = bot.getMessagesInfo(target, [msg.get("reply_to_message_id")])[0]["author_object_guid"]
								user = bot.getUserInfo(guid)["data"]["user"]["username"]
								if not guid in admins:
									alert(guid,user)
								else:
									bot.sendMessage(target, "❌ کاربر ادمین میباشد", message_id=msg.get("message_id"))
							except:
								bot.sendMessage(target, "❌ لطفا دستور را به درستی وارد کنید", message_id=msg.get("message_id"))



						elif msg.get("text") == "قفل گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["AddMember"])
								bot.sendMessage(target, "🔒 گروه قفل شد", message_id=msg.get("message_id"))
							except:
								print("err lock GP")

						elif msg.get("text") == "بازکردن گروه" or msg.get("text") == "باز کردن گروه" and msg.get("author_object_guid") in admins :
							try:
								bot.setMembersAccess(target, ["SendMessages","AddMember"])
								bot.sendMessage(target, "🔓 گروه اکنون باز است", message_id=msg.get("message_id"))
							except:
								print("err unlock GP")

					else:
						if msg.get("text") == "!start" or msg.get("text") == "/start" and msg.get("author_object_guid") in admins :
							try:
								sleeped = False
								bot.sendMessage(target, "ربا‌ت با موفقیت روشن شد!", message_id=msg.get("message_id"))
							except:
								print("err on bot")
								
				elif msg["type"]=="Event" and not msg.get("message_id") in answered and not sleeped:
					name = bot.getGroupInfo(target)["data"]["group"]["group_title"]
					data = msg['event_data']
					if data["type"]=="RemoveGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"‼️ کاربر {user} به دلیل رعایت نکردن قوانین \nازگروه اخراج شد", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err rm member answer")
					
					elif data["type"]=="AddedGroupMembers":
						try:
							user = bot.getUserInfo(data['peer_objects'][0]['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"هــای {user} عزیز 😘🌹 \n • به گـروه {name} خیـلی خوش اومدی 😍❤️ \nلطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی!\nبرای دریافت دستورات کلمه دستورات را ارسال نمایید @Zn_MmD_Zn", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err add member answer")
					
					elif data["type"]=="LeaveGroup":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"بسلامت 👋 {user}", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Leave member Answer")
							
					elif data["type"]=="JoinedGroupByLink":
						try:
							user = bot.getUserInfo(data['performer_object']['object_guid'])["data"]["user"]["first_name"]
							bot.sendMessage(target, f"هــای {user} عزیز 😘🌹 \n • به گـروه {name} خیـلی خوش اومدی 😍❤️ \nلطفا قوانین رو رعایت کن .\n 💎 برای مشاهده قوانین کافیه کلمه (قوانین) رو ارسال کنی!\nبرای دریافت دستورات را ارسال نمایید @Zn_MmD_Zn", message_id=msg["message_id"])
							# bot.deleteMessages(target, [msg["message_id"]])
						except:
							print("err Joined member Answer")
							
				else:
					if "forwarded_from" in msg.keys() and bot.getMessagesInfo(target, [msg.get("message_id")])[0]["forwarded_from"]["type_from"] == "Channel" and not msg.get("author_object_guid") in admins :
						bot.deleteMessages(target, [msg.get("message_id")])
						guid = msg.get("author_object_guid")
						user = bot.getUserInfo(guid)["data"]["user"]["username"]
						bot.deleteMessages(target, [msg.get("message_id")])
						alert(guid,user,True)
					
					continue
			except:
				continue

			answered.append(msg.get("message_id"))
			print("[" + msg.get("message_id")+ "] >>> " + msg.get("text") + "\n")

	except KeyboardInterrupt:
		exit()

	except Exception as e:
		if type(e) in list(retries.keys()):
			if retries[type(e)] < 3:
				retries[type(e)] += 1
				continue
			else:
				retries.pop(type(e))
		else:
			retries[type(e)] = 1
			continue
