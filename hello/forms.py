from django import forms
from .models import Active_Group, Submissions
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class NewGroupForm(forms.ModelForm):
    link_of_data = forms.FileField(label = "File Containing Data", help_text="Submit Igor Binary or CSV with Data")
    link_of_metadata = forms.FileField(label = "File Containing Metadata",
            help_text=mark_safe('Submit Igor Binary or CSV with Metadata. See <a href="http://cires1.colorado.edu/jimenez-group/AMSsd/"" target="_blank">original database</a> for citation examples'))

    class Meta:
        model = Active_Group
        labels = {
            "name": _("Name of Group")
        }
        help_texts = {
            'name': mark_safe(_('Please format your group name as <i>yourinstitution_yourgroup</i> (ie: WashU_ACT)')),
        }
        fields = ['name','link_of_data','link_of_metadata']

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submissions
        fields = ['link_of_data', ]
