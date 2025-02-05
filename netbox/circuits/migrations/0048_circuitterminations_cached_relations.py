import django.db.models.deletion
from django.db import migrations, models


def populate_denormalized_fields(apps, schema_editor):
    """
    Copy site ForeignKey values to the Termination GFK.
    """
    CircuitTermination = apps.get_model('circuits', 'CircuitTermination')

    terminations = CircuitTermination.objects.filter(site__isnull=False).prefetch_related('site')
    for termination in terminations:
        termination._region_id = termination.site.region_id
        termination._site_group_id = termination.site.group_id
        termination._site_id = termination.site_id
        # Note: Location cannot be set prior to migration

    CircuitTermination.objects.bulk_update(terminations, ['_region', '_site_group', '_site'], batch_size=100)


class Migration(migrations.Migration):
    dependencies = [
        ('circuits', '0047_circuittermination__termination'),
    ]

    operations = [
        migrations.AddField(
            model_name='circuittermination',
            name='_location',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='circuit_terminations',
                to='dcim.location',
            ),
        ),
        migrations.AddField(
            model_name='circuittermination',
            name='_region',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='circuit_terminations',
                to='dcim.region',
            ),
        ),
        migrations.AddField(
            model_name='circuittermination',
            name='_site',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='circuit_terminations',
                to='dcim.site',
            ),
        ),
        migrations.AddField(
            model_name='circuittermination',
            name='_site_group',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='circuit_terminations',
                to='dcim.sitegroup',
            ),
        ),
        # Populate denormalized FK values
        migrations.RunPython(code=populate_denormalized_fields, reverse_code=migrations.RunPython.noop),
        # Delete the site ForeignKey
        migrations.RemoveField(
            model_name='circuittermination',
            name='site',
        ),
        migrations.RenameField(
            model_name='circuittermination',
            old_name='provider_network',
            new_name='_provider_network',
        ),
    ]
