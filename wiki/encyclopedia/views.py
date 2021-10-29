from django.shortcuts import render
from django.http import HttpResponseRedirect
from django import forms
from random import randint
import markdown2

from . import util


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
    error = False
    if request.method == "POST":
        title = request.POST['new_title']
        content = request.POST['new_content']
        if title in util.list_entries():
            error = True
            return render(request, "encyclopedia/newpage.html", {
                "error": error
            })
        else:
            util.save_entry(title, content)
            return HttpResponseRedirect(f"/wiki/{title}")
    else:
        return render(request, "encyclopedia/newpage.html", {
            "error": error
        })

def search(request):
    if request.method == "POST":
        input = request.POST['q']
        if input in util.list_entries():
            return HttpResponseRedirect(f"wiki/{input}")
        else:
            list_of_search_result = []
            resultshown = False
            for pagename in util.list_entries():
                if input.upper() in pagename.upper():
                    list_of_search_result.append(pagename)
                    resultshown = True
            return render(request, "encyclopedia/search.html", {
                "searchresults": list_of_search_result,
                "resultshown": resultshown
            })
    else:
        return render(request, "encyclopedia/index.html")

def edit(request, name):
    entry = util.get_entry(name)
    return render(request, "encyclopedia/edit.html", {
        "name": name,
        "entry": entry
    })

def confirmedit(request, name):
    content = request.POST['edited_content']
    util.save_entry(name, content)
    return HttpResponseRedirect(f"/wiki/{name}")
