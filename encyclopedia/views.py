from django.shortcuts import render
from . import util 
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
# to randomize the list for random function and random button
from random import shuffle
import markdown2

class EditForm(forms.Form):
    title = forms.CharField(label="Title")
    data = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}))

# convert the markdown to html
def markdown_convert(html):
    html = markdown2.markdown(html)
    return html

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": EditForm()
    })

    
def title(request, title):
    if title is None:
        return render(request, "encyclopedia/apology.html",{
            "messege": "You forgot to enter title",
            "title": "Error"
        })
        
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/apology.html",{
            "messege": "File was not found",
            "title": "Error"
        })
    
    else:
        entry = markdown_convert(entry)
        return render(request, "encyclopedia/title.html",{
            "entry": entry,
            "title": title
        })


def search(request):
    if request.method == "POST":
        title = request.POST["q"]
        entry = util.get_entry(title)
        if entry is not None:
            entry = markdown_convert(entry)
            return render(request, "encyclopedia/title.html",{
                "title": title,
                "entry": entry
            })

        else:
            entries = util.list_entries()
            related = []
            for entry in entries:
                if title.lower() in entry.lower():
                    related.append(entry)

            if len(related) is 0:
                return render(request, "encyclopedia/apology.html",{
                    "title": "Apology",
                    "messege": "No data found"
                })

            else:
                return render(request, "encyclopedia/recomended.html", {
                     "messege": "You mean",
                     "entry": related
                })

    # else:
    #     return render(request, "encyclopedia/apology.html")


def new(request):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            data = form.cleaned_data["data"]
            # to make it a heading in the markdown
        if title in util.list_entries():
            return render(request, "encyclopedia/apology.html",{
                "messege": "Error",
                "title": "File with same name already exist"
            })
        else:
            util.save_entry(title, data)
            return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "encyclopedia/new.html", {
            "form": EditForm()
        })

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            info = form.cleaned_data["data"]
            util.save_entry(title, info)
            info = markdown_convert(info)
            return render(request, "encyclopedia/title.html",{
                "entry": info,
                "title": title
            })

    else:
        entry = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "form": EditForm(initial={"title": title, "data": entry}),
            "title": title
        })

def random(request):
    list = util.list_entries()
    shuffle(list)
    return HttpResponseRedirect(f"wiki/{list[0]}")

    





