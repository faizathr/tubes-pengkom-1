from django.http import HttpRequest, HttpResponse
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from .models import ChatbotUser, ChatbotCart, ChatbotSale
from hashlib import sha256, sha512
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
import time as time
import base64
import json
import datetime
import requests
import urllib.parse

data = ChatbotUser.objects.filter(username='admin')

SERVICE_NAME = json.loads(data[0].variables)["SERVICE_NAME"]
SERVICE_HANDLE = json.loads(data[0].variables)["SERVICE_HANDLE"]
socmed_list = json.loads(data[0].variables)["socmed_list"]
for i in range(len(socmed_list)):
   socmed_list[i][1] = socmed_list[i][1].replace("{SERVICE_HANDLE}",SERVICE_HANDLE)
marketplace_list = json.loads(data[0].variables)["marketplace_list"]
for i in range(len(marketplace_list)):
   marketplace_list[i][1] = marketplace_list[i][1].replace("{SERVICE_HANDLE}",SERVICE_HANDLE)
contact_list = json.loads(data[0].variables)["contact_list"]
for i in range(len(contact_list)):
   contact_list[i][1] = contact_list[i][1].replace("{SERVICE_HANDLE}",SERVICE_HANDLE)
payment_method = json.loads(data[0].variables)["payment_method"]
TELEGRAM_API_TOKEN = data[0].telegram_token
API_KEY = data[0].api_key
item_list = json.loads(data[0].items_json)

def is_json(arr):
   try:
      json.loads(arr)
      return True
   except:
      return False

def rupiah(angka):
   return f"Rp {'{:20,.2f}'.format(angka).replace('.',',').replace(',','.','{:20,.2f}'.format(angka).count(',')).lstrip()}"

TODAY_UNIX = int(time.mktime(datetime.datetime(int(datetime.datetime.now().strftime("%Y")), int(datetime.datetime.now().strftime("%m").lstrip("0")), int(datetime.datetime.now().strftime("%d").lstrip("0"))).timetuple()))

updater = Updater(TELEGRAM_API_TOKEN,use_context=True)

