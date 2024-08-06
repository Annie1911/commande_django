from django import forms

class DateRangeForm(forms.Form):
    date = forms.DateField(label='Date', widget=forms.SelectDateWidget, required=False)
    period_choice = forms.ChoiceField(
        choices=[('today', 'Aujourd\'hui'), ('custom', 'Période personnalisée')],
        label='Période',
        required=True
    )

    def clean(self):
        cleaned_data = super().clean()
        period_choice = cleaned_data.get("period_choice")
        date = cleaned_data.get("date")
        
        if period_choice == 'custom' and not date:
            raise forms.ValidationError("Pour une période personnalisée, veuillez spécifier une date.")
        
        return cleaned_data
