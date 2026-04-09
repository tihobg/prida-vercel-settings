from import_export import resources
from . models import Score, Person


class PersonResource(resources.ModelResource):
    class Meta:
        model = Person
        # fields = '__all__'
