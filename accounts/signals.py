# # -*- coding: utf-8 -*-
# from django.contrib.auth import user_logged_in, user_logged_out
# from django.dispatch import receiver
# from accounts.models import UserInfo
#
#
#
# @receiver(user_logged_in)
# def on_user_login(sender, **kwargs):
#     UserInfo.objects.get_or_create(username=kwargs.get("username"))