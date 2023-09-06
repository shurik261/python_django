from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.core.files.storage import FileSystemStorage

def proces_get_view(request:HttpRequest) -> HttpResponse:
    a = request.GET.get('a', '')
    b = request.GET.get('b', '')
    result = a + b
    context = {
        'a': a,
        'b': b,
        'result': result

    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)

def user_form(request:HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/user-bio-form.html')

# def handle_file_upload(request:HttpRequest) -> HttpResponse:
#     if request.method == 'POST' and request.FILES.get('myfile'):
#         myfile = request.FILES['myfile']
#         fs = FileSystemStorage()
#         filename = fs.save(myfile.name, myfile)
#         print('saved file', filename)
#     return render(request, 'requestdataapp/file-upload.html')

def view_func(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile') :
        myfile = request.FILES['myfile']
        if myfile.size < 1048576:
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print('Saved file', filename)

        else:
            return HttpResponseForbidden(f"Ошибка: Размер файла, превышает максимально допустимый размер (1 МБ).")
    return render(request, 'requestdataapp/file-upload.html')