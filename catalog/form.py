from django import forms


class AddCommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    product_id = forms.IntegerField(widget=forms.HiddenInput())
    author_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(AddCommentForm, self).__init__(*args, **kwargs)