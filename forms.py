from wtforms import Form, StringField, IntegerField, EmailField, validators
from wtforms.fields import DateField, SelectField, SelectMultipleField


class UserForm(Form):
    matricula = IntegerField('Matrícula', [
        validators.DataRequired(message="La matrícula es obligatoria")
    ])
    nombre = StringField('Nombre', [
        validators.DataRequired(message="El nombre es obligatorio")
    ])
    apellido = StringField('Apellido', [
        validators.DataRequired(message="El apellido es obligatorio")
    ])
    correo = EmailField('Correo', [
        validators.DataRequired(message="El correo es obligatorio"),
        validators.Email(message="Debe ser un correo válido")
    ])

class ClienteForm(Form):
    nombre = StringField('Nombre completo', [validators.DataRequired()])
    direccion = StringField('Dirección', [validators.DataRequired()])
    telefono = StringField('Teléfono', [
        validators.DataRequired(),
        validators.Length(min=8, max=15, message="Número de teléfono no válido")
    ])
    
class PizzaForm(Form):
    tamano = SelectField('Tamaño', choices=[
        ('chica', 'Chica'),
        ('mediana', 'Mediana'),
        ('grande', 'Grande')
    ], validators=[validators.DataRequired()])

    ingredientes = SelectMultipleField('Ingredientes', choices=[
        ('jamon', 'Jamón'),
        ('piña', 'Piña'),
        ('champiñones', 'Champiñones')
    ])

    cantidad = IntegerField('Número de pizzas', [validators.DataRequired()])