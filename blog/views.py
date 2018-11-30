from django.shortcuts import render
from django.http import HttpResponse
from .models import Article, Category, Banner, Link, Tag  # 要查询所有文章，需要把文章表从数据模型导入到views中
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger#导入分页插件包
def hello(request):
    return HttpResponse("欢迎使用Django！")
def indextest(request):
    #添加两个变量
    sitename='Django中文网'
    url='www.django.cn'
    #加一个列表
    list=[
        '开发前的准备',
        '项目需求分析',
        '数据库设计分析',
        '创建项目',
        '基础配置',
        '欢迎页面',
        '创建数据库模型',
    ]
    #加一个字典
    mydict={
        'name':'吴秀峰',
        'qq':'445813',
        'wx':'vipdjango',
        'email':'445813@qq.com',
    }
    #对Article进行声明并实例化，然后生成对象allarticle
    allarticle=Article.objects.all()
    #把查询到的对象，封装到上下文中
    #把两个变量封装到上下文里
    context={
        'sitename':sitename,
        'url':url,
        'list':list,#把list封装到context
        'mydict':mydict,#把mydict封装到上下文中
        'allarticle':allarticle,
    }
    #把上下文传递到模板里
    return render(request,'indextest.html',context)
#-------------------
#首页
def index(request):
    allcategory = Category.objects.all()  # 通过Category表查出所有分类
    banner=Banner.objects.filter(is_active=True)[0:4]#查询所有幻灯图数据，并进行切片
    tui=Article.objects.filter(tui__id=1)[:3]#查询推荐位ID为1的文章
    allarticle=Article.objects.all().order_by('-id')[0:10]
    hot=Article.objects.all().order_by('views')[:10]#通过浏览数进行排序
    remen=Article.objects.filter(tui__id=2)[:6]
    tags=Tag.objects.all()
    link=Link.objects.all()
    # 把查询出来的分类封装到上下文里
    context = {
        'allcategory': allcategory,
        'banner':banner,#把查询到的幻灯图数据封装到上下文
        'tui':tui,
        'allarticle':allarticle,
        'hot':hot,
        'remen':remen,
        'tags':tags,
        'link':link,
    }
    return render(request, 'index.html', context)  # 把上下文传到index.html页面

#列表页
def list(request,lid):
   list=Article.objects.filter(category_id=lid)#获取通过URL传进来的lid，然后筛选处对应的文章
   cname=Category.objects.get(id=lid)#获取当前文章的栏目名
   remen=Article.objects.filter(tui__id=2)[:6]#右侧的热门推荐
   allcategory=Category.objects.all()#导航素有分类
   tags=Tag.objects.all()#右侧所有文章标签

   page=request.GET.get('page')#在URL中获取当前页面数
   paginator=Paginator(list,5)#对查询到的数据对象list进行分页，设置超过5条数据就分页
   try:
       list=paginator.page(page)#获取当前页码记录
   except PageNotAnInteger:
       list=paginator.page(1)#如果用户数据的页码不是整数时，显示第1页的内容
   except EmptyPage:
       list=paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表中时，显示最后一页的内容

   return render(request,'list.html',locals())
#内容页
def show(request,sid):
    show=Article.objects.get(id=sid)#查询指定id的文章
    allcategory=Category.objects.all()#导航上的分类
    tags=Tag.objects.all()#右侧所有标签
    remen=Article.objects.filter(tui__id=2)[:6]#右侧热门推荐
    hot=Article.objects.all().order_by("?")[:10]#内容下面的您可能感兴趣的文章，随机推荐
    previous_blog=Article.objects.filter(created_time__gt=show.created_time,category=show.category.id).first()
    next_blog=Article.objects.filter(created_time__lt=show.created_time,category=show.category.id).last()
    show.views=show.views+1
    show.save()
    return render(request,'show.html',locals())
#标签页
def tag(request, tag):
    list=Article.objects.filter(tags__name=tag)#通过文章标签进行查询文章
    remen=Article.objects.filter(tui__id=2)[:6]
    allcategory=Category.objects.all()
    tname=Tag.objects.get(name=tag)#获取当前搜索的标签名
    page=request.GET.get('page')
    tags=Tag.objects.all()
    paginator=Paginator(list,5)
    try:
        list=paginator.page(page)#获取当前页码的记录
    except PageNotAnInteger:
        list=paginator.page(1)#如果用户输入的页码不是整数时，显示第一页的内容
    except EmptyPage:
        list=paginator.page(paginator.num_pages)#如果用户输入的页数不在系统的页码列表时，显示最后一页的内容
    return render(request,'tags.html',locals())


# 搜索页
def search(request):
    ss=request.GET.get('search')#获取搜索的关键词
    list=Article.objects.filter(title__icontains=ss)#获取到搜索关键词通过标题进行匹配
    remen=Article.objects.filter(tui__id=2)[:6]
    allcategory=Category.objects.all()
    page=request.GET.get('page')
    tags=Tag.objects.all()
    paginator=Paginator(list,10)
    try:
        list=paginator.page(page)#获取当前页码记录
    except PageNotAnInteger:
        list=paginator.page(1)#如果用户输入的页码不是整数，显示第一页的内容
    except EmptyPage:
        list=paginator.page(paginator.num_pages)#如果用户输入的页数不在系统页码列表中，显示最后一页的内容
    return render(request,'search.html',locals())

# 关于我们
def about(request):
    allcategory=Category.objects.all()
    return render(request,'page.html',locals())