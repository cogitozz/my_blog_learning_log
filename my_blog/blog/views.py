from django.shortcuts import render
from .models import Topic, Entry
from django.http import HttpResponseRedirect, Http404  # 用户提交主题后我们将使用这个类将用户重定向到网页topics
from django.urls import reverse
from .forms import TopicForm, EntryForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    """学习笔记的主页"""
    return render(request, 'blog/index.html')

@login_required
def topics(request):
    """显示所有的主题"""
    # topics = Topic.objects.order_by('date_added')
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    context = {'topics': topics}
    return render(request, 'blog/topics.html', context)

@login_required
def topic(request, topic_id):
    """显示单个主题及其所有的条目"""
    topic = Topic.objects.get(id=topic_id)

    # 确认请求的主题属于当前用户
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'blog/topic.html', context)

@login_required
def new_topic(request):
    """用户添加新主题"""
    if request.method != 'POST':
        # 未提交数据：创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)  # 使用用户输入的数据（它们存储在request.POST 中）创建一个TopicForm 实例
        if form.is_valid():     # 。函数is_valid() 核实用户填写了所有必不可少的字段（表单字段默认都是必不可少的），且输入的数据与要求的字段类型一致

            new_topic = form.save(commit=False)
            new_topic.owner = request.user  # 这两行用于解决保护用户主题之后出现的添加新主题出错

            form.save()     # 将提交的信息保存到数据库
            return HttpResponseRedirect(reverse('blog:topics'))
    context = {'form': form}        #  通过上下文字典将表单发送给模板
    return render(request, 'blog/new_topic.html', context)

@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # 未提交数据，创建一个空表单
        form = EntryForm()
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)     # 让Django创建一个新的条目对象，并将其存储到new_entry 中，但不将它保存到数据库中。
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(reverse('blog:topic', args=[topic_id]))    # 我们将用户重定向到显示相关主题的页面。
    context = {'topic': topic, 'form': form}
    return render(request, 'blog/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
    """编辑既有的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)    # 这个实参让Django创建一个表单，并使用既有条目对象中的信息填充它。用户将看到既有的数据，并能够编辑它们。
    else:
        # POST提交的数据，对数据进行处理
        form = EntryForm(instance=entry, data=request.POST)     # Django根据既有条目对象创建一个表单实例，并根据request.POST 中的相关数据对其进行修改。
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blog:topic',args=[topic.id]))
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'blog/edit_entry.html', context)















