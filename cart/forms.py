from django import forms


class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(widget=forms.TextInput(
        attrs={'size': '2', 'value': '1', 'class': 'quantity'}),
        error_messages={'invalid': '请输入一个有效的数字'},
        min_value=1)
    product_id = forms.IntegerField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(AddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError('需要启用cookies')
