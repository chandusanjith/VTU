from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa
import os
from random import randint
from rest_framework.response import Response
from rest_framework import status
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        response = BytesIO()
        file = open("my.file.pdf", "wb")
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
        file.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return Response({"ERROR": "pdf gen err"}, status=status.HTTP_404_NOT_FOUND)

    @staticmethod
    def render_to_file(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}-{1}.pdf".format(params['request'].user.first_name, randint(1, 1000000))
        #file_path1 = os.path.join(os.path.abspath(os.path.dirname("__file__")), "media", file_name)
        #print(file_path1)
        file_path2 = os.path.join(BASE_DIR,'media')
        file_path = file_path2 + '/' + file_name
        print(file_path)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return file_name