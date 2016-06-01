from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader, RequestContext
from django.views.generic import View
from xinlireading.forms import SignupForm, SigninForm
from django.contrib.auth import authenticate, login

# import pdb; pdb.set_trace()

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

# Create your views here.
def home(request):
	context = {
		'is_signup': True,
		'is_signin': True
	}
	return render(request, 'xinlireading/home.html', context)

def invalid(request):
	context = {
		'a': 1
	}
	return render(request, 'xinlireading/invalid.html', context)

def success(request):
	context = {
		'a': 2
	}
	return render(request, 'xinlireading/success.html', context)

# def signup(request):
# 	context = {'is_signup': True }
# 	return render(request, 'xinlireading/signup.html', context)
class SignupView(View):
	template_name = 'xinlireading/signup.html'
	context = {'is_signup': True }
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, self.context)

	def post(self, request, *args, **kwargs):
		form = SignupView(request.POST)
		if form.is_valid():
			return redirect('/dashboard/')
		return render(request, self.template_name, {'form': form})

# def signin(request):
# 	context = {'is_signin': True }
# 	return render(request, 'xinlireading/signin.html', context)
class SigninView(View):
	template_name = 'xinlireading/signin.html'
	context = {'is_signin': True }
	def get(self, request, *args, **kwargs):
		return render(request, self.template_name, self.context)

	def post(self, request, *args, **kwargs):

		# Method 1:
		form = SigninForm(request.POST)
		print(form)
		if form.is_valid():
			return redirect('/success/')
		return redirect('/invalid/')

		# Method 2:
		username = request.POST.get('username')
		password = request.POST.get('password')
		print(username + ':' +password)
		user = authenticate(username=username, password=password)
		print(user)
		if user is not None:
			login(request, user)
			return redirect('/success/')
		else:
			return redirect('/invalid/')