def start(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   update.message.reply_text(
      f"Hi! Welcome to {SERVICE_NAME}.\n\
      Type /store to check our marketplace\n\
      Type /stock to check our products stocks\n\
      Type /socmed to check our social media\n\
      Type /contact to contact us\n\
      Type /order to order our product\n\
      Type /cart to view your shopping cart\n\
      Type /clearcart to empty your shopping cart\n\
      Type /checkout to checkout yout shopping cart")

def help(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   update.message.reply_text("""Available Commands :-
   /store - To check our marketplace
   /stock - To check our products stocks
   /socmed - To check our social media
   /contact - To contact us
   /order - To order our product
   /cart - To view your shopping cart
   /clearcart - To empty your shopping cart
   /checkout - To checkout yout shopping cart""")

def store(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   store_text = "Checkout our marketplace!"
   for i in range(len(marketplace_list)):
      store_text += f"\n\n{marketplace_list[i][0]}\n{marketplace_list[i][1]}\n{marketplace_list[i][2]}"
   update.message.reply_text(store_text)

def stock(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   data_stock = ChatbotUser.objects.filter(username='admin')
   item_stock = json.loads(data_stock[0].items_json)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   stock_text = "Here is the list of our current items availability"
   for i in range(len(item_stock)):
      stock_text += f"\n{item_stock[i][0]}: {item_stock[i][1]}"
   update.message.reply_text(stock_text)

def socmed(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   socmed_text = ""
   for i in range(len(socmed_list)):
      socmed_text += f"\n{socmed_list[i][0]}: {socmed_list[i][1]}"
   update.message.reply_text(socmed_text)

def contact(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   contact_text = ""
   for i in range(len(contact_list)):
      contact_text += f"\n{contact_list[i][0]}: {contact_list[i][1]}"
   update.message.reply_text(contact_text)

def order(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   order_text =""
   update.message.reply_text(f"Which product do you want to order?")
   for i in range(len(item_list)):
      order_text += f"\n{str(i+1)}. {item_list[i][0]} ---> {rupiah(item_list[i][2])}"
   update.message.reply_text(order_text)
   order_text2 =""
   for i in range(len(item_list)):
      order_text2 += f"\nType /buy {str(i+1)} to add {item_list[i][0]} to your cart."
   update.message.reply_text(order_text2)

def buy(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
   try:
      if item_list[int(context.args[0]) - 1][1]<=0:
         update.message.reply_text(str(item_list[int(context.args[0]) - 1][0])+"is currently out of stock.\n\
      We are sure we are going to restock.\n\
      Please be patient.")
      else:
         updatecart = ChatbotCart.objects.get(username=update.message.chat_id)
         jsoncart = json.loads(updatecart.items)
         if len(jsoncart) == 0:
            jsoncart.append([item_list[int(context.args[0]) - 1][3],item_list[int(context.args[0]) - 1][0],1,item_list[int(context.args[0]) - 1][2]])
            updatecart.items = json.dumps(jsoncart)
            updatecart.save()
         else:
            existing_selected_item = [0,0]
            for i in range(len(jsoncart)):
               if jsoncart[i][0] == item_list[int(context.args[0]) - 1][3]:
                  existing_selected_item[0] += 1
                  existing_selected_item[1] = i
            if existing_selected_item[0] > 0:
               jsoncart[existing_selected_item[1]][2] += 1
               updatecart.items = json.dumps(jsoncart)
               updatecart.save()
            else:
               jsoncart.append([item_list[int(context.args[0]) - 1][3],item_list[int(context.args[0]) - 1][0],1,item_list[int(context.args[0]) - 1][2]])
               updatecart.items = json.dumps(jsoncart)
               updatecart.save()
         update.message.reply_text(f"{item_list[int(context.args[0]) - 1][0]} added to your cart.")
   except Exception as error:
      buy_error = ""
      for i in range(len(item_list)):
         buy_error += f"\nType /buy {str(i+1)} to order {item_list[i][0]}."
      update.message.reply_text(buy_error)

def cart(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
      output = "Your cart is empty, use /order to buy something."
   else:
      carts = json.loads(query[0].items)
      if len(carts) == 0:
         output = "Your cart is empty, use /order to buy something."
      else:
         output = ""
         total_price = 0
         total_items = 0
         for i in range(len(carts)):
            output += f"{carts[i][1]} x {carts[i][2]} per {rupiah(carts[i][3])} = {rupiah(carts[i][2]*carts[i][3])}\n"
            total_price += carts[i][2]*carts[i][3]
            total_items += carts[i][2]
         output += f"Subtotal ({total_items} item{'s' if total_items > 1 else ''}): {rupiah(total_price)}"
   update.message.reply_text(output)

def clearcart(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
      output = "Your cart is already empty."
   else:
      carts = json.loads(query[0].items)
      if len(carts) == 0:
         output = "Your cart is already empty."
      else:
         emptycart = ChatbotCart.objects.get(username=update.message.chat_id)
         emptycart.items = json.dumps([])
         emptycart.save()
         output = "Your cart is cleared."
   update.message.reply_text(output)

def checkout(update: Update, context: CallbackContext):
   query = ChatbotCart.objects.filter(username=update.message.chat_id)
   if len(query) == 0:
      new_user = ChatbotCart(username=update.message.chat_id,items=[])
      new_user.save()
      update.message.reply_text("Your cart is empty, use /order to buy something.")
   else:
      data_stock = ChatbotUser.objects.get(username='admin')
      data_cart = ChatbotCart.objects.get(username=update.message.chat_id)
      carts = json.loads(query[0].items)
      if len(carts) == 0:
         update.message.reply_text("Your cart is empty, use /order to buy something.")
      else:
         output = "Order Summary\n"
         notify_message = f"There is a new checkout from user {update.message.chat_id}\n{datetime.datetime.now()} {datetime.datetime.now().strftime('%z')}\n"
         total_price = 0
         total_items = 0
         for i in range(len(carts)):
            output += f"{carts[i][1]} x {carts[i][2]} per {rupiah(carts[i][3])} = {rupiah(carts[i][2]*carts[i][3])}\n"
            notify_message += f"{carts[i][1]} x {carts[i][2]} per {rupiah(carts[i][3])} = {rupiah(carts[i][2]*carts[i][3])}\n"
            total_price += carts[i][2]*carts[i][3]
            total_items += carts[i][2]
         output += f"Subtotal ({total_items} item{'s' if total_items > 1 else ''}): {rupiah(total_price)}\n"
         notify_message += f"Subtotal ({total_items} item{'s' if total_items > 1 else ''}): {rupiah(total_price)}\n"
         output += "\nHere are the payment methods that you can choose"
         for i in range(len(payment_method)):
            output += f"\n{payment_method[i][0]} ---> {payment_method[i][1]}"
         output += "\n\nDon't forget to send your payment proof for us to confirm.\nDon't hesitate to contact us through /contact if you have any questions."
         update.message.reply_text(output)
         data_sales = ChatbotSale(username=update.message.chat_id,sales=json.dumps(carts),date=TODAY_UNIX)
         data_sales.save()
         notify_target = json.loads(data_stock.notify_id)
         for i in notify_target:
            fetch = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?chat_id={i}&text={urllib.parse.quote(notify_message)}')
         item_stock = json.loads(data_stock.items_json)
         item_cart = json.loads(data_cart.items)
         for i in range(len(item_cart)):
            for j in range(len(item_stock)):
               if item_cart[i][0] == item_stock[j][3]:
                  item_stock[j][1] -= item_cart[i][2]
         data_stock.items_json = json.dumps(item_stock)
         data_stock.save()
         update.message.reply_text("Proccessing your purchase . . .")
         time.sleep(5)
         data_cart.items = json.dumps([])
         data_cart.save()
         update.message.reply_text(f'Payment has been confirmed. Thankyou for ordering!')
def unknown(update: Update, context: CallbackContext):
   update.message.reply_text(
      "Sorry '%s' is not a valid command\nType /help to check available commands" % update.message.text)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', help))
updater.dispatcher.add_handler(CommandHandler('store', store))
updater.dispatcher.add_handler(CommandHandler('stock', stock))
updater.dispatcher.add_handler(CommandHandler('socmed', socmed))
updater.dispatcher.add_handler(CommandHandler('contact', contact))
updater.dispatcher.add_handler(CommandHandler('order', order))
updater.dispatcher.add_handler(CommandHandler('buy', buy))
updater.dispatcher.add_handler(CommandHandler('cart', cart))
updater.dispatcher.add_handler(CommandHandler('clearcart', clearcart))
updater.dispatcher.add_handler(CommandHandler('checkout', checkout))
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))

updater.start_polling()

def index(request):
   return HttpResponse("200 OK")

def api(request):
   try:
      data_admin = ChatbotUser.objects.get(username='admin')
      if sha256(request.GET['key'].encode('utf-8')).hexdigest() == sha256(API_KEY.encode('utf-8')).hexdigest():
         if request.GET.get('type') and request.GET.get('data'):
            if request.GET["type"] == "request":
               if request.GET["data"] == "variables":
                  return HttpResponse(data_admin.variables)
               elif request.GET["data"] == "items":
                  return HttpResponse(data_admin.items_json)
               elif request.GET["data"] == "notify":
                  return HttpResponse(data_admin.notify_id)
               elif request.GET["data"] == "cart" and request.GET.get('value'):
                  data_cart = ChatbotCart.objects.filter(username=request.GET["value"])
                  if len(data_cart) == 0:
                     new_user = ChatbotCart(username=request.GET["value"],items=[])
                     new_user.save()
                     output = "[]"
                  else:
                     output = data_cart[0].items
                  return HttpResponse(output)
               elif request.GET["data"] == "sendnotify" and request.GET.get('value'):
                  notify_target = json.loads(data_admin.notify_id)
                  for i in notify_target:
                     fetch = requests.get(f'https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage?chat_id={i}&text={urllib.parse.quote(request.GET["value"])}')
               else:
                  return HttpResponse(status=400)
            elif request.GET["type"] == "update" and request.GET.get('value'):
               if request.GET["data"] == "telegram":
                  data_admin.telegram_token = request.GET["value"]
                  data_admin.save()
                  return HttpResponse("Success")
               elif request.GET["data"] == "notify":
                  if is_json(request.GET["value"]):
                     data_admin.notify_id = request.GET["value"]
                     data_admin.save()
                     return HttpResponse("Success")
                  else:
                     return HttpResponse(status=400)
               elif request.GET["data"] == "cart" and request.GET.get('username'):
                  if is_json(request.GET["value"]):
                     data_cart = ChatbotCart.objects.filter(username=request.GET["username"])
                     if len(data_cart) == 0:
                        new_user = ChatbotCart(username=request.GET["username"],items=request.GET["value"])
                        new_user.save()
                     else:
                        update_cart = ChatbotCart.objects.get(username=request.GET["username"])
                        update_cart.items = request.GET["value"]
                        update_cart.save()
                     return HttpResponse("Success")
                  else:
                     return HttpResponse(status=400)
               else:
                  return HttpResponse(status=400)
            else:
               return HttpResponse(status=400)
         else:
            return HttpResponse(status=404)
      else:
         return HttpResponse("Invalid key")
   except:
      return HttpResponse(status=400)
   
   

def admin(request):
   if request.session.get('user') and request.session.get('session'):
      data = ChatbotUser.objects.get(username=request.session['user'])
      if request.session['session'] == data.password:
         response = HttpResponse(status=302)
         response['Location'] = '/dashboard/'
         return response
      else:
         return render(request,("admin.html"))
   else:
      return render(request,("admin.html"))

def dashboard(request):
   global TODAY_UNIX
   if request.GET.get('logout') and request.GET['logout'] == "1":
      request.session['user'] = ""
      request.session['session'] = ""
      response = HttpResponse(status=302)
      response['Location'] = '/admin/'
      return response
   elif request.session.get('user') and request.session.get('session'):
      data_admin = ChatbotUser.objects.get(username=request.session['user'])
      if request.session['session'] == data_admin.password:
         data_cart = ChatbotCart.objects.all()
         SOURCE_CODE = "https://github.com/faizath/tubes-pengkom-1"
         today_data_sales = ChatbotSale.objects.filter(date=TODAY_UNIX)
         total_data_sales = ChatbotSale.objects.all()
         today_income = 0
         today_sales = 0
         total_income = 0
         total_sales = 0
         total_items = len(json.loads(data_admin.items_json))
         total_users = len(data_cart)
         if len(today_data_sales) > 0:
            for i in range(len(today_data_sales)):
               sales_obj = json.loads(today_data_sales[i].sales)
               for j in range(len(sales_obj)):
                  today_income += sales_obj[j][2]*sales_obj[j][3]
                  today_sales += sales_obj[j][2]
         if len(total_data_sales) > 0: 
            for i in range(len(total_data_sales)):
               sales_obj = json.loads(total_data_sales[i].sales)
               for j in range(len(sales_obj)):
                  total_income += sales_obj[j][2]*sales_obj[j][3]
                  total_sales += sales_obj[j][2]
         weekly_sales = []
         weekly_revenue = []
         weekly_sales_label = []
         for i in range(1,8):
            weekly_sales_query = ChatbotSale.objects.filter(date=TODAY_UNIX - ((7-i) * 86400))
            unix = datetime.datetime.fromtimestamp(TODAY_UNIX - ((7-i) * 86400))
            if len(weekly_sales_query) > 0:
               weekly_sales_temp = 0
               weekly_revenue_temp = 0
               for j in range(len(weekly_sales_query)):
                  sales_obj = json.loads(weekly_sales_query[j].sales)
                  for k in range(len(sales_obj)):
                     weekly_sales_temp += sales_obj[k][2]
                     weekly_revenue_temp += sales_obj[k][2]*sales_obj[k][3]
               weekly_sales += [weekly_sales_temp]
               weekly_revenue += [weekly_revenue_temp]
            else:
               weekly_sales += [0]
               weekly_revenue += [0]
            weekly_sales_label += [f'{unix.strftime("%b")} {unix.strftime("%d")} {unix.strftime("%Y")}']
         weekly_sales = json.dumps(weekly_sales)
         weekly_revenue = json.dumps(weekly_revenue)
         total_revenue = str(int(total_income))
         if len(total_revenue) == 6:
            total_revenue = f"Rp{total_revenue[0:3]}K"
         else:
            total_revenue = f"Rp{total_revenue[0:-6]}M" 
         return render(request,("dashboard.html"),{
            "username":request.session['user'],
            "source_code":SOURCE_CODE,
            "today_income":rupiah(today_income),
            "today_sales":"{:,.0f}".format(today_sales),
            "total_income":rupiah(total_income),
            "total_sales":"{:,.0f}".format(total_sales),
            "weekly_sales":weekly_sales,
            "weekly_sales_label":weekly_sales_label,
            "weekly_revenue":weekly_revenue,
            "total_items":total_items,
            "total_users":total_users,
            "total_revenue":total_revenue
            })
      else:
         response = HttpResponse(status=302)
         response['Location'] = '/admin/'
         return response
   else:
      response = HttpResponse(status=302)
      response['Location'] = '/admin/'
      return response

def database(request):
   if request.POST.get('type'):
      response = HttpResponse(status=302)
      if request.POST['type'] == "login" and request.POST.get('username') and request.POST.get('password'):
         query = ChatbotUser.objects.filter(username=request.POST['username'])
         if len(query) > 0:
            if sha512(request.POST['password'].encode('utf-8')).hexdigest() == query[0].password:
               request.session['user'] = request.POST['username']
               request.session['session'] = sha512(request.POST['password'].encode('utf-8')).hexdigest()
               response['Location'] = '/dashboard/'
            else:
               response['Location'] = "/admin/?e=i"
         else:
            response['Location'] = '/admin/?e=n'
      elif request.POST['type'] == "admin":
         exit()
      return response
   else:
      raise PermissionDenied()