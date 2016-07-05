from django.shortcuts import render, redirect, get_object_or_404, render_to_response
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View
from xinlireading.forms import TestStudentForm, XLRAuthenticationForm, CustomUserCreationForm, EditProfileForm, DashboardForm, BookDetailForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Book, Activity, ReadingGroup, ReadingGroupMembership, UserFavoriteBook
from allauth.account.models import EmailAddress

# from django.conf import settings
import os
import uuid
from django.contrib import messages
import json

class TestCreateStudentView(View):
	template_name = 'xinlireading/test-crop-image.html'

	def get(self, request, *args, **kwargs):
		form = TestStudentForm()
		return render(request, self.template_name, { 'form': form })

# list of mobile User Agents
mobile_uas = [
	'w3c ','acs-','alav','alca','amoi','audi','avan','benq','bird','blac',
	'blaz','brew','cell','cldc','cmd-','dang','doco','eric','hipt','inno',
	'ipaq','java','jigs','kddi','keji','leno','lg-c','lg-d','lg-g','lge-',
	'maui','maxo','midp','mits','mmef','mobi','mot-','moto','mwbp','nec-',
	'newt','noki','oper','palm','pana','pant','phil','play','port','prox',
	'qwap','sage','sams','sany','sch-','sec-','send','seri','sgh-','shar',
	'sie-','siem','smal','smar','sony','sph-','symb','t-mo','teli','tim-',
	'tosh','tsm-','upg1','upsi','vk-v','voda','wap-','wapa','wapi','wapp',
	'wapr','webc','winw','winw','xda','xda-'
	]

mobile_ua_hints = [ 'SymbianOS', 'Opera Mini', 'iPhone' ]

def mobileBrowser(request):
	''' Super simple device detection, returns True for mobile devices '''

	mobile_browser = False
	ua = request.META['HTTP_USER_AGENT'].lower()[0:4]

	if (ua in mobile_uas):
		mobile_browser = True
	else:
		for hint in mobile_ua_hints:
			if request.META['HTTP_USER_AGENT'].find(hint) > 0:
				mobile_browser = True

	return mobile_browser

def test(request):
	return render(request, 'xinlireading/test.html', None);

# Create your views here.
def home(request):

	context = {
		'is_signup': True,
		'is_signin': True,
		'books': Book.objects.all(),
		'email_valid': True
	}
	return render(request, 'xinlireading/home.html', context)

def reset_password(request):
	print('reset_password');
	if request.method == "POST":
		print('POST');
		print(request);
		body_unicode = request.body.decode('utf-8')
		body_dic = json.loads(body_unicode)
		email = str(body_dic['email'])
		user = User.objects.filter(email=email).first()
		print(user);
		if user is not None:
			return HttpResponse('success');
		else:
			return HttpResponse('not found');

def invalid(request):
	return render(request, 'xinlireading/invalid.html', None)

def success(request):
	return render(request, 'xinlireading/success.html', None)

class SignupView(View):
	template_name = 'xinlireading/signup.html'
	def get(self, request, *args, **kwargs):
		context = {'is_signup': True }
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		username = request.POST.get('nickname')
		password = request.POST.get('password1')
		form = CustomUserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
			new_user.userprofile.name = request.POST.get('nickname')
			new_user.userprofile.save()
			login(request, new_user)
			return redirect('/account/dashboard/')
		context = {
					'is_signup': True,
					 'form': form
				}
		return render(request, self.template_name, context)

class SigninView(View):
	template_name = 'xinlireading/signin.html'
	context = {'is_signin': True }
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, self.context)

	def post(self, request, *args, **kwargs):
		body_unicode = request.body.decode('utf-8')
		body_dic = json.loads(body_unicode)
		username = str(body_dic['email'])
		password = str(body_dic['password'])
		remember_me = bool(body_dic['remember_me'])
		if remember_me:
			request.session.set_expiry(0)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
			return HttpResponse('success')
		else:
			return HttpResponse('用户名密码不匹配!')


class DashboardView(LoginRequiredMixin, View):
	template_name = 'xinlireading/dashboard.html'

	def get(self, request, *args, **kwargs):
		membership = ReadingGroupMembership.objects.filter(user=request.user)
		email_valid = EmailAddress.objects.filter(user=request.user, verified=True).exists()
		return render(request, self.template_name, {'membership': membership, 'email_valid': email_valid})

	# Logout
	def post(self, request, *args, **kwargs):
		logout(request)
		return redirect('/home/')


class EditProfileView(LoginRequiredMixin, View):
	login_url = "/account/signin/"
	template_name = "xinlireading/edit-profile.html"

	def get(self, request, *args, **kwargs):
		print('get EditProfileView');
		form = EditProfileForm(instance=request.user.userprofile)
		print(request.user.userprofile.intro);
		userprofile = request.user.userprofile;
		email_valid = EmailAddress.objects.filter(user=request.user, verified=True).exists()
		return render(request, self.template_name, { 'form': form, 'email_valid': email_valid })

	def post(self, request, *args, **kwargs):
		form = EditProfileForm(request.POST, instance=request.user.userprofile);
		if form.is_valid():
			form.save();
			return HttpResponse('Success')
		return HttpResponse('Faild');

