"""
URL configuration for it_company_task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from task_manager.views import LoginView

urlpatterns = [
	path("admin/", admin.site.urls),
	path("", include("task_manager.urls", "task_manager")),
	path("accounts/login/", LoginView.as_view(), name="login"),
	path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
	from django.conf.urls.static import static

	from debug_toolbar.toolbar import debug_toolbar_urls

	urlpatterns += static(
		settings.STATIC_URL, document_root=settings.STATIC_ROOT
	)

	urlpatterns += debug_toolbar_urls()
