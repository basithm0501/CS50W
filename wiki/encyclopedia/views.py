from django.shortcuts import render
import markdown2

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
        