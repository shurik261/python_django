from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.core.files.storage import FileSystemStorage
from .forms import UserBioForm, UploadFileForm

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
    context = {
        'form': UserBioForm(),
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)

def handle_file_upload(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # myfile = request.FILES['myfile']
            myfile = form.cleaned_data['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print('saved file', filename)
    else:
        form = UploadFileForm()
    context = {
        'form': form
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)

# def view_func(request:HttpRequest) -> HttpResponse:
#     if request.method == 'POST' and request.FILES.get('myfile') :
#         myfile = request.FILES['myfile']
#         if myfile.size < 1048576:
#             fs = FileSystemStorage()
#             filename = fs.save(myfile.name, myfile)
#             print('Saved file', filename)
#
#         else:
#             return HttpResponseForbidden(f"Ошибка: Размер файла, превышает максимально допустимый размер (1 МБ).")
#     return render(request, 'requestdataapp/file-upload.html')