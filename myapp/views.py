from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import Publisher, Book, Member, Order
from django.shortcuts import render


# Create your views here.
def index(request):
    response = HttpResponse()
    booklist = Book.objects.all().order_by('id')[:10]
    heading1 = '<p>' + '<b>List of available books:</b> ' + '</p>'
    response.write(heading1)
    for book in booklist:
        para = '<p>'+ str(book.id) + ': ' + str(book) + '</p>'
        response.write(para)

    publisherlist = Publisher.objects.all().order_by("-city")
    heading2 = '<br><p>' + '<b>List of Publishers:</b>' + '</p>'
    response.write(heading2)
    for publisher in publisherlist:
        name = '<p>' + str(publisher.name) + '\t lives in' + '<b> \t' + str(publisher.city)+ '</b>' '</p>'
        response.write(name)
        return response

def about(request):
    respose1 = HttpResponse()
    heading3 = '<h1> <b> <center> This is an eBook APP </center> </b> </h1>'
    respose1.write(heading3)
    return respose1

def details(request, book_id):
    response_detail = HttpResponse()
    book = Book.objects.get(id=book_id)
    title = '<p> <b>Book name is:</b> ' + str(book.title.upper()) + '</p>'
    price = '<p> <b>Book Price is:</b> ' + '$' + str(book.price) + '</p>'
    author = '<p> <b>Publisher of book is:</b> ' + str(book.publisher)+ '</p>'
    response_detail.write(title)
    response_detail.write(price)
    response_detail.write(author)
    return response_detail


