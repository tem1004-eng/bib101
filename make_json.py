import json
import re
import os

def convert_bible():
    input_file = r"C:\boga\개역개정.txt"
    output_file = r"C:\boga\my_bible.json"
    
    # 성경 데이터를 담을 구조
    bible_structure = []
    book_map = {} 
    
    # 정규표현식 설명: [책이름][숫자]:[숫자][공백][본문]
    # 예: 창1:1 태초에... / 창세기 1:1 태초에... 모두 인식
    pattern = re.compile(r"([가-힣]+)\s*(\d+)[:|](\d+)\s*(.*)")

    if not os.path.exists(input_file):
        print(f"❌ 파일을 찾을 수 없습니다: {input_file}")
        print("파일명이 '개역개정.txt'가 맞는지, C:\\boga 폴더에 있는지 확인해주세요.")
        return

    # 인코딩 문제 해결 (UTF-8 먼저 시도 후 실패 시 CP949 시도)
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='cp949') as f:
            lines = f.readlines()

    print("🔄 변환을 시작합니다...")

    for line in lines:
        line = line.strip()
        if not line: continue
        
        match = pattern.search(line)
        if match:
            book_name, chapter_str, verse_str, text = match.groups()
            chapter_num = int(chapter_str) - 1
            
            # 새로운 성경 책이 나오면 등록
            if book_name not in book_map:
                book_map[book_name] = len(bible_structure)
                bible_structure.append({
                    "book_name": book_name,
                    "chapters": []
                })
            
            book_idx = book_map[book_name]
            chapters = bible_structure[book_idx]["chapters"]
            
            # 장(Chapter) 배열 크기 맞추기
            while len(chapters) <= chapter_num:
                chapters.append([])
            
            # 절(Verse) 추가
            chapters[chapter_num].append(text)

    # JSON 파일 저장
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(bible_structure, f, ensure_ascii=False, indent=4)
        
    print(f"✅ 변환 완료! '{output_file}' 파일이 생성되었습니다.")

if __name__ == "__main__":
    convert_bible()