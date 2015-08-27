from django import forms
from django.core.exceptions import ValidationError
from models import AddressSet

def validate_bulk_import_max_records(bulk_addresses):
	if len(bulk_addresses.strip().split('\n')) > 500:
		raise ValidationError(
			'Too many records. Please provide 500 or fewer lines '
			'of address data at once.',
			code='too_many')

# Keep from attempting imports if there are addresses which will fail to import.
# I tried to use try/except to gracefully handle database import errors, but
# exceptions are thrown after aborting an import when trying to access the DB again.
# The solution may be to redirect to a page that doesn't hit the database, but rather a
# simple 500 internal server error page for situations like that.
#
# Of course, I don't know that I could even test that, since I'm now going to gracefully catch
# the only example I could come up with which causes a db error.

def validate_bulk_import_line_length(bulk_addresses):
    for line in bulk_addresses.split('\n'):
        if len(line) > 1000:
            raise ValidationError(
                    'At least one line was too long. Please limit addresses'
                    'to 1000 characters or fewer.'
            )

class BulkImportForm(forms.Form):
	
	bulk_addresses = forms.CharField(max_length=40000, 
		widget=forms.Textarea,
		label="Paste up to 500 addresses here, one per line.",
		validators=[validate_bulk_import_max_records,
           validate_bulk_import_line_length,
        ],

	)
        address_set_select = forms.ModelChoiceField(
                label="Which set should these addresses be imported to?",
                queryset=AddressSet.objects.all(),
                empty_label='Address Set:',
        )

class AddressSetSelectForm(forms.Form):

        address_set_select = forms.ModelChoiceField(
                label="Which set of addresses would you like to view?",
                queryset=AddressSet.objects.all(),
                empty_label='Address Set:',
        )
