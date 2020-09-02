from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'base.html')

def new_search(request):
    search = request.POST.get('content')
    print(search)


    return render(request, 'index.html', {'search': search})