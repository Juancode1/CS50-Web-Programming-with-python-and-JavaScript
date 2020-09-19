from django.shortcuts import render
from django import forms  
from . import util
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _ #translator module
import markdown2
from markdown2 import Markdown
import random

def validate(strti):
    if str.lower(strti) not in [e.lower() for e in util.list_entries()] :
        return None
    else:
        return True

class SearchForm(forms.Form):
    titulo= forms.CharField(label="",
        widget=forms.TextInput(attrs={'placeholder': 'Search encyclopedia'})
        )

def index(request):
    if request.method == "POST":
        if request.POST['action'] == 'Search':
            form=SearchForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data["titulo"]
            if validate(title):
                return HttpResponseRedirect(reverse("title", args=(title,)))
            else:
                options=[]
                for tit in util.list_entries():
                    if set(title).issubset(str.lower(tit)):
                        options.append(tit)
                return render(request,"encyclopedia/index.html",{
                     "entries": options,
                     "Sform": form,
                 })

    else:
        form=SearchForm()

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "Sform":form,
    })

class EntryForm(forms.Form):
    titulo= forms.CharField( label="Entry Title ")
    contenido= forms.CharField( label="Entry Content ", widget=forms.Textarea)

def newpage(request):
    if request.method == "POST":
        if request.POST['action'] == 'Save Entry':
            entry=EntryForm(request.POST)
            if entry.is_valid():
                title=str.capitalize(entry.cleaned_data["titulo"])
                content=entry.cleaned_data["contenido"]
            if not validate(title):
                util.save_entry(title,"# "+title+"\n"+title+" "+content)
                content=markdown2.markdown(util.get_entry(title))
                return render(request,"encyclopedia/page.html",{
                "content":content,
                "title":title,
                "Sform":SearchForm(),
                })
            else:
                return render(request,'encyclopedia/newpage.html',{
                "message":"Invalid Credentials",
                "Eform":entry,
                "Sform":SearchForm(),
            })

        elif request.POST['action'] == 'Search':
            form=SearchForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data["titulo"]
            if validate(title):
                content=util.get_entry(title)
                return render(request,"encyclopedia/page.html",{
                "content":content,
                "title":str.capitalize(title),
                "Sform":SearchForm(),
                })
            else:
                options=[]
                for tit in util.list_entries():
                    if set(title).issubset(str.lower(tit)):
                        options.append(tit)
                return render(request,"encyclopedia/index.html",{
                     "entries": options,
                     "Sform": form,
                 })
        
    else:
        sform=SearchForm()
        eform=EntryForm()

    return render(request,"encyclopedia/newpage.html",{
        "Sform":sform,
        "Eform":eform
    })

def editpage(request):
    if request.method == "POST":
        if request.POST['action'] == 'Edit Entry':
            entry=EntryForm(request.POST)
            if entry.is_valid():
                title=entry.cleaned_data["titulo"]
                content=entry.cleaned_data["contenido"]
            util.save_entry(title,content)
            content=markdown2.markdown(util.get_entry(title))
            return render(request,"encyclopedia/page.html",{
            "content":content,
            "title":title,
            "Sform":SearchForm(),
            })

        elif request.POST['action'] == 'Search':
            form=SearchForm(request.POST)
            if form.is_valid():
                title=form.cleaned_data["titulo"]
            if validate(title):
                content=util.get_entry(title)
                return render(request,"encyclopedia/page.html",{
                "content":content,
                "title":str.capitalize(title),
                "Sform":SearchForm(),
                })
            else:
                options=[]
                for tit in util.list_entries():
                    if set(title).issubset(str.lower(tit)):
                        options.append(tit)
                return render(request,"encyclopedia/index.html",{
                     "entries": options,
                     "Sform": form,
                 })
    else:
        title=request.GET["edit"]
        content=util.get_entry(title)
        Savetitle=''
        for l in range(2,len(title)+2):
            Savetitle+=content[l]
        
        eform=EntryForm(initial={'titulo':Savetitle,'contenido':content})
        return render(request,"encyclopedia/editpage.html",{
            "Sform":SearchForm(),
            "Eform":eform
        })

def title(request,titulo):
    content=util.get_entry(titulo)
    if content == None:
        return HttpResponse(" Error 404 : page not Found ")
    else:
        content=markdown2.markdown(content)
        return render(request,"encyclopedia/page.html",{
            "content":content,
            "title":str.capitalize(titulo),
            "Sform":SearchForm(),
        })

def randompage(request):
    titles=util.list_entries()
    title=random.choice(titles)
    content=util.get_entry(title)
    content=markdown2.markdown(content)
    return render(request,"encyclopedia/page.html",{
        "content":content,
        "title":str.capitalize(title),
        "Sform":SearchForm(),
    })