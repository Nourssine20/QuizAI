from django.contrib import admin
from .models import Test,Response,UserFeedback
admin.site.register(Test)
admin.site.register(Response)
# Register your models here.
admin.site.register(UserFeedback)
