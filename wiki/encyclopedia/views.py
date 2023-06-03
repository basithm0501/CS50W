from django.shortcuts import render
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, topic):
    if topic in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "entries": util.list_entries(),
            "topic": topic,
            "content": markdown2.markdown(util.get_entry(topic)),
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "entries": util.list_entries(),
            "topic": topic
        })

def result(request):
    search = request.GET.get('q', '')
    if search in util.list_entries():
        return render(request, "encyclopedia/entry.html", {
            "entries": util.list_entries(),
            "topic": search,
            "content": markdown2.markdown(util.get_entry(search)),
        })
    else:
        relatedresults = []
        for entry in util.list_entries():
            if search in entry:
                relatedresults.append(entry)

        return render(request, "encyclopedia/results.html", {
            "entries": util.list_entries(),
            "results": relatedresults
        })
        
def newpage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/newpage.html", {
            "entries": util.list_entries(),
        })
    elif request.method == "POST":
        n_title = request.POST.get("title", "")
        n_content = request.POST.get("content", "")
        if n_title in util.list_entries():
            return render(request, "encyclopedia/newpage.html", {
                "entries": util.list_entries(),
                "err": True
            })
        else:
            make_new_md(n_title, n_content)
            return render(request, "encyclopedia/entry.html", {
                "entries": util.list_entries(),
                "topic": n_title,
                "content": markdown2.markdown(n_content),
            })
        
def edit(request, topic):
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "entries": util.list_entries(),
            "topic": topic,
            "content": util.get_entry(topic)
        })
    elif request.method == "POST":
        n_content = request.POST.get("new_content", "")
        make_new_md(topic, n_content)
        return render(request, "encyclopedia/entry.html", {
            "entries": util.list_entries(),
            "topic": topic,
            "content": markdown2.markdown(util.get_entry(topic)),
        })

def rand(request):
    topic = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
            "entries": util.list_entries(),
            "topic": topic,
            "content": markdown2.markdown(util.get_entry(topic)),
        })

def make_new_md(title, content):
    content = content.replace("\n", "")
    f = open(f"entries/{title}.md", "w")
    f.write(content)
    f.close()
