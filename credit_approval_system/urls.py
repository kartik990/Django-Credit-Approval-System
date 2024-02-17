from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('credit-approval/', include('credit_approval.urls')),
]
