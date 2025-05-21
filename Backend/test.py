from books.models import Books

for book in Books.objects.all():
    if book.recommended_song and "{URL" in book.recommended_song:
        start = book.recommended_song.find("https://")
        end = book.recommended_song.find("}", start)
        clean_url = book.recommended_song[start:end] if end != -1 else book.recommended_song[start:]
        book.recommended_song = clean_url.strip()
        book.save()