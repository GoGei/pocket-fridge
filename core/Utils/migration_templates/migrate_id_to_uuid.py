"""
Template of how ID can be migrated to UUID
"""

import uuid
from django.db import migrations, models


def fill_id_with_uuid(apps, schema_editor):
    Model = apps.get_model('Model', 'Model')
    Related = apps.get_model('Related', 'Related')

    for item in Model.objects.all():
        old_obj_id = item.id

        qs = Related.objects.select_related('model').filter(model=item)
        item.id = uuid.uuid4()
        item.save()
        qs.update(model=item)

        Model.objects.filter(id=old_obj_id).first().delete()


OPERATIONS = [
    migrations.AlterField(
        model_name='modename',
        name='id',
        field=models.CharField(auto_created=True, max_length=36, primary_key=True, serialize=False),
    ),
    migrations.RunPython(fill_id_with_uuid),
    # separate to 2nd migration
    # https://docs.djangoproject.com/en/dev/ref/migration-operations/#runpython
    migrations.AlterField(
        model_name='modename',
        name='id',
        field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
    ),
]
