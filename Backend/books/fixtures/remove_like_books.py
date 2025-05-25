import json

# books.json 파일 읽기
with open('books.json', 'r', encoding='utf-8') as f:
    books_data = json.load(f)

# 각 책 데이터에서 like_books 필드 제거
for book in books_data:
    if 'fields' in book and 'like_books' in book['fields']:
        del book['fields']['like_books']

# 수정된 데이터를 다시 파일에 저장
with open('books.json', 'w', encoding='utf-8') as f:
    json.dump(books_data, f, ensure_ascii=False, indent=4) 