from django.views.generic.edit import FormView

from .forms import ReportDownloadForm
from .reports import ReportBuilder

# Create your views here.

class ReportDownload(FormView):
    template_name = 'reports/report_download_form.html'
    form_class = ReportDownloadForm

    def form_valid(self, form):
        report = ReportBuilder(
            form.cleaned_data['start'],
            form.cleaned_data['end'],
        )

        document = getattr(report, form.cleaned_data['report'])(
            orientation=form.cleaned_data['orientation'],
        )

        return report.get_response(document)
