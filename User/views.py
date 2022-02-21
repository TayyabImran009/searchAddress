from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import CutomUserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
import uuid
from .models import*
from django.conf import settings
from django.core.mail import send_mail
from django.db.models import Q
import requests
import json
from datetime import datetime
import csv
import codecs

# Create your views here.
def home(request):
	if request.method == 'POST':
		fname = request.POST['fname']
		lname = request.POST['lname']
		address = request.POST['address']
		city = request.POST['city']
		state = request.POST['state']
		zip = request.POST['zip']
		type = request.POST['type']
		if not request.user.is_authenticated:
			request.session['address'] = address
			request.session['city'] = city
			request.session['state'] = state
			request.session['zip'] = zip
			request.session['type'] = type
			return redirect('login')
		newAddress = userAddress(user=request.user, address=address, city=city, state=state, zip=zip, tag=type)
		newAddress.save()
	if request.user.is_authenticated:
		addressObj = userAddress.objects.filter(user=request.user)
		context = {
			'addressObj':addressObj
		}
		return render(request,'User/home.html',context)
	return render(request,'User/home.html')

def details(request, pk):
	useraddress = userAddress.objects.get(id=pk)
	oldDetails = userAddress.objects.filter(address=useraddress.address)
	addressDetailsTagsObj = addressDetailsTags.objects.all()
	detailsTagsObj = detailsTags.objects.filter(user=request.user)
	dataList = []
	addressDetailsObj = None
	context={}
	try:
		for data in oldDetails:
			if data.id != pk and (datetime.today().replace(tzinfo=None) - data.created_at.replace(tzinfo=None)).days < 7 and data.is_dataRetrived:
				dataList.append(data)
		for data in dataList:
			addressDetailsObj = addressDetails.objects.filter(address = data)

		context={
			'addressDetails':addressDetailsObj,
			'useraddress':useraddress,
			'addressDetailsTags':addressDetailsTagsObj,
			'detailsTagsObj':detailsTagsObj
		}
	except:
		print("no match found")
	if addressDetailsObj == None and useraddress.is_dataRetrived != True:
		try:	
			headers = {
			'x-api-key': 'test-d56ef9dd-00f4-4eab-af9b-284f0c81b0c0',
			}

			data = {
			"Key":"[ANY VALUE YOU WANT]",
			"FName":"",  # optional
			"LName":"",  # optional
			"Address1":useraddress.address,
			"City":useraddress.city,
			"State":useraddress.state,
			"Zip":useraddress.zip
			}
			print('https://api.skipengine.com/v2/service', headers, data)
			response = requests.post('https://api.skipengine.com/v2/service', headers=headers, data=data)
			j = response.json()
			filterData = j["Output"]["Identity"]["Phones"]
			for data in filterData:
				temp = addressDetails(number=data["Phone"], address=useraddress)
				temp.save()
			addressDetailsObj = addressDetails.objects.filter(address = useraddress)
			context={
				'addressDetails':addressDetailsObj,
				'useraddress':useraddress,
				'addressDetailsTags':addressDetailsTagsObj,
				'detailsTagsObj':detailsTagsObj
			}
			useraddress.is_dataRetrived = True
			useraddress.save()
		except:
			context={
				'useraddress':useraddress,
				'msg':"Invalid address",
				'addressDetailsTags':addressDetailsTagsObj,
				'detailsTagsObj':detailsTagsObj
			}
			return render(request,'User/details.html',context)
	if addressDetailsObj == None:
		addressDetailsObj = addressDetails.objects.filter(address = useraddress)
		context={
			'addressDetails':addressDetailsObj,
			'useraddress':useraddress,
			'addressDetailsTags':addressDetailsTagsObj,
			'detailsTagsObj':detailsTagsObj
		}
	return render(request,'User/details.html',context)

def addDetailsTags(request,pk,id,addressid):
	tagObj = addressDetailsTags.objects.get(id=pk)
	addressDetailObj = addressDetails.objects.get(id=id)
	try:
		detailsTagsObj = detailsTags.objects.get(user=request.user,addressDetails=addressDetailObj)
		detailsTagsObj.tags.add(tagObj)
		detailsTagsObj.save()
	except:
		detailsTagsObj = detailsTags.objects.create(user=request.user,addressDetails=addressDetailObj)
		detailsTagsObj.tags.add(tagObj)
		detailsTagsObj.save()
	return redirect('details',addressid)

def numberCheck(request,pk,id):
	addressDetailsObj = addressDetails.objects.get(id=pk)
	if request.user in addressDetailsObj.numberChecked.all():
		addressDetailsObj.numberChecked.remove(request.user)
	else:
		addressDetailsObj.numberChecked.add(request.user)
	
	return redirect('details',id)

def loginUser(request):

	if request.user.is_authenticated:
		return redirect('home')
	msg = None
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		try:
			user = User.objects.get(username=username)
			user = authenticate(request, username=username, password=password) # check password

			if user is not None and accountsCheck.objects.get(user=user).is_verified:
				login(request, user)
				if 'address' in request.session:
					newAddress = userAddress(user=request.user, address=request.session['address'], city=request.session['city'], state=request.session['state'], zip=request.session['zip'], tag=request.session['type'])
					del request.session['address']
					del request.session['city']
					del request.session['state']
					del request.session['zip']
					del request.session['type']
					newAddress.save()
				return redirect('home')
			else:
				msg = 'User/Something is wrong'
		except:
			msg = 'User not recognized.'
	context = {
		'msg':msg
	}
	return render(request,'User/login.html',context)

def register(request):
	msg = None
	form = CutomUserCreationForm
	if request.method == 'POST':
		form = CutomUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			# user.username = user.username.lower()
			user.save()

			auth_token = str(uuid.uuid4())
			accountsCheck_obj = accountsCheck.objects.create(user=user, auth_token = auth_token)
			accountsCheck_obj.save()

			verificationMain(user.email,auth_token,request)

			msg = 'Verifecation Link has been send to your mail. Kindly verify it.'
			context = {'form':form, 'msg':msg}
			return render(request,'User/register.html', context)
		else:
			msg = 'Error.'
	context = {'form':form, 'msg':msg}
	return render(request,'User/register.html', context)

def verify(request, auth_token):
	accountsCheck_obj = accountsCheck.objects.get(auth_token = auth_token)
	if accountsCheck:
		accountsCheck_obj.is_verified = True
		accountsCheck_obj.save()
		return redirect('login')

def verificationMain(email, auth_token,request):
	subject = 'Please verify your account'
	message = f'Hi please click on the link to verify your account {request.build_absolute_uri()}verify/{auth_token}'
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [email]
	send_mail(subject,message,email_from, recipient_list)

def logoutUser(request):
	logout(request)
	return redirect('login')

def fileUpload(request):
	if request.method == 'POST':

		csv_file = request.FILES["dataFile"]#change csv_file according to your form input name
		file_data = csv_file.read().decode("utf-8")     
		lines = file_data.split("\n")
		lines.pop(0)
		for row in lines:
			print(row)
			data = row.split(",")
			if(row):
				userAddress.objects.create(fname=data[0],lname=data[1],user=request.user,address=data[2],city=data[3],state=data[4],zip=data[5])
	return redirect('home')

def deleteTag(request, pk, id,did):
	detailsTagsObj = detailsTags.objects.get(id=pk)
	addressDetailsTagsObj = addressDetailsTags.objects.get(id=id)
	detailsTagsObj.tags.remove(addressDetailsTagsObj)
	detailsTagsObj.save()
	return redirect(details,did)