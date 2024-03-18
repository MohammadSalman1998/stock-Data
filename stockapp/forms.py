from django import forms
from .models import StockData

class StockForm(forms.Form):
    ticker = forms.CharField(max_length=10)
    start_date = forms.DateField()
    end_date = forms.DateField()

    def clean(self):
        # cleaned_data = super().clean()
        ticker = self.get("ticker")
        start_date = self.get("start_date")
        end_date = self.get("end_date")

        if start_date and end_date:
            if end_date < start_date:
                self.add_error("end_date", "End date should be after the start date.")