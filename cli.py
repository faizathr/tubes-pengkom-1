import time
import sys
import os
import datetime
import re

SERVICE_NAME = "TubesMarket"
SERVICE_HANDLE = "tubesmarket"

item_list = [["Laptop", 2360, 8000000, "laptop"], ["Keyboard", 4518, 300000, "keyboard"], ["Mouse", 1119, 100000, "mouse"]]

socmed_list = [['Instagram', f'https://www.instagram.com/{SERVICE_HANDLE}'], 
            ['Tiktok',f'https://www.tiktok.com/{SERVICE_HANDLE}'], 
            ['Youtube',f'https://www.youtube.com/{SERVICE_HANDLE}'],
            ['Facebook',f'https://www.facebook.com/{SERVICE_HANDLE}']]

marketplace_list = [["Tokopedia",f"https://www.tokopedia.com/{SERVICE_HANDLE}","We have been starting sales with Tokopedia since 2021, 4261\n\t  of items sold either inside or outside Medan and Jakarta.\n\t  Our offline stores are not open for public. We just accepting online orders.\n\t  But, if you are interested on checking our product quality live.\n\t  Feel free to find our contact person, to have a walk on our small exhibition."],
                    ["Bukalapak",f"https://www.bukalapak.com/{SERVICE_HANDLE}","We have been starting sales with Bukalapak since 2022, 123\n\t  of items sold either inside or outside Medan and Jakarta.\n\t  Our offline stores are not open for public. We just accepting online orders.\n\t  But, if you are interested on checking our product quality live.\n\t  Feel free to find our contact person, to have a walk on our small exhibition."],
                    ["Shopee",f"https://www.shopee.co.id/{SERVICE_HANDLE}","We have been starting sales with Shopee since 2020, best computer\n\t  stores existed in shopee, with lots of discount and good reviews, 6419 of items\n\t  sold either inside or outside Medan and Jakarta. Our offline stores\n\t  are not open for public. We just accepting online orders.\n\t  But, if you are interested on checking our product quality live.\n\t  Feel free to find our contact person, to have a walk on our small exhibition."]]

contact_list = [['WhatsApp','+62 XXX-XXXX-XXX'],
               ['Phone Number','+62 XXX-XXXX-XXX'],
               ['Line',f'@{SERVICE_HANDLE}'],
               ['Telegram',f'@{SERVICE_HANDLE}']]

payment_method = [['BCA','1234567890'], 
                  ['BNI','1234567890'],
                  ['BRI','1234567890'],
                  ['GOPAY',"+62 XXX-XXXX-XXX"],
                  ['DANA','+62 XXX-XXXX-XXX'],
                  ['SHOPEEPAY','+62 XXX-XXXX-XXX'],
                  ['LINKAJA',"+62 XXX-XXXX-XXX"],
                  ]

print(f"Bot\t: Hi! Welcome to {SERVICE_NAME}.\n\
          Type /store to check our marketplace\n\
          Type /stock to check our products stocks\n\
          Type /socmed to check our social media\n\
          Type /contact to contact us\n\
          Type /order to order our product\n\
          Type /cart to view your shopping cart\n\
          Type /clearcart to empty your shopping cart\n\
          Type /checkout to checkout yout shopping cart\n\
          Type /exit to exit this chatbot interface")

