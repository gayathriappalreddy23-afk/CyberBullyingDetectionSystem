from django.shortcuts import render

# Create your views here.

def post_comments(request, post_id):
    return render(request, 'comments/comments.html')
