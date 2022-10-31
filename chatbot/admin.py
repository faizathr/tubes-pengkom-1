from django.contrib import admin
from .models import ChatbotUser, ChatbotCart, ChatbotSale
admin.site.register(ChatbotUser)
admin.site.register(ChatbotCart)
admin.site.register(ChatbotSale)