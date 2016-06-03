from django.db import models
from django.contrib.auth.models import User

# 书籍
class Book(models.Model):
	type = models.IntegerField()
	title = models.CharField(max_length=200)

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
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	start_date = models.DateTimeField()
	duration = models.IntegerField()

	def __str__(self):
		return self.book.title + str(self.start_date)

# 会员
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	is_activated = models.BooleanField()
	# name = models.CharField(max_length=50)
	avatar = models.ImageField(blank=True)

	def __str__(self):
		return self.user.username

# 读书群
class ReadingGroup(models.Model):
	activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	members = models.ManyToManyField(
		User,
		through = 'ReadingGroupMembership',
		through_fields=('reading_group', 'user'),
	)

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
