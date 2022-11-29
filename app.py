from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import re 
from pymongo import MongoClient
from datetime import datetime
from datetime import date
from pytz import timezone 

cluster = MongoClient("mongodb+srv://lna:lna@cluster0.ou6skhm.mongodb.net/?retryWrites=true&w=majority")
db = cluster["bakery_test"]
users = db["users"]
orders = db["orders"]
app = Flask(__name__)


@app.route("/", methods=["get", "post"])
def reply():
    text =request.form.get("Body")
    number = request.form.get("From")
    number = number.replace("whatsapp:","")
    response = MessagingResponse()
    ind_time = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%b-%Y %I:%H:%M %p')
    user = users.find_one({"number":number})
    if bool(user) == False:
      response.message("Hi, Thanks for contacting *Incafe*\nYou can choose from one of the options below:"
      "\n\n*Type*\n\n1️⃣ to *Contact* us\n2️⃣ To *order* snacks\n3️⃣ To know our *working hours*\n4️⃣ To get our *address*")
      users.insert_one({"number":number,"status":"main","messages":[]})
    elif user['status']== "main":
      try:
        option =int(text)
      except:
        response.message("Please Add a valid responds")
        return str(response)
      if option == 1:
        response.message("You can contact us through phone or  e-mail.\n\n*Phone*: 9597009155\n*Email*: contactus@gmil.com")
      elif option==2:
        response.message("you have enterd *ordering mode*")
        users.update_one({"number":number},{"$set":{"status":"ordering"}})
        response.message("You can slect one of the\n1️⃣Red Velvet Cake\n2️⃣Dark Forest Cake\n3️⃣Ice Cream Cake\n4️⃣Plum Cake\n5️⃣Sponge Cake\n6️⃣Genoise Cake\n7️⃣Angel Cake\n8️⃣Carrot Cake\n9️⃣Fruit Cake\n0️⃣GO Back")
      elif option==3:
        response.message("We work everyday from *9 AM to 10 PM*")
      elif option==4:
        addr=response.message("Our address:\n*5-48,murgan nagar*\n*raman nagar*\n*mettur dam*\n*salem-636403*")
      else:
        response.message("Please Add a valid responds")
    elif user['status']== "ordering":
      try:
        option =int(text)
      except:
        response.message("Please Add a valid responds")
      if option==0:
         users.update_one({"number":number},{"$set":{"status":"main"}})
         response.message("You can choose from one of the options below:""\n\n*Type*\n\n1️⃣ to *Contact* us\n2️⃣ To *order* snacks\n3️⃣ To know our *working hours*\n4️⃣ To get our *address*")
      elif 1<= option <=9:
        cakes = ["Red Velvet Cake", "Dark Forest Cake", "Ice Cream Cake",
                     "Plum Cake", "Sponge Cake", "Genoise Cake", "Angel Cake", "Carrot Cake", "Fruit Cake"]
        slected = cakes[option-1]
        users.update_one({"number":number},{"$set":{"status":"Address"}})
        users.update_one({"number":number},{"$set":{"item":slected}})
        response.message("Excellent choice 😉")
        response.message("Please enter your address to conform your order")
      else:
        response.message("Please Add a valid responds")
    elif user["status"] == "Address":
      slected = user["item"]
      response.message("Thanks for shopping with us")
      response.message("Your order for *{}* in 10 mints your order will be packers\nand you can pick it".format(slected))
      orders.insert_one({"numbers":number,"item":slected,"Address":text,"Order_time":ind_time})
      users.update_one({"number":number},{"$set":{"status":"ordered"}})
    elif user["status"] == "ordered":
      response.message("Hi, Thanks for contacting again\nYou can choose from one of the options below:"
            "\n\n*Type*\n\n1️⃣ to *Contact* us\n2️⃣ To *order* snacks\n3️⃣ To know our *working hours*\n4️⃣ To get our *address*")
      users.update_one({"number":number},{"$set":{"status":"main"}})
    users.update_one({"number":number},{"$push":{"messages":{"text":text,"date":ind_time}}})
    return str(response)

    

if __name__ == "__main__":
    app.run()


    """
   #greet_word = ["hello","hi","Hi","Hello","Vnnakam"]
   # for i in greet_word:
   #or (text=="hello") or (text=="Hello") or (text=="Hi") or (text=="vannkam"):
    if "hi" or "hello" in text:
        response.message("hi👋")
          
    else:
      response.message("I don't Understand")
    """
