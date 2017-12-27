from django.forms import Form
from django.forms import IntegerField,CharField,DateTimeField

class ModifyForm(Form):
    title = CharField(max_length=50)
    content = CharField(max_length=500)
    pid = IntegerField()
    update_time = DateTimeField()