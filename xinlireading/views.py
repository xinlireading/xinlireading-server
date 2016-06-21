from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View
from xinlireading.forms import TestStudentForm, XLRAuthenticationForm, CustomUserCreationForm, EditProfileForm, DashboardForm, BookDetailForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from .models import Book
# from django.conf import settings
import os
import uuid


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
		'is_signin': True
	}
	return render(request, 'xinlireading/home.html', context)

def invalid(request):
	return render(request, 'xinlireading/invalid.html', None)

def success(request):
	return render(request, 'xinlireading/success.html', None)

# def signup(request):
#	 context = {'is_signup': True }
#	 return render(request, 'xinlireading/signup.html', context)
class SignupView(View):
	template_name = 'xinlireading/signup.html'
	def get(self, request, *args, **kwargs):
		context = {'is_signup': True }
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		print('post')
		username = request.POST.get('username')
		password = request.POST.get('password1')
		# print(username + ' password: ' + password)

		# form = XLRRegistrationForm(request.POST)
		form = CustomUserCreationForm(request.POST)
		print(form.errors)
		if form.is_valid():
			form.save()
			new_user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
			login(request, new_user)
			return redirect('/dashboard/')
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

		# Method 1:
		# form = SigninForm(request.POST)
		# print(form)
		# if form.is_valid():
		#	 return redirect('/success/')
		# return redirect('/invalid/')

		# Method 2:
		if not request.POST.get('remember_me', None):
			request.session.set_expiry(0)

		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)
			return redirect('/account/dashboard/')
		else:
			return redirect('/account/invalid/')

class DashboardView(LoginRequiredMixin, View):
	login_url = '/account/signin/'
	# redirect_field_name = 'redirect_to'
	template_name = 'xinlireading/dashboard.html'

	def get(self, request, *args, **kwargs):
		form = DashboardForm(instance=request.user.userprofile)
		return render(request, self.template_name, {'form': form})

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
		return render(request, self.template_name, { 'form': form })

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

class BookDetailView(View):
	template_name = "xinlireading/book-detail.html"
	def get(self, request, *args, **kwargs):
		book_id = self.kwargs['book_id']
		book = get_object_or_404(Book, pk=book_id)
		# form = BookDetailForm(instance=book)
		# print(form)
		# return render(request, self.template_name, {'form': form})
		return render(request, self.template_name, {'book': book})
