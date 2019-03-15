from django import forms
from .models import Topic       # 首先导入了模块forms 以及要使用的模型Topic
from .models import Entry

class TopicForm(forms.ModelForm):
    class Meta:     # 最简单的ModelForm 版本只包含一个内嵌的Meta 类，它告诉Django根据哪个模型创建表单，以及在表单中包含哪些字段。
        model = Topic   # 我们根据模型Topic 创建一个表单，该表单只包含字段text
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}