chatbot = True
username = ""
cart = []
while chatbot:
    user = input("You\t: ").lower()
    if user == "/help":
        print("Bot\t: Available Commands :-\n\
          /store - To check our marketplace\n\
          /stock - To check our products stocks\n\
          /socmed - To check our social media\n\
          /contact - To contact us\n\
          /order - To order our product\n\
          /cart - To view your shopping cart\n\
          /clearcart - To empty your shopping cart\n\
          /checkout - To checkout yout shopping cart\n\
          /exit - To exit this chatbot interface")
    elif user == "/store":
        store_text = "Bot\t: Checkout our marketplace!"
        for i in range(len(marketplace_list)):
            store_text += f"\n\n\t  {marketplace_list[i][0]}\n\t  {marketplace_list[i][1]}\n\t  {marketplace_list[i][2]}"
        print(store_text)
    elif user == "/stock":
        stock_text = "Bot\t: Here is the list of our current items availability"
        for i in range(len(item_list)):
            stock_text += f"\n\t  {item_list[i][0]}: {item_list[i][1]}"
        print(stock_text)
    elif user == "/socmed":
        socmed_text = f"Bot\t: {socmed_list[0][0]}: {socmed_list[0][1]}"
        for i in range(1,len(socmed_list)):
            socmed_text += f"\n\t  {socmed_list[i][0]}: {socmed_list[i][1]}"
        print(socmed_text)
    elif user == "/contact":
        contact_text = f"Bot\t: {contact_list[0][0]}: {contact_list[0][1]}"
        for i in range(1,len(contact_list)):
            contact_text += f"\n\t  {contact_list[i][0]}: {contact_list[i][1]}"
        print(contact_text)
    elif user == "/order":
        order_text = "Bot\t: Which product do you want to order?"
        for i in range(len(item_list)):
            order_text += f"\n\t  {str(i+1)}. {item_list[i][0]} ---> Rp {'{:20,.2f}'.format(item_list[i][2]).replace('.',',').replace(',','.','{:20,.2f}'.format(item_list[i][2]).count(',')).lstrip()}"
        for i in range(len(item_list)):
            order_text += f"\n\t  Type /buy {str(i+1)} to add {item_list[i][0]} to your cart."
        print(order_text)
    elif user.split(" ")[0] == "/buy":
        try:
            if item_list[int(user.split(" ")[1]) - 1][1]<=0:
                print(f'Bot\t: {item_list[int(user.split(" ")[1]) - 1][0]} is currently out of stock.\n\
          We are sure we are going to restock.\n\
          Please be patient.')
            else:
                if len(cart) == 0:
                    cart.append([item_list[int(user.split(" ")[1]) - 1][3],item_list[int(user.split(" ")[1]) - 1][0],1,item_list[int(user.split(" ")[1]) - 1][2]])
                else:
                    existing_selected_item = [0,0]
                    for i in range(len(cart)):
                        if cart[i][0] == item_list[int(user.split(" ")[1]) - 1][3]:
                            existing_selected_item[0] += 1
                            existing_selected_item[1] = i
                    if existing_selected_item[0] > 0:
                        cart[existing_selected_item[1]][2] += 1
                    else:
                        cart.append([item_list[int(user.split(" ")[1]) - 1][3],item_list[int(user.split(" ")[1]) - 1][0],1,item_list[int(user.split(" ")[1]) - 1][2]])
                print(f'Bot\t: {item_list[int(user.split(" ")[1]) - 1][0]} added to your cart.')
        except Exception as error:
            buy_error = f"Bot\t: Type /buy 1 to order {item_list[0][0]}."
            for i in range(1,len(item_list)):
                buy_error += f"\n\t  Type /buy {str(i+1)} to order {item_list[i][0]}."
            print(buy_error)
    elif user == "/cart":
        if len(cart) == 0:
            output = "Your cart is empty, use /order to buy something."
        else:
            output = ""
            total_price = 0
            total_items = 0
            for i in range(len(cart)):
                output += ("" if i == 0 else "\n\t  ") + f"{cart[i][1]} x {cart[i][2]} per Rp {'{:20,.2f}'.format(cart[i][3]).replace('.',',').replace(',','.','{:20,.2f}'.format(cart[i][3]).count(',')).lstrip()} = Rp {'{:20,.2f}'.format(cart[i][2]*cart[i][3]).replace('.',',').replace(',','.','{:20,.2f}'.format(cart[i][2]*cart[i][3]).count(',')).lstrip()}"
                total_price += cart[i][2]*cart[i][3]
                total_items += cart[i][2]
            output += f"\n\t  Subtotal ({total_items} item{'s' if total_items > 1 else ''}): Rp {'{:20,.2f}'.format(total_price).replace('.',',').replace(',','.','{:20,.2f}'.format(total_price).count(',')).lstrip()}"
        print(f"Bot\t: {output}")
    elif user == "/clearcart":
        if len(cart) == 0:
            output = "Your cart is already empty."
        else:
            cart = []
            output = "Your cart is cleared."
        print(f"Bot\t: {output}")
    elif user == "/checkout":
        if len(cart) == 0:
            print("Bot\t: Your cart is empty, use /order to buy something.")
        else:
            email = input("Bot\t: Please type in your email address\nYou\t: ")
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            while not re.fullmatch(regex, email):
                email = input("Bot\t: Please type in your valid email address\nYou\t: ")
            output = "Bot\t: Order Summary"
            total_price = 0
            total_items = 0
            for i in range(len(cart)):
                output += f"\n\t  {cart[i][1]} x {cart[i][2]} per Rp {'{:20,.2f}'.format(cart[i][3]).replace('.',',').replace(',','.','{:20,.2f}'.format(cart[i][3]).count(',')).lstrip()} = Rp {'{:20,.2f}'.format(cart[i][2]*cart[i][3]).replace('.',',').replace(',','.','{:20,.2f}'.format(cart[i][2]*cart[i][3]).count(',')).lstrip()}"
                total_price += cart[i][2]*cart[i][3]
                total_items += cart[i][2]
            output += f"\n\t  Subtotal ({total_items} item{'s' if total_items > 1 else ''}): Rp {'{:20,.2f}'.format(total_price).replace('.',',').replace(',','.','{:20,.2f}'.format(total_price).count(',')).lstrip()}"
            output += "\n\n\t  Here are the payment methods that you can choose"
            for i in range(len(payment_method)):
                output += f"\n\t  {payment_method[i][0]} ---> {payment_method[i][1]}"
            output += "\n\n\t  Don't forget to send your payment proof for us to confirm.\n\t  Don't hesitate to contact us through /contact if you have any questions."
            print(output)
            for i in range(len(cart)):
                for j in range(len(item_list)):
                    if cart[i][0] == item_list[j][3]:
                        item_list[j][1] -= cart[i][2]
            animation = "|/-\\"
            anicount = 0
            counttime = 0
            while (counttime != 200):
                time.sleep(0.075)
                sys.stdout.write("\r"+ "\t  Proccessing your purchase . . . " + animation[anicount])
                sys.stdout.flush()
                anicount = (anicount + 1)% 4
                counttime = counttime + 1
            cart = []
            print('\nBot\t: Payment has been confirmed. Thankyou for ordering!')
    elif user == "/exit":
        print(f"Bot\t: Thanks for using our chatbot!")
        exit()
    else:
        print(f"Bot\t: Sorry {user} is not a valid command\n\t  Type /help to check available commands")