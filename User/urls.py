from django.contrib import admin
from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.loginUser, name="login"),
	path('register/', views.register, name="register"),
      path('verify/<auth_token>', views.verify, name="verify"),
	path('logout/', views.logoutUser, name="logout"),

	path('', views.home, name="home"),

      path('details/<int:pk>/', views.details, name="details"),

      path('detailsTags/<int:pk>/<int:id>/<int:addressid>', views.addDetailsTags, name="detailsTags"),

      path('deleteTag/<int:pk>/<int:id>/<int:did>',views.deleteTag, name="deleteTag"),

      path('numberCheck/<int:pk>/<int:id>',views.numberCheck, name="numberCheck"),

	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="User/restPassword/restPassword.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="User/restPassword/passwordRestSend.html"),
          name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="User/restPassword/newPssword.html"),
          name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="User/restPassword/passwordResetComplete.html"),
          name="password_reset_complete"),

      path('fileUpload/', views.fileUpload, name="fileUpload"),
]
