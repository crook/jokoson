import csv

from django.http import HttpResponse

from django.shortcuts import render_to_response
from django.template import RequestContext
from jokoson.file import forms


def upload_file(request):
    if request.POST:
        form = forms.UploadFileForm(request.POST, request.FILES)
        with request.FILES['file'] as f:
            # TODO: Parse csv file and persist into db
            pass
            # f = request.FILES['file']
            # line = f.readline()  # 读取表头
            # while True:
            #     line = f.readline()
            #     try:
            #         line1 = line.decode('utf-8-sig')
            #         if not line1 or line1 == '\r\n' or line1 == '\r' or line1 == '\n' or line1 == '': break
            #         arg = line1.split(',')
            #         publicationTime = arg[3].rstrip('\r\n')
            #         book = Book(name=arg[0], author=arg[2], press=arg[1],
            #                     publicationTime=publicationTime)
            #         book.save()
            #     except:
            #         pass
            #         line2 = line.decode('gb2312')
            #         if not line2 or line2 == '\r\n' or line2 == '\r' or line2 == '\n' or line2 == '': break
            #         arg = line2.split(',')
            #         publicationTime = arg[3].rstrip('\r\n')
            #         book = Book(name=arg[0], author=arg[2], press=arg[1],
            #                     publicationTime=publicationTime)
            #         book.save()
            # f.close()

        # return render_to_response('book/success.html')
        return HttpResponse(None, None, None)

    else:
        form = forms.UploadFileForm()
    # return render_to_response('book/upload.html', {'form': form})
    return HttpResponse(None, None, None)

    return


def download_file(request):
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=book_list.csv'
    writer = csv.writer(response)
    # TODO: export as csv file
    # writer.writerow(['name', 'author', 'press', 'publicationTime', 'reader'])
    # books = Book.objects.all()
    # for book in books:
    #     if book.reader_id:
    #         try:
    #             readName = Reader.objects.get(id__iexact=book.reader_id).name
    #         except:
    #             readName = ''
    #     else:
    #         readName = ''
    #     writer.writerow(
    #         [book.name, book.author, book.press, book.publicationTime,
    #          readName])
    return response
