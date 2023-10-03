from django.shortcuts import render
from django.http import HttpResponse

import os

from .module.modules import *

# Create your views here.
def process(request):
    file = request.FILES.get('file')
    fileType = str(file).split('.')[1]

    print('Submission: ' + str(request))
    print(str(file).split('.')[1])
    print(file)

    txt = ""

    if (fileType == 'hwp'):
        txt = hwpToTxt(file)
    elif (fileType == 'pdf'):
        txt = pdfToTxt(file)
    elif (fileType == 'docx'):
        txt = docxToTxt(file)
    elif (fileType == 'pptx'):
        txt = pptxToTxt(file)
    elif (fileType in ['gif', 'png', 'jpg', 'jpeg', 'tif', 'tiff']):
        txt = imgToTxt(file)
    else:
        return HttpResponse('error: invalid file type')

    txtToSpch(txt)

    f = open('result.mp3', 'rb')
    response = HttpResponse()
    response.write(f.read())
    response['Content-Type'] = 'audio/mp3'
    response['Content-Disposition'] = 'attachment; filename = %s.mp3' % str(file).split('.')[0]
    response['Content-Length'] = os.path.getsize('result.mp3')

    return response


