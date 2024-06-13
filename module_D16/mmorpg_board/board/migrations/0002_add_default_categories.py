from django.db import migrations

def create_categories(apps, schema_editor):
    Category = apps.get_model('board', 'Category')
    categories = ['Танки', 'Хилы', 'ДД', 'Торговцы', 'Гилдмастеры', 'Квестгиверы', 'Кузнецы', 'Кожевники', 'Зельевары', 'Мастера заклинаний']
    for category in categories:
        Category.objects.create(name=category)

class Migration(migrations.Migration):

    dependencies = [
        ('board', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_categories),
    ]
