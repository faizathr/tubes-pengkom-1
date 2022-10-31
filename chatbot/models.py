from django.db import models

class ChatbotUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    api_key = models.CharField(max_length=36, default=None, blank=True, null=True)
    telegram_token = models.TextField(default=None, blank=True, null=True)
    variables = models.TextField(default='{}')
    items_json = models.TextField(default='[]')
    notify_id = models.TextField(default='[]')

    def __str__(self):
        return self.username

class ChatbotCart(models.Model):
    username = models.CharField(max_length=100)
    items = models.TextField()

    def __str__(self):
        return self.username

class ChatbotSale(models.Model):
    username = models.CharField(max_length=100)
    sales = models.TextField()
    date = models.IntegerField()

    def __str__(self):
        return self.username