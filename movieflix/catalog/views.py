from django.shortcuts import render
# Create your views here.
from catalog.forms import RegisterForm
import random
from catalog.models import Movies, Users, Ratings
from django.http import HttpResponseRedirect
from catalog import output
import datetime
import json
from catalog.ratingFiltering import wrdf
from catalog.ratingFiltering import collaborative
from django.views.decorators.cache import cache_page



from django.views.generic import DetailView


latest = ''
genres = ''
top = ''
topgenres = ''
logged = ''
'''
@cache_page(60 * 30)
def findlatest(request):
	latest = Movies.objects.order_by('-release_dat')[:20]
	genres = {}
	for i in range(20):
		genres[i] = ''
		for j in json.loads((latest[i].genres).replace("\'", "\"")) :
			genres[i] = genres[i] + " "+ j["name"]
#		for j in latest[i].genres.strip('][').split(','):
#			print(eval(j))
#			context["genres"][i] = context["genres"][i] + json.loads(j)["name"] 
	return latest, genres'''


def history(request, username):
	uid = Users.objects.filter(username=username).first()
	hist = Ratings.objects.filter(userid = uid.id)
	context = {}
	context["history"] = []
	context["logged"] = username
	for i in range(len(hist)):
		histmovies = Movies.objects.filter(id = hist[i].movieid).first()
		context["history"].append(histmovies)
	#histmovies = Movies.objects.filter(id = hist.movieid)
	#context["history"] = hist
	return render(request, "history.html", context) 

def modhistory(request, username, movie):
	uid = Users.objects.filter(username=username).first()
	hist = Ratings.objects.filter(userid = uid.id)
	context = {}
	context["history"] = []
	for i in range(len(hist)):
		histmovies = Movies.objects.filter(id = hist[i].movieid).first()
		context["history"].append(histmovies)
	#histmovies = Movies.objects.filter(id = hist.movieid)
	#context["history"] = hist
	return render(request, "history.html", context) 

@cache_page(60 * 15)
def index(request):
	global latest
	global genres
	global topgenres
	global top
	latest = Movies.objects.order_by('-release_dat')[:20]
	context = {}
	context["latest"] = latest 
	context["genres"] = {}
	for i in range(20):
		context["genres"][i] = ''
		for j in json.loads((latest[i].genres).replace("\'", "\"")) :
			context["genres"][i] = context["genres"][i] + " "+ j["name"]
#		for j in latest[i].genres.strip('][').split(','):
#			print(eval(j))
#			context["genres"][i] = context["genres"][i] + json.loads(j)["name"] 
	genres = context["genres"]
#	for i in range(20):
#		for j in latest[i].genres:
#			context["genres"][i] .append(json.loads(j)['name'])
	lis = wrdf().head(16)
	top = lis.values.tolist()
	context["top"] = top
	context["topgenres"] = {}
	for i in range(len(top)):
		context["topgenres"][i] = ''
		for j in json.loads((top[i][3]).replace("\'", "\"")) :
			context["topgenres"][i] = context["topgenres"][i] + " "+ j["name"]
	topgenres = context["topgenres"]
	#request.session['maincontext'] ={"top" :str(top), "latest" : str(latest), "genres": str(context["genres"]), "topgenres": str(context["topgenres"])}
	return render(request, 'index.html', context)
'''
class mainPage(DetailView):
	model = Movies
	template_name = 'index.html'
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['latest'] = Movies.objects.order_by('-release_dat')[:4]
		return context'''

def withRecom(request, username):

	#latestUpdate = Ratings.objects.order_by('-timestamp')[:1]
	latest = Movies.objects.order_by('-release_dat')[:20]
	context = {}
	context["recommendations"] = ""
	context["latest"] = latest 
	context["genres"] = {}
	for i in range(20):
		context["genres"][i] = ''
		for j in json.loads((latest[i].genres).replace("\'", "\"")) :
			context["genres"][i] = context["genres"][i] + " "+ j["name"]
#		for j in latest[i].genres.strip('][').split(','):
#			print(eval(j))
#			context["genres"][i] = context["genres"][i] + json.loads(j)["name"] 
	genres = context["genres"]
#	for i in range(20):
#		for j in latest[i].genres:
#			context["genres"][i] .append(json.loads(j)['name'])
	lis = wrdf().head(16)
	top = lis.values.tolist()
	context['user'] = logged
	context["top"] = top
	context["topgenres"] = {}
	for i in range(len(top)):
		context["topgenres"][i] = ''
		for j in json.loads((top[i][3]).replace("\'", "\"")) :
			context["topgenres"][i] = context["topgenres"][i] + " "+ j["name"]
	topgenres = context["topgenres"]
	print("------"+logged)
	loggedid = Users.objects.filter(username = username).first()
	print(loggedid)

	if str(loggedid.id) not in output.recommendations.keys():
		return context
	else:
		movs = output.recommendations[str(loggedid.id)]
		l =[]
		for i in movs:
			l.append(Movies.objects.get(id = i))


	#context['latest'] = request.session['maincontext']['latest']
	#context['latest'] = latest
	#context['genres'] = request.session['maincontext']['genres']
	#context['genres'] = genres
	#context['top'] = request.session['maincontext']['top']
	#context['top'] = top
	#context['topgenres'] = request.session['maincontext']['topgenres']
	#context['topgenres'] = topgenres
	context["recommendations"] = l
	#print(context['recommendations'])
	#context['user'] = request.session['user']
	
	return context



