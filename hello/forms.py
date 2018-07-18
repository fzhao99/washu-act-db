from django import forms
from .models import Active_Group
from django.utils.safestring import mark_safe

class NewGroupForm(forms.ModelForm):
    link_of_data = forms.FileField(label = "File Containing Data", help_text="Submit Igor Binary or CSV with Data")
    link_of_metadata = forms.FileField(label = "File Containing Metadata",
            help_text=mark_safe('Submit Igor Binary or CSV with Metadata. See <a href="http://cires1.colorado.edu/jimenez-group/AMSsd/"" target="_blank">original database</a> for citation examples'))

    class Meta:
        model = Active_Group
        fields = ['name','link_of_data','link_of_metadata']
