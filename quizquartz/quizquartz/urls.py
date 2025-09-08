"""
URL configuration for quizapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from django.urls import path, include
from django.contrib import admin
from pathlib import Path
import environ


BASE_DIR = Path(__file__).resolve().parent.parent
DOTENV_PATH = BASE_DIR / ".env"

env = environ.Env()
environ.Env.read_env(DOTENV_PATH)

urlpatterns = [
    path(route=env("ADMIN_ROUTE"), view=admin.site.urls),  # Admin route is secret.
    path(route="auth-api/", view=include("accounts.urls")),
    path(route="quiz-api/", view=include("quizzes.urls")),
]
