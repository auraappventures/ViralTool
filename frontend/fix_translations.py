#!/usr/bin/env python3
"""
Fix common translation errors in Gen Z content
"""
import json
import re

# Common fixes for each language
FIXES = {
    'de': {
        'Tee verschütten': 'Klatsch ausplaudern',
        'Situationsbeziehung': 'Situationship',
        'Geister': 'ghosten',
        'explodieren': 'viral gehen',
        'höchste bezahlte': 'bestbezahlte',
        'Tiktok': 'TikTok',
        'sich lustig machen über': 'hatern auf',
    },
    'es': {
        'derramando el té': 'contando secretos',
        'relación de situación': 'situationship',
        'fantasma': 'desaparecer',
        'explotar': 'hacerse viral',
    },
    'fr': {
        'renverser le thé': 'révéler les secrets',
        'relation de situation': 'situationship',
        'fantôme': 'disparaître',
        'exploser': 'devenir viral',
    },
    'pt': {
        'derramando o chá': 'contando segredos',
        'relação de situação': 'situationship',
        'fantasma': 'sumir',
        'explodir': 'viralizar',
    },
    'ru': {
        'проливая чай': 'раскрываю секреты',
        'ситуационные отношения': 'ситуэйшеншип',
        'призрак': 'пропадать',
        'взорваться': 'стать вирусным',
    },
    'ko': {
        '차를 엎지르는': '남들 모르는 얘기',
        '상황 관계': '상황관계',
        '유령': '사라지기',
        '폭발하다': '바이럴 되다',
    },
    'ja': {
        'お茶をこぼす': '裏話を暴露',
        '状況関係': 'シチュエーションシップ',
        '幽霊': 'ゴースト',
        '爆発する': 'バズる',
    }
}

def fix_text(text, lang):
    """Apply fixes to text"""
    if not text:
        return text
    
    fixes = FIXES.get(lang, {})
    for wrong, right in fixes.items():
        text = text.replace(wrong, right)
        text = text.replace(wrong.capitalize(), right.capitalize())
        text = text.replace(wrong.upper(), right.upper())
        text = text.replace(wrong.lower(), right.lower())
    
    # Fix TikTok capitalization
    text = re.sub(r'\btiktok\b', 'TikTok', text, flags=re.IGNORECASE)
    text = re.sub(r'\btik tok\b', 'TikTok', text, flags=re.IGNORECASE)
    
    return text

def fix_file(filename, lang):
    """Fix translations in a file"""
    print(f"Fixing {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fix visual styles
    for item in data['visualStyles']:
        item['title'] = fix_text(item['title'], lang)
        if item.get('info'):
            item['info'] = fix_text(item['info'], lang)
    
    # Fix hooks
    for item in data['hooks']:
        item['idea'] = fix_text(item['idea'], lang)
        if item.get('notes'):
            item['notes'] = fix_text(item['notes'], lang)
    
    # Fix scripts
    for item in data['scripts']:
        item['paragraph1'] = fix_text(item['paragraph1'], lang)
        item['paragraph2'] = fix_text(item['paragraph2'], lang)
        if item.get('notes'):
            item['notes'] = fix_text(item['notes'], lang)
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Fixed {filename}")

def main():
    files = [
        ('src/data/contentDataDe.json', 'de'),
        ('src/data/contentDataEs.json', 'es'),
        ('src/data/contentDataFr.json', 'fr'),
        ('src/data/contentDataPt.json', 'pt'),
        ('src/data/contentDataRu.json', 'ru'),
        ('src/data/contentDataKr.json', 'ko'),
        ('src/data/contentDataJp.json', 'ja'),
    ]
    
    for filename, lang in files:
        fix_file(filename, lang)
    
    print("\n✓ All files fixed!")

if __name__ == '__main__':
    main()
