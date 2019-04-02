from django.db import models

# Create your models here.

class Role(models.Model):

    title = models.CharField(max_length=32,verbose_name='角色名称')
    permissions = models.ManyToManyField(to='Permission',verbose_name='角色权限')

    def __str__(self):
        return self.title

class UserInfo(models.Model):

    name = models.CharField(max_length=32,verbose_name='用户姓名')
    pwd = models.CharField(max_length=64,verbose_name='密码',default='')
    roles = models.ManyToManyField(to=Role,verbose_name='用户角色')

    def __str__(self):
        return self.name

    # class Meta:
    #     # django以后在数据迁移时不会再为其创建UserInfo表，但可以作为父类被其他类继承
    #     abstract = True

class Permission(models.Model):

    title = models.CharField(max_length=32,verbose_name='权限名称')
    urls = models.CharField(max_length=64,verbose_name='权限路径')
    name = models.CharField(verbose_name='URL别名',max_length=32,unique=True)
    menus = models.ForeignKey(to='Menu',verbose_name='一级菜单名称',help_text='null表示非菜单',on_delete=models.CASCADE,null=True)
    pid = models.ForeignKey(to='Permission',verbose_name='关联权限',null=True,blank=True,on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Menu(models.Model):

    title = models.CharField(verbose_name='菜单',max_length=32)
    icon = models.CharField(verbose_name='菜单图标',max_length=32)

    def __str__(self):
        return self.title
