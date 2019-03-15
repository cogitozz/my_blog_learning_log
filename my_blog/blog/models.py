from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):  # 创建一个类继承Model—定义模型基本功能
    """用户学习的主题"""

# Topic 类只有两个属性：text 和date_added 。
    text = models.CharField(max_length=200)     # 属性text是一个CharField——由字符或文本组成的数据。需要存储少量的文本,
                                            # 定义CharField 属性时，必须告诉Django 该在数据库中预留多少空间
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, models.CASCADE)
    def __str__(self):      # 告诉Django，默认应使用哪个属性来显示有关主题的信息。
        """返回模型的字符串表示"""
        return self.text

# 这个模型是基于上面的Topic模型创建的条目模型
class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    topic = models.ForeignKey(Topic, models.CASCADE)    # 属性topic 是一个ForeignKey 实例。外键是一个数据库术语，它引用了数据库中的另一条记
                                        # 录；这些代码将每个条目关联到特定的主题。关于Foreignkey()的参数说明：https://blog.csdn.net/learnpy3/article/details/79387945
    text = models.TextField()   # 属性text ，它是一个TextField 实例。这种字段不需要长度限制
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:     # 在Entry 类中嵌套了Meta 类。Meta 存储用于管理模型的额外信息，在这里，它让我们能够设置一个特殊属性，让Django在需要时使用Entries 来表示多个条
                    # 目。如果没有这个类， Django将使用Entrys来表示多个条目。
        verbose_name_plural = 'entries'

    def __str__(self):
        """返回模型的字符串表示"""
        return self.text[:50] + "..."   # 让Django只显示text 的前50个字符










