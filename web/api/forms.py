from django import forms
from .models import cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = cliente
        exclude = ['status', 'query_date']

    def clean(self):
        # funcion para la validacion
        super(ClienteForm, self).clean()
        dnilen = len(str(self.cleaned_data.get('dni')))
        monto = self.cleaned_data.get('monto')

        if dnilen > 8 or dnilen < 6:
            self._errors['dni'] = self.error_class([
                'DNI debe tener entre 6 y 8 digitos'])

        if monto > 1000000 or monto < 100:
            self._errors['monto'] = self.error_class([
                'Monto inválido'])

        return self.cleaned_data