# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_product_type_and_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='produto_cliente',
            field=models.BooleanField(
                default=False,
                help_text='Marca este produto como o produto cliente base para comparações',
                verbose_name='Produto Cliente Base'
            ),
        ),
    ]