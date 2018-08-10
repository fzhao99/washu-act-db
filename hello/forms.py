from django import forms
from .models import Active_Group, Submissions, Data_Type_Collection
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _


class NewGroupForm(forms.ModelForm):
    link_of_data = forms.FileField(label = "File Containing Data", help_text="Submit Igor Binary or CSV with Data")
    link_of_metadata = forms.FileField(label = "File Containing Metadata",
            help_text=mark_safe('Submit Igor Binary or CSV with Metadata. See <a href="http://cires1.colorado.edu/jimenez-group/AMSsd/"" target="_blank">original database</a> for citation examples'))
    comment_file = forms.FileField(label = "File with additional comments", help_text =" Submit text file with any additional comments. Not required", required=False)
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

class NewDatabaseRequestForm(forms.ModelForm):

    class Meta:
        model = Data_Type_Collection
        labels = {
            "name": _("Proposed Name"),
            "description": _("Description"),
            "authorized_contributors": _("Authorized Contributors"),
            "public":_("Public"),
        }
        help_texts = {
            'description': _('Description of what the database will be used for.'),
            'authorized_contributors': _('Enter the usernames for the proposed contributors. '
                    'Hold down "Control", or "Command" on a Mac, to select more than one.'),
            "public":_("If selected, the database will be available to all users"
                    " who have login credentials. Please 1) Leave the box unselected "
                    " 2) email the admin with a list of the email addresses you "
                    " wish to have access if you don't wish for this to be case.")
        }
        fields = ['name', 'description','public']
