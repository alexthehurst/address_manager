from django import forms
from django.core.exceptions import ValidationError

def validate_bulk_import_max_records(bulk_addresses):
	if len(bulk_addresses.strip().split('\n')) > 500:
		raise ValidationError(
			'Too many records. Please provide 500 or fewer lines '
			'of address data at once.',
			code='too_many')

class BulkImportForm(forms.Form):
	
	bulk_addresses = forms.CharField(max_length=40000, 
		widget=forms.Textarea,
		label="Paste up to 500 addresses here, one per line.",
		validators=[validate_bulk_import_max_records],

	)