# Upload image file.
def upload(request):
	if request.method == 'POST':
		username = request.POST['username']
		file = request.FILES['file']
		newFilename = "{}.{}".format(uuid.uuid4(), 'png')
		newFilePath = "{}/{}/{}".format('avatar',request.user.id, newFilename)
		path = default_storage.save(newFilePath, ContentFile(file.read()))
		return HttpResponse(newFilePath)
	else:
		return HttpResponse('GET')

class BaseHeaderView(View):
	template_name = "xinlireading/base-header.html"
	def get(self, request, *args, **kwargs):
		form = BaseHeaderForm(instance=request.user.userprofile)
		return render(request, self.template_name, {'form': form})

class BooksView(LoginRequiredMixin, View):
	template_name = "xinlireading/books.html"
	def get(self, request, *args, **kwargs):
		# print(kwargs);
		print(request.path);
		if request.path == '/books/':
			books = Book.objects.all()
		elif request.path == '/reading/books/':
			favoriteBooks = Book.objects.filter(userfavoritebook__user=request.user)
			readingBooks = Book.objects.filter(activitys__readinggroup__readinggroupmembership__user=request.user)
			books = favoriteBooks|readingBooks


		email_valid = EmailAddress.objects.filter(user=request.user, verified=True).exists()
		return render(request, self.template_name, { 'books': books, 'email_valid': email_valid })

class BookDetailView(LoginRequiredMixin, View):
	template_name = "xinlireading/book-detail.html"
	def get(self, request, *args, **kwargs):
		book_id = self.kwargs['book_id']
		book = get_object_or_404(Book, pk=book_id)
		userFavoriteBook = UserFavoriteBook.objects.filter(book=book,user__id=request.user.id).first()
		isFavorite = 0 if userFavoriteBook == None else 1
		email_valid = EmailAddress.objects.filter(user=request.user, verified=True).exists()
		return render(request, self.template_name, { 'book': book, 'isFavorite': isFavorite, 'email_valid': email_valid })

	def post(self, request, *args, **kwargs):
		body_unicode = request.body.decode('utf-8')
		body_dic = json.loads(body_unicode)
		# print(body_dic['favorite'])
		favorite = bool(body_dic['favorite'])
		print(favorite)
		book_id = self.kwargs['book_id']
		book = get_object_or_404(Book, pk=book_id)
		if favorite:
			userFavoriteBook = UserFavoriteBook(book=book, user=request.user)
			userFavoriteBook.save()
		else:
			print('delete')
			UserFavoriteBook.objects.filter(book=book, user=request.user).first().delete()

		return HttpResponse('success')

class ActivitySignView(View):
	template_name = "xinlireading/activity-sign.html"
	def get(self, request, *args, **kwargs):
		# book_id = self.kwargs['book_id']
		# book = get_object_or_404(Book, pk=book_id)
		activity_id = self.kwargs['activity_id']
		membership = ReadingGroupMembership.objects.filter(user=request.user, reading_group__activity__id=activity_id).first()
		print(membership)
		email_valid = EmailAddress.objects.filter(user=request.user, verified=True).exists()
		return render(request, self.template_name, { 'membership': membership, 'email_valid': email_valid })

	def post(self, request, *args, **kwargs):
		activity_id = self.kwargs['activity_id']
		print(activity_id)
		group = ReadingGroup.objects.filter(activity__id=activity_id, opening=True).first()
		if group == None:
			return HttpResponse('没有可加入的群组!', status=500)

		if ReadingGroupMembership.objects.filter(user=request.user, reading_group=group).count() > 0:
			return HttpResponse('不可重复报名!', status=500)

		readingGroupMembership = ReadingGroupMembership(reading_group=group, user=request.user)
		readingGroupMembership.save()
		return HttpResponse('报名成功!', status=201)

		# return render_to_response(self.template_name, None)


from allauth.account.views import LoginView
from allauth.account.forms import LoginForm, ResetPasswordForm
class JointLoginResetPasswordView(LoginView):
	form_class = LoginForm
	# reset_password_form = ResetPasswordForm

	def __init__(self, **kwargs):
		super(JointLoginResetPasswordView, self).__init__(*kwargs)

	def get_context_data(self, **kwargs):
		context = super(JointLoginResetPasswordView, self).get_context_data(**kwargs)
		# context['resetpasswordform'] = get_form_class(app_settings.FORMS, 'resetpassword', self.reset_password_form)
		context['reset_password_form'] = ResetPasswordForm()
		context['is_signin'] = 'yes'
		return context

class SettingsAccountView(LoginRequiredMixin, View):
	""" Account settings """
	template_name = "xinlireading/settings-account.html"
	def get(self, request, *args, **kwargs):
		email_valid = EmailAddress.objects.filter(user=request.user, verified=True).exists()
		return render(request, self.template_name, { 'email_valid': email_valid })
