from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from ckeditor.fields import RichTextField
from django.utils import timezone

class TestStudent(models.Model):
	name =  models.CharField(max_length=100)
	GENDER_CHOICES = (
		('M', 'Male'),
		('F', 'Female'),
	)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M', null=True)

# 书籍类型
class BookType(models.Model):
	name = models.CharField(max_length=100)

	def __str__(self):
		return self.name

class Author(models.Model):
	name = models.CharField(max_length=200)
	intro = RichTextField(blank=True)

	def __str__(self):
		return self.name

# 书籍
class Book(models.Model):
	# type = models.IntegerField()
	type = models.ForeignKey(BookType, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	# author = models.CharField(max_length=200, blank=True)
	author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True)
	publisher = models.CharField(max_length=200, blank=True)
	publish_date = models.DateField(auto_now=False, auto_now_add=False)
	price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=0)
	intro = RichTextField(blank=True)
	cover = models.ImageField(blank=True)

	def __str__(self):
		return self.title

# 领读文章
class Article(models.Model):
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	content = models.TextField()

	def __str__(self):
		return self.title

# 评分
class Grade(models.Model):
	book = models.OneToOneField(Book, on_delete=models.CASCADE)
	reader_count = models.IntegerField(default=0)
	score = models.FloatField(default=0)

	def __str__(self):
		return self.book.title


# 读书活动
class Activity(models.Model):
	title = models.CharField(max_length=200, blank=True)
	intro = models.CharField(max_length=200, blank=True)
	book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="activitys")
	start_date = models.DateTimeField(default=timezone.now)
	duration = models.IntegerField()
	rule = RichTextField(blank=True)

	def __str__(self):
		# return self.book.title + str(self.start_date) + " " + self.title
		# return self.book.title + self.start_date.strftime("%Y-%m-%d %H:%M") + " " + self.title
		return self.book.title + " - " + self.title + " " + self.start_date.strftime("%Y-%m-%d")


# 会员
class UserProfile(models.Model):
	UNKNOWN = 'U'
	MALE = 'M'
	FEMALE = 'F'
	GENDER_CHOICES = (
	    (UNKNOWN, '请选择你的性别'),
	    (MALE, '男'),
	    (FEMALE, '女'),
	)
	YEAR_CHOICES = (
	    [(-1, '年')] + [(i, str(i)) for i in range(2016, 1900, -1)]
	)
	MONTH_CHOICES = (
	    [(-1, '月')] + [(i, str(i)) for i in range(1, 13)]
	)
	DAY_CHOICES = (
	    [(-1, '日')] + [(i, str(i)) for i in range(1, 32)]
	)
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_activated = models.BooleanField(default=False)
	name = models.CharField(max_length=100)
	avatar_url = models.CharField(max_length=200, null=True, blank=True) #, default="avatar/avatar.png"
	intro = models.CharField(max_length=200, null=True, blank=True)
	gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
	address_country = models.CharField(max_length=200)
	address_city = models.CharField(max_length=200)
	birth_year = models.IntegerField(default=-1, choices=YEAR_CHOICES)
	birth_month = models.IntegerField(default=-1, choices=MONTH_CHOICES)
	birth_day = models.IntegerField(default=-1, choices=DAY_CHOICES)

	def __str__(self):
		return self.user.username + ' ' + self.name

# 读书群
class ReadingGroup(models.Model):
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(
		User,
		through = 'ReadingGroupMembership',
		through_fields=('reading_group', 'user'),
	)
	wechatGroupImage = models.ImageField(blank=True)
	opening = models.BooleanField(default=True)

	def __str__(self):
		return self.name

# 读书群会员资格 Group-User
class ReadingGroupMembership(models.Model):
	reading_group = models.ForeignKey(ReadingGroup, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.reading_group.name + ": " + self.user.username

# 读书笔记
class Note(models.Model):
	reading_group_membership = models.ForeignKey(ReadingGroupMembership, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	content = models.TextField()

	def __str__(self):
		return self.title

# 用户收藏书籍 User-Book
class UserFavoriteBook(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)

	def __str__(self):
		 return self.book.title + ": " + self.user.username
