from app.views.api import APIView, APIError, takes_json
from app.models import Game

from website.settings import *
from django.http import HttpRequest

from app.compiler import Compiler


class CompileView(APIView):
    def post(self, request: HttpRequest):
        file_content = request.FILES['input_file'].read()
        lang = request.POST['language']
        DIR = Path(__file__).resolve().parent.parent.parent.parent
        file_name = "main." + FRONTEND_LANGUAGES[lang]
        file_extension = FRONTEND_LANGUAGES[lang]
        file_path = os.path.join(DIR / "media", file_name)
        source_file = open(file_path, "w")
        source_file.write(str(file_content.decode()))
        source_file.close()
        file_compiler = Compiler(str(DIR / ("media/" + file_name)), file_extension, None)
        file_compiler.compile()
        while file_compiler.report is None:
            continue
        os.remove(str(DIR / ("media/" + file_name)))
        if file_compiler.report.status == 0:
            return self.render_json(200,
                                    {'status': 'File compiled',
                                     'report': str(file_compiler.report)})
        else:
            return self.render_json(200,
                                    {'status': 'File compilation failed',
                                     'report': str(file_compiler.report)})
