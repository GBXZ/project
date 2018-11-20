from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View
from myblog import models
from django.core.paginator import Paginator
from django.contrib.syndication.views import Feed

import markdown
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger


# 主页
class Index(View):
	def get(self, request):
		post_list = models.Post.objects.all().order_by('-create_time')
		# 查询出归档日期的文章
		year = request.GET.get('year', '')
		month = request.GET.get('month', '')
		category = request.GET.get('category', '')
		tag = request.GET.get('tag', '')
		if year and month:
			post_list = models.Post.objects.filter(create_time__year=int(year), create_time__month=int(month)) \
				.order_by('-create_time')
		# 查询出分类的文章
		if category:
			post_list = models.Post.objects.filter(category__name=category)
		if tag:
			post_list = models.Post.objects.filter(tags=tag)
		# 使用pure_pagination 进行分页代码
		try:
			page = request.GET.get('page', 1)
		except:
			page = 1
		p = Paginator(post_list, 3, request=request)   # 中间的1 是每页显示的数量
		posts = p.page(page)
		# 查询出总共页数
		p = Paginator(post_list, 3)
		page_total = p.num_pages

		# 使用 django pagintor 进行分页代码
		# page_num = int(request.GET.get('page', 1))
		# p = Paginator(post_list, 1)
		# if int(page_num) == 1:
		# 	x = 1
		# else:
		# 	x = int(page_num)
		# 	x = x - 1
		# if page_num == p.num_pages:
		# 	y = int(p.num_pages)
		# else:
		# 	y = int(page_num)
		# 	y = y+1
		# page_total = p.num_pages
		# post_list = p.page(1)
		return render(request, 'myblog/index.html', locals())

	def post(self, request):
		search_feild = request.POST.get('search', '')
		post_list = models.Post.objects.filter(title__icontains=search_feild)
		try:
			page = request.GET.get('page', 1)
		except:
			page = 1
		p = Paginator(post_list, 3, request=request)  # 中间的1 是每页显示的数量
		posts = p.page(page)
		# 查询出总共页数
		p = Paginator(post_list, 3)
		page_total = p.num_pages
		return render(request, 'myblog/index.html', locals())


# 文章详细信息
class Detail(View):
	def get(self, request, pk):
		# get_object_or_404 有两个参数，第一个是查询源，第二个条件，如果查询为空返回404页面
		post = get_object_or_404(models.Post, id=pk)
		# markdown标记语言
		# post.body = markdown.markdown(post.body, extensions=[
		# 	'markdown.extensions.extra',
		# 	'markdown.extensions.codehilite',
		# 	'markdown.extensions.toc',
		# ])
		comments = models.Comment.objects.filter(post_id=int(pk))
		# 标记语言以及生成目录列表
		md = markdown.Markdown(extensions=[
			'markdown.extensions.extra',
			'markdown.extensions.codehilite',
			'markdown.extensions.toc',
		])
		post.body = md.convert(post.body)
		toc = md.toc
		# post.increase_views用来自增长阅读量
		post.increase_views()
		return render(request, 'myblog/single.html', locals())

	def post(self, request, pk):
		search_field = request.POST.get('search', '')
		post_list = models.Post.objects.filter(title__icontains=search_field)
		if search_field:
			try:
				page = request.GET.get('page', 1)
			except:
				page = 1
			p = Paginator(post_list, 3, request=request)  # 中间的1 是每页显示的数量
			posts = p.page(page)
			# 查询出总共页数
			p = Paginator(post_list, 3)
			page_total = p.num_pages
			return render(request, 'myblog/index.html', locals())
		else:
			name = request.POST.get('name', '')
			email = request.POST.get('email', '')
			url = request.POST.get('url', '')
			comment = request.POST.get('comment', '')
			new_comment = models.Comment()
			new_comment.post_id = int(pk)
			new_comment.name = name
			new_comment.email = email
			new_comment.personal_website = url
			new_comment.comment = comment
			new_comment.save()
			return redirect('/myblog/detail/{0}'.format(pk))


# 归档显示
# class Archives(View):
# 	def get(self, request):
# 		year = request.GET.get('year', '')
# 		month = request.GET.get('month', '')
# 		# 条件查询出某年某月的文章
# 		post_list = models.Post.objects.filter(create_time__year=int(year), create_time__month=int(month ))\
# 			.order_by('-create_time')
# 		return render(request, 'myblog/index.html', locals())

# Create your views here.
# class Search_post(View):
# 	def post(self):

class Formyself(View):
	pass


# RSS订阅
# class LastestEntries(Feed):
# 	title = 'GBXZ'
# 	link = '/myblog/'
