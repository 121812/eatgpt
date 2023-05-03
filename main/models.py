from django.db import models

# Create your models here.
class DailyFood(models.Model):
    ip = models.CharField(max_length=255, verbose_name='ip地址')
    date = models.CharField(max_length=255, verbose_name='日期')
    food_dict = models.CharField(max_length=1024, verbose_name='数据')
    raw = models.CharField(max_length=1024, verbose_name='原始数据')
    
    class Meta():
        db_table = 't_daily_food'
        verbose_name = 'IP食物每日缓存表'
        ordering = ["date"]
