from django.core.management import call_command
from django.core.serializers import base, python


def load_fixture(apps, fixture, app_label):
    """
    Example of usage in migrations:

    from core.Utils.migration import load_fixture as load


    def load_fixture(apps, schema_editor):
        load(apps, 'your_data', 'ModelName')


    class Migration(migrations.Migration):
        operations = [
            migrations.RunPython(load_fixture)
        ]
    """
    # Save the old _get_model() function
    old_get_model = python._get_model

    # Define new _get_model() function here, which utilizes the apps argument to
    # get the historical version of a model. This piece of code is directly stolen
    # from django.core.serializers.python._get_model, unchanged. However, here it
    # has a different context, specifically, the apps variable.
    def _get_model(model_identifier):
        try:
            return apps.get_model(model_identifier)
        except (LookupError, TypeError):
            raise base.DeserializationError("Invalid model identifier: '%s'" % model_identifier)

    #  Replace the _get_model() function on the module, so loaddata can utilize it.
    python._get_model = _get_model
    try:
        # Call loaddata command
        call_command('loaddata', fixture, app_label=app_label)
    finally:
        # Restore old _get_model() function
        python._get_model = old_get_model
