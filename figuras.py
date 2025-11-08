from wtforms import Form, FloatField, validators

class FigurasForm(Form):
    valor1 = FloatField('Valor 1', [validators.Optional()])
    valor2 = FloatField('Valor 2', [validators.Optional()])
