from django import forms

class AddTransantionForm(forms.Form):
    pricePerCoin = forms.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    quantity = forms.DecimalField(max_digits=10, decimal_places=2, null=False, default=0)
    date = forms.CharField(label='Mensaje', widget=forms.Textarea)