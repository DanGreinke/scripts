from django.shortcuts import render, redirect
from . import util
import markdown2
from django.http import HttpResponse
from django import forms
from random import choice


class newEntry(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Title', 'style': 'width: 300px;', 'class': 'form-control'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Content Text', 'style':'width: 900px;','class': 'form-control'}))


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def md(request,page):
    try:
        return render(request,'encyclopedia/page.html',{
            "content": markdown2.markdown(util.get_entry(page)),
            "query_results": False,
            "title": page
        })
    except:
        return HttpResponse('Page Not Found :(')

def search(request):
    entries = util.list_entries()
    query = request.GET.get("q", "")
    if query in entries:
        return redirect('/wiki/' + query)
    else:
        results = [entry for entry in entries if query.lower() in entry.lower()]
        return render(request,'encyclopedia/index.html',{
            "entries": results,
            "query_results": True
        })

def create(request):
    if request.method == "POST":
        form = newEntry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return redirect('/wiki/{title}'.format(title=title))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": newEntry()
    })

def edit(request, page):
    title = page
    content = util.get_entry(page)
    form = newEntry(initial={'title':title,'content':content})
    return render(request, "encyclopedia/create.html", {
        "form": form
    })

def random(request):
    entries = util.list_entries()
    return redirect('/wiki/' + choice(entries))

