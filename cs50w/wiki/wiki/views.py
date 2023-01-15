'''
from django.shortcuts import render
from encyclopedia import util
import markdown2
#from . import util

# Views below here
def md(request,page):
    return render(request,'encyclopedia/page.html',{
        "page": markdown2.markdown(get_entry(page))
    })

'''