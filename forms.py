from django import forms

class BulkImportForm(forms.Form):
	bulk_addresses = forms.CharField(max_length=40000, widget=forms.Textarea, label="Paste up to 500 addresses here, one per line.")