from django.views import generic
#@cache_page(60 * 30)
class moviesAll(generic.ListView):
	model = Movies
	context_object_name = 'movie_list'
	queryset = Movies.objects.all().order_by('title')[:1000]
	template_name = 'all.html'
'''
from catalog.forms import RegisterForm

class PostForm(ModelForm):
	class Meta:
		model = Users

		fields = ["username", "email", "password"]

		def clean(self):
			super(PostForm, self).clean()

			username = self.cleaned_data.get('username')
			password = self.cleaned_data.get('password')
			email = self.cleaned_data.get('email')

			if len(username) < 3 :
				self.errors['username'] =self.error_class([''])


def register(request):
	username = "not logged in"

	if request.method == "POST":
		reg = RegisterForm(request.POST)

		if RegisterForm.is_valid():
			username = RegisterForm.cleaned_data['username']

	return render(request,"signin.html", {"username" : username})'''

'''
from catalog.forms import RegisterForm

def signup(request):
	username = ''
	password1 = ''
	password2 = ''
	email = ''

	form = RegisterForm(request.POST or None)
	if form.is_valid():
		fs = form.save(commit = False)
		username = form.cleaned_data.get("username")
		password1 = form.cleaned_data.get("password1")
		password2 = form.cleaned_data.get("password2")
		email = form.cleaned_data.get("email")

		if password1 == password2:
			try:
				user = Users.objects.get(email = email)
				context = {'form':form, 'error':'The email id you entered already has an account.'}
				return render(request, 'index.html', context) 
			except Users.DoesNotExist:
				user = Users.objects.create_user(username, password = password1, email = email)

				user.save()
				login(request,user)

				fs.user = request.user

				fs.save()
				context = {'form': form}
				return render(request, 'signed.html', context)

		else:
			context = {'form': form, 'error': 'The passwords do not match.'}
			return render(request, 'index.html', context)

	else:
		context = {'form':form}
		return render(request, 'index.html', context)'''

def signup(request):
	print("form is submitted")
	#if request.method == 'POST':
	#	form = RegisterForm(response.POST)
	username = request.POST["username"]
	email = request.POST["email"]
	password = request.POST["password"]
	#if form.is_valid():

	try:
		check = Users.objects.get(email = email)
		context = {'email': email,'error':'The email id you entered already has an account.'}
		return render(request, 'index.html', context)
	except Users.DoesNotExist:
		users = Users(username = username, password = password, email = email)
		users.save()
		#context = {'error': '', 'username': username, 'email': email}
		#return render(request, 'signed.html', context)
		request.session['user'] = email
		#context = withRecom(request, username)
		#ur = "http://127.0.0.1:8000/catelog/" + username
		#return HttpResponseRedirect(ur, context)
		return HttpResponseRedirect("http://127.0.0.1:8000/catelog/")


from catalog.forms import RegisterForm
#@cache_page(60 * 30)
def login(request):
	global logged
	email = request.POST['email']
	password = request.POST['password']
	form = RegisterForm(request.POST)
	username = Users.objects.filter(email=email).first().username
	if form.is_valid():
		#context = {'error': '', 'email':email}
		#request.session['user'] = email
		logged = email
		context = withRecom(request, username)
		ur = "http://127.0.0.1:8000/catelog/" + username
		return HttpResponseRedirect(ur, context)
		#added_user(request, username)
	else:
		context = {'error':'Entered email or password is incorrect.', 'email':email}
		return render(request, 'index.html', context)

def usingle(request,username, movie):
	#print(movie)
	details = Movies.objects.filter(title = movie).first()
	print(request.user)
	uid = Users.objects.filter(username = username).first()
	rate = Ratings.objects.filter(movieid = details.id, userid = uid.id).first()
	context = {}
	context["ratings"] = ""
	if rate!=None:
		context["ratings"] = rate.rating
	print(details)
	#print(rate.rating)

	context["genres"] = ""
	for j in json.loads((details.genres).replace("\'", "\"")) :
			context["genres"] = context["genres"] + " "+ j["name"]

	context["cast"] = ""
	#for j in json.loads((details.cast).replace("\'", "\"")) :
	#		context["crew"] = context["crew"] + " "+ j["name"]

	context["details"] = details
	print(details.title)


	return render(request, 'usingle.html', context)

#@cache_page(60 * 30)
def added_user(request, username):
	#print("---"+request.user.id)
	context = withRecom(request, username)
	print(context["latest"])
	return render(request, "signed.html", context)

def news(request):
	return render(request, "news.html")

def rate(request, username, movie):
	rating = request.POST["quantity"]
	uid = Users.objects.filter(username = username).first()
	mid = Movies.objects.filter(title=movie).first()
	r = Ratings(movieid = mid.id, userid = uid.id, rating = rating)
	r.save()
	collaborative()
	ur = "http://127.0.0.1:8000/catelog/" + username + "/" + movie
	return HttpResponseRedirect(ur)










