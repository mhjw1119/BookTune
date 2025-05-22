from django.db import migrations

def remove_author_suffix(apps, schema_editor):
    Books = apps.get_model('books', 'Books')
    for book in Books.objects.all():
        author = book.author
        author = author.replace('(지은이)', '').replace('(옮긴이)', '').strip()
        book.author = author
        book.save()

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_books_main_category'),
    ]

    operations = [
        migrations.RunPython(remove_author_suffix),
    ] 