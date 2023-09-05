from django.http import HttpRequest, HttpResponse,HttpResponseForbidden
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
import os

def view_func(request:HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile') :
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        file_url = fs.url(filename)
        file_path = fs.url(filename).lstrip('/')
        file_size = os.path.getsize(file_path)

        if file_size > 1 * 1024 * 1024:
            print('Ошибка: Размер файла', file_url, 'превышает максимально допустимый размер (1 МБ).')
            fs.delete(filename)
            return HttpResponseForbidden(f"Ошибка: Размер файла, {file_url}, превышает максимально допустимый размер (1 МБ).")

        else:
            print('Saved file', file_url)

    return render(request, 'practical_work/file_upload.html')
