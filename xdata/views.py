from django.shortcuts import render, redirect
from .forms import ClientsForm, NotificationsForm, FilterwordsForm, CSVUploadForm
from .models import Filterwords, Clients, Articles, Notifications, Sites
from django.shortcuts import get_object_or_404
import csv
import io
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd



#from django.http import Http404

# Create your views here.

#HOME
def home(request):
    return render(request, 'xdata/home.html')


#CLIENT CRUD operations:

#READ
def clients_list(request):
    clients_list = list(Clients.objects.all())  # Convert the QuerySet to a list
    context = {'clients_list': clients_list}
    return render(request, "xdata/clients_list.html", context)

#INSERT / UPDATE
def clients_form(request, id=0):
    if request.method == 'POST':  # POST requests
        if id == 0: #POST for INSERT
            form = ClientsForm(request.POST)
        else: #POST for UPDATE
            client = Clients.objects.get(pk=id)
            form = ClientsForm(request.POST, instance=client)
        if form.is_valid():
            # Create and save the new client
            new_client = form.save()
            print("Form is valid. Data saved.")
            
            selected_filterword = form.cleaned_data.get('filterwordsid') #select filerwordID for new client
            filterword = Filterwords.objects.get(id=selected_filterword) #retriving existing filterword from table
            new_filterword = Filterwords( #to be pushed in the table
                    clientid = new_client.id,
                    word = filterword.word,
                    wordalias = filterword.wordalias,
                    subwordalias = filterword.subwordalias,
                    stopword = filterword.stopword,
            )
            new_filterword.save()
            
            return redirect('/clients/list')
        else:
            print("Form is invalid.")
            return render(request, "xdata/clients_form.html", {'form': form})
    else: # GET requests
        # Create the form instance and set the initial values to None
        if id == 0: #GET for INSERT operation
            form = ClientsForm()
            #print(form['filterwordsid'].value())  # Check the initial value
        else: #GET for UPDATE operation
            client = Clients.objects.get(pk=id)
            form = ClientsForm(instance=client) #populating the form 
        return render(request, "xdata/clients_form.html", {'form': form})

#DELETE
def clients_delete(request, id):
    client = Clients.objects.get(pk=id)
    client.delete()
    return redirect('/clients/list')


# ARTICLES

# READ ALL
def articles_list(request):
    articles_list = list(Articles.objects.all())  # Convert the QuerySet to a list
    context = {'articles_list': articles_list}
    return render(request, "xdata/articles_list.html", context)

# SEARCH
def search_articles(request):
    clientid = request.GET.get('clientid')
    articles_list = None  # Initialize the list to None
    if clientid:
        try:
            articles_list = Articles.objects.filter(clientid=clientid)
        except Articles.DoesNotExist:
            # Handle the case where no articles match the clientid
            articles_list = []

    context = {'articles_list': articles_list}
    return render(request, 'xdata/articles_list_id.html', context)


#FILTERWORDS CRUD

#READ all or ID
def filterwords_list(request, clientid=0):
    if clientid == 0:
        filterwords_list = list(Filterwords.objects.all())  # Convert the QuerySet to a list
        context = {'filterwords_list': filterwords_list}
        return render(request, "xdata/filterwords_list.html", context)
    else:
        try:
            filterwords_list = list(Filterwords.objects.filter(clientid=clientid))
            # here I pass clientid since for the insertion I will need to know
            # specific if of the client to insert filterword for it
            context = {'filterwords_list': filterwords_list, 'clientid': clientid}
            return render(request, "xdata/filterwords_list_id.html", context)
        except Notifications.DoesNotExist:
            context = {'clientid': clientid}
            return render(request, "xdata/filterword_not_found.html", context)


# INSERT
def filterwords_insert(request, clientid):
    client = Clients.objects.get(id=clientid)
    
    if request.method == 'POST':
        form = FilterwordsForm(request.POST)
        if form.is_valid():
            filterword = form.save(commit=False)
            filterword.clientid = client.id  # Set the client
            filterword.save()
            print("Form is valid. Data saved.")
            return redirect('/clients/list')
        else:
            print("Form is invalid.")
            return render(request, "xdata/filterwords_form.html", {'form': form})
    else:
        form = FilterwordsForm()
        return render(request, "xdata/filterwords_form.html", {'form': form})


# UPDATE
def filterwords_update(request, filterword_id):
    if request.method == 'POST':  # POST requests
        filterword = Filterwords.objects.get(pk=filterword_id)
        form = FilterwordsForm(request.POST, instance=filterword)
        if form.is_valid():
            # Create and save the new filter word
            form.save()
            print("Form is valid. Data saved.")
            return redirect('/clients/list')
        else:
            print("Form is invalid.")
            return render(request, "xdata/filterwords_form.html", {'form': form})
    else: # GET requests
        filterword = Filterwords.objects.get(pk=filterword_id)
        form = FilterwordsForm(instance=filterword) #populating the form 
        return render(request, "xdata/filterwords_form.html", {'form': form})


# DELETE
def filterwords_delete(request, id=0):
    filterword = Filterwords.objects.get(pk=id)
    filterword.delete()
    return redirect('/clients/list')


# CSV UPLOAD HANDLING

def preview_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            data = pd.read_csv(csv_file)

            # Save each row from the CSV to the database
            for index, row in data.iterrows():
                csv_data_instance = Filterwords(
                    clientid=row['clientid'],
                    word=row['word'],
                    wordalias=row['wordalias'],
                    subwordalias=row['subwordalias'],
                    stopword=row['stopword']
                )
                csv_data_instance.save()

            return render(request, 'xdata/preview_csv.html', {'data': data})
    else:
        form = CSVUploadForm()
    return render(request, 'xdata/upload_csv.html', {'form': form})

#NOTIFICATIONS CRUD

#READ
def notifications_list(request, clientid=0):
    if clientid == 0: # if all list
        notifications_list = list(Notifications.objects.all())  # Convert the QuerySet to a list
        context = {'notifications_list': notifications_list}
        return render(request, "xdata/notifications_list.html", context)
    else: # if only based on ID
        try:
            notifications_list = list(Notifications.objects.filter(clientid=clientid))
            context = {'notifications_list': notifications_list, 'clientid': clientid}
            return render(request, "xdata/notifications_list_id.html", context)
        except Notifications.DoesNotExist:
            context = {'clientid': clientid}
            return render(request, "xdata/notification_not_found.html", context)

# INSERT 
def notifications_insert(request, clientid):
    client = Clients.objects.get(id=clientid)
    
    if request.method == 'POST':
        form = NotificationsForm(request.POST)
        if form.is_valid():
            notification = form.save(commit=False)
            notification.clientid = client.id  # Set the client
            notification.save()
            print("Form is valid. Data saved.")
            return redirect('/clients/list')
        else:
            print("Form is invalid.")
            return render(request, "xdata/notifications_form.html", {'form': form})
    else:
        form = NotificationsForm()
        return render(request, "xdata/notifications_form.html", {'form': form})

# UPDATE
def notifications_update(request, notification_id):
    if request.method == 'POST':  # POST requests
        notification = Notifications.objects.get(pk=notification_id)
        form = NotificationsForm(request.POST, instance=notification)
        if form.is_valid():
            # Create and save the new notification
            form.save()
            print("Form is valid. Data saved.")
            return redirect('/clients/list')
        else:
            print("Form is invalid.")
            return render(request, "xdata/notifications_form.html", {'form': form})
    else: # GET requests
        notification = Notifications.objects.get(pk=notification_id)
        form = NotificationsForm(instance=notification) #populating the form 
        return render(request, "xdata/notifications_form.html", {'form': form})
    

#DELETE
def notifications_delete(request, id=0):
    notification = Notifications.objects.get(pk=id)
    notification.delete()
    return redirect('/clients/list')