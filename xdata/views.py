from django.shortcuts import render, redirect
from .forms import ClientsForm
from .models import Filterwords, Clients, Articles, Notifications, Sites

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
            """
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
            """
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
def articles_list(request):
    articles_list = list(Articles.objects.all())  # Convert the QuerySet to a list
    context = {'articles_list': articles_list}
    return render(request, "xdata/articles_list.html", context)

#SEARCH
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