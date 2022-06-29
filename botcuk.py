# -*- coding: utf-8 -*-
"""
Created on Tue Jun 28 08:07:15 2022

@author: Ismail
"""
def main():
    import telebot
    import pymongo
    import datetime
    import pandas as pd 
    
    def print_col(col):
        df = pd.DataFrame(col.find())
        print(df)
    
    def get_collection():
        client = pymongo.MongoClient()
        db = client["database"]
        col = db["transactions"]
        return col, db
    
    API_TOKEN = "5327586510:AAHhZoAddBQ0dw9y_Hq-6cRaAWG0ZnaGm5M"
    
    bot = telebot.TeleBot(API_TOKEN)
    
    # Handle '/start' and '/help'
    @bot.message_handler(commands=['help', 'start'])
    def send_welcome(message):
        bot.reply_to(message, """\
    Welcome! One Ring to rule them all, One Ring to find them, One Ring to bring them all, and in the darkness bind them.
    """)
    
    @bot.message.handler(commands=['balance'])
    def show_balance(message):
        col, db = get_collection()
        # summary by whole
        pipe = [{'$group': {'_id': None, 'total': {'$added_amount'}}}]
        total_until_now_cursor = db.transactions.aggregate(pipeline=pipe)
        cursorToList = list(total_until_now_cursor)
        for document in cursorToList:  
            bot.reply_to(message, "Total Balance: " + str(document['total']))
    
    
    @bot.message_handler(regexp="[\-\+]?[0-9]*(\.[0-9]+)?") # [+-]?([0-9]*[.])?[0-9]+
    def handle_message(message):
        print("\n\n if öncesi first" + str(message)) 
        col, db = get_collection()
        col.insert_one({"telegram_user_name": message.from_user.username, 
                   "added_amount": float(message.text),
                   "datetime": str(datetime.datetime.now())})
        
        # summary by whole
        pipe = [{'$group': {'_id': None, 'total': {'$sum': '$added_amount'}}}]
        total_until_now_cursor = db.transactions.aggregate(pipeline=pipe)
        cursorToList = list(total_until_now_cursor)
        for document in cursorToList:  
            bot.reply_to(message, "Total saved amount till now: " + str(document['total']))
    
        # summary by users
        pipe_by_user= [{'$group': {'_id': '$telegram_user_name', 'total': {'$sum': '$added_amount'}}}]
        pipeByUserCursor = db.transactions.aggregate(pipeline=pipe_by_user)
        pipeByuserCursorToList = list(pipeByUserCursor)
        for document in pipeByuserCursorToList:  
            bot.reply_to(message, "User @{} saved as much as: {}".format(str(document['_id']), str(document['total'])))


    bot.infinity_polling()

if __name__ == '__main__':
    main()