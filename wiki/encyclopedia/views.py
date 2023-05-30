from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, topic):
    return render(request, "encyclopedia/entry.html", {
        "entries": util.list_entries(),
        "topic": topic,
        "content": util.get_entry(topic),
    })

