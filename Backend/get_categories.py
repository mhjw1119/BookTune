import json

# JSON 파일 읽기
with open('books/fixtures/books.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 카테고리 이름 추출
categories = set()
for item in data:
    category = item['fields'].get('category_name')
    if category:
        categories.add(category)

# 정렬된 카테고리 목록 출력
print("\n유니크한 카테고리 목록:")
for category in sorted(categories):
    print(f"- {category}")
print(f"\n총 {len(categories)}개의 카테고리가 있습니다.") 