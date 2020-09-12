import secrets

from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown

from . import util


class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'id': 'title'}))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'id': 'content'}))
    edit = forms.BooleanField(
        initial=False, widget=forms.HiddenInput(), required=False)


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    markDownPage = Markdown()
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/entryNotFound.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "entry": markDownPage.convert(entryPage),
            "entryTitle": entry
        })


def newEntry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title) is None or form.cleaned_data["edit"] is True:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={'entry': title}))
            else:
                return render(request, "encyclopedia/entryNotFound.html", {
                    "form": form,
                    "existing": True,
                    "entry": title
                })
        else:
            return render(request, "encyclopedia/newEntry.html", {
                "form": form,
                "existing": False
            })
    else:
        return render(request, "encyclopedia/newEntry.html", {
            "form": NewEntryForm(),
            "existing": False
        })


def editEntry(request, entry):
    entryPage = util.get_entry(entry)
    if entryPage is None:
        return render(request, "encyclopedia/entryNotFound.html", {
            "entryTitle": entry
        })
    else:
        form = NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = forms.HiddenInput()
        form.fields["content"].initial = entryPage
        form.fields["edit"].initial = True
        return render(request, "encyclopedia/newEntry.html", {
            "form": form,
            "edit": form.fields["edit"].initial,
            "entryTitle": form.fields["title"].initial
        })


def randomEntry(request):
    entryLists = util.list_entries()
    random_Entry = secrets.choice(entryLists)
    return HttpResponseRedirect(reverse("entry", kwargs={'entry': random_Entry}))


def searchEntry(request):
    result = request.GET.get('q', '')
    if(util.get_entry(result) is not None):
        return HttpResponseRedirect(reverse("entry", kwargs={'entry': result}))
    else:
        Entries = []
        for entry in util.list_entries():
            if result.upper() in entry.upper():
                Entries.append(entry)
        return render(request, "encyclopedia/index.html", {
            "entry": Entries,
            "search": True,
            "value": result,
            "msg": "not found !!"
        })
