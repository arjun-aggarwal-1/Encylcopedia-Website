from django.shortcuts import render
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from random import choice
from django.urls import reverse
from . import util
from markdown2 import Markdown

class NewForm(forms.Form):
    name=forms.CharField(label="New Entry")
    text = forms.CharField(label="Text", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def create(request):
    if request.method=="POST":
        form = NewForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data["name"]
            text = form.cleaned_data["text"]
            if util.get_entry(name):
                return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
            })
            util.save_entry(name, text)
            return render(request, "encyclopedia/index.html", {
                    "entries": util.list_entries()
            })
    return render(request, "encyclopedia/create.html",
    {"form":NewForm()})

def entry(request, name):
    entry = util.get_entry(name)
    if entry == None:
        return render(request, "encyclopedia/error.html", {
            "message" : f"No entry for {name} found. Why not create one?"
        })

    mymarkdown = Markdown()
    return render(request, "encyclopedia/entry.html", {
        "name" : name,
        "entry" : mymarkdown.convert(entry)
    })

def edit(request):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html")

    if request.method == "POST":
        if request.POST["action"] == "edit":
            return render(request, "encyclopedia/edit.html", {
                "name" : request.POST["name"],
                "entry" : util.get_entry(request.POST["name"])
            })

        elif request.POST["action"] == "save":
            util.save_entry(request.POST["name"], request.POST["entry"])
            url = reverse('entry', kwargs={'name': request.POST["name"]})
            return HttpResponseRedirect(url)

def search(request):
    if request.method == "POST":
        query = request.POST["q"]
        entry = util.get_entry(query)

        if entry:
            url = reverse('entry', kwargs={'name': query})
            return HttpResponseRedirect(url)

        else:
            entries = util.list_entries()
            matches = []

            for entry in entries:
                if query.upper() in entry.upper():
                    matches.append(entry)

            return render(request, "encyclopedia/search.html", {
                "entries" : matches
            })
def random(request):
    entries = util.list_entries()
    entry = choice(entries)
    url = reverse('entry', kwargs={'name': entry})
    return HttpResponseRedirect(url)