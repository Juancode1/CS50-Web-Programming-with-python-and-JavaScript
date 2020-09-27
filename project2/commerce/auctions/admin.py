from django.contrib import admin
from .models import listing,User,comments,bids,sold,watchlistM

# Register your models here.
admin.site.register(listing)
admin.site.register(User)
admin.site.register(comments)
admin.site.register(bids)
admin.site.register(sold)
admin.site.register(watchlistM)