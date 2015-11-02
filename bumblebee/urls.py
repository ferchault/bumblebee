# django imports
from django.conf.urls import include, url

# app-specific imports
import results.views as views

urlpatterns = [
	url(r'^results/', include('results.urls'))
]