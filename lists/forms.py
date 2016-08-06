from django.core.exceptions import ValidationError
from django import forms

from lists.models import Item, List

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this item in your list"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': 'Enter a to-do item',
                'class': 'form-control input-lg',
            }),
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class ExistingListItemForm(ItemForm):

    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as verr:
            verr.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(verr)

    def save(self):
        return forms.models.ModelForm.save(self)


class NewListForm(ItemForm):

    def save(self, owner):
        if owner.is_authenticated():
            List.create_new(
                first_item_text=self.cleaned_data['text'],
                owner=owner
            )
        else:
            List.create_new(
                first_item_text=self.cleaned_data['text'],
            )
