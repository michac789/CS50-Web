from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from random import randint
import markdown2

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label="search")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def loadpage(request, name):
    if name in util.list_entries():
        return render(request, "encyclopedia/name.html", {
            "name": name,
            "content": markdown2.markdown(util.get_entry(name))
        })
    else:
        return render(request, "encyclopedia/error.html")

def random(request):
    list = util.list_entries()
    choose = randint(0, len(list) - 1)
    return HttpResponseRedirect(f"/wiki/{list[choose]}")

def newpage(request):
    return render(request, "encyclopedia/newpage.html")

def search(request):
    if request.method == "POST":
        input = request.POST['q']
        if input in util.list_entries():
            return HttpResponseRedirect(f"wiki/{input}")
        else:
            list_of_search_result = []
            for pagename in util.list_entries():
                if input.upper() in pagename.upper():
                    list_of_search_result.append(pagename)
            return render(request, "encyclopedia/search.html", {
                "searchkey": list_of_search_result
            })
    else:
        return render(request, "encyclopedia/index.html")
    #list = util.list_entries()
    #for page in list:
    #    if list[page] == input:
    #       return HttpResponseRedirect(f"/wiki/{list[page]}")
    
