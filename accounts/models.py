# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, Permission
from djcelery.compat import python_2_unicode_compatible
# Create your models here.


@python_2_unicode_compatible
class PermissionList(models.Model):
    name = models.CharField(max_length=64)
    url = models.CharField(max_length=255)

    # def __unicode__(self):
    #     return '%s(%s)' % (self.name, self.url)

    def __str__(self):
        return '%s(%s)' % (self.name, self.url)


@python_2_unicode_compatible
class RoleList(models.Model):
    name = models.CharField(max_length=64)
    # 如果关联的model定义在前面可以直接引用(如 PermissionList),
    # 否则 需要填写未定义模块的名字(如 'PermissionList')
    permission = models.ManyToManyField(PermissionList, blank=True)

    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return self.name


class UserManger(BaseUserManager):
    def create_user(self, email, username, password=None):
        '''创建普通用户'''
        if not email:
            raise ValueError(u'邮件不能为空!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        '''创建超级用户'''
        user = self.create_user(email, username=username, password=password)
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserInfo(AbstractBaseUser):
    '''用户信息'''
    username = models.CharField(max_length=64, unique=True, db_index=True)
    email = models.EmailField(max_length=255)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    nickname = models.CharField(max_length=64, null=True)
    role = models.ForeignKey(RoleList, null=True, blank=True, on_delete=models.SET_NULL)
    objects = UserManger()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def has_perm(self, perm, obj=None):
        if self.is_active and self.is_superuser:
            return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        '''The user is identified by their email address'''
        return self.email

    def get_short_name(self):
        '''The user is identified by their email address'''
        return self.email

    @property
    def is_staff(self):
        '''Is the user a member of staff'''
        return self.is_superuser

