from django.forms import ModelForm, ValidationError
from MainApp.models import Snippet


class SnippetForm(ModelForm):
    class Meta:
        model = Snippet
        # Описываем поля, которые будем заполнять в форме
        fields = ['name', 'lang', 'code']
        # Или исключаем поля
#        exclude=['creation_date']

    def clean_name(self):
        """ Метод для проверки длины поля ‹name> """
        snippet_name = self.cleaned_data.get("name")
        if snippet_name is not None and len(snippet_name) > 3:
            return snippet_name
        raise ValidationError("Snippet`s name too short.")
