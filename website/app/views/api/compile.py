from pathlib import Path
import os

from app.views.api import APIView, APIError, takes_json
from app.compiler import Compiler
from app.models import Game, CompilerReport

from django.http import HttpRequest
from django.conf import settings


class CompileView(APIView):
    @takes_json
    def post(self, request: HttpRequest):
        file_content = request.FILES['input_file'].read()
        try:
            lang = str(self.json_input.get("language"))
        except:
            raise APIError("Undefined language", 422)
        DIR = Path(__file__).resolve().parent.parent.parent.parent
        file_name = f"main.{settings.FRONTEND_LANGUAGES[lang]}"
        file_path = os.path.join(DIR / "media", file_name)
        with open(file_path, "w") as source_file:
            file_extension = settings.FRONTEND_LANGUAGES[lang]
            source_file.write(str(file_content.decode()))
        file_compiler = Compiler(str(DIR / ("media/" + file_name)), file_extension, None)
        file_compiler.compile()
        while file_compiler.report is None:
            continue
        os.remove(str(DIR / ("media/" + file_name)))
        if file_compiler.report.status == CompilerReport.Status.OK:
            return self.render_json(200,
                                    {'status': 'File compiled',
                                     'report': str(file_compiler.report)})
        else:
            return self.render_json(422,
                                    {'status': 'File compilation failed',
                                     'report': str(file_compiler.report)})
