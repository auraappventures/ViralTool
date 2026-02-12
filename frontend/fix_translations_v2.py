#!/usr/bin/env python3
"""
Fix translations to be more natural for Gen Z TikTok content
"""
import json
import re

def fix_german(text):
    """Fix German translations to sound more natural"""
    if not text:
        return text
    
    # Keep English terms that Gen Z uses
    replacements = {
        # Slang - keep English or use natural German
        'den Tee verschütten': 'Klatsch ausplaudern',
        'Situationsbeziehung': 'Situationship',
        'posten und geistern': 'posten und ghosten',
        'explodieren': 'viral gehen',
        'explodiert': 'viral gegangen',
        'explodierte': 'viral gegangen',
        'Keine Kappe': 'Ernsthaft',
        'keine Kappe': 'ernsthaft',
        'Hauptcharakter-Energie': 'Main Character Energy',
        'mietfrei leben': 'geht mir nicht aus dem Kopf',
        'es gibt': 'es hat so',
        'die Aufgabe verstanden': 'hat die Aufgabe verstanden',
        
        # TikTok specific
        'Tiktok': 'TikTok',
        'tiktok': 'TikTok',
        'Algorithmus': 'Algorithmus',
        'Engagement': 'Engagement',
        'Views': 'Views',
        'Follower': 'Follower',
        'Creator': 'Creator',
        
        # Common awkward translations
        'höchste bezahlte': 'bestbezahlte',
        'sich lustig machen über': 'hatern',
        'in die DMs rutschen': 'in die DMs slidet',
        'Wachstumsstrategie': 'Growth-Strategie',
        'Geist': 'Ghost',
        'Geister': 'Ghosten',
        
        # Fix weird literal translations
        'grüne Kleidung': 'grüne Outfits',
        'Toiletten-Scroll-Theorie': 'Toiletten-Scroll-Theorie',
        'weicher Shadowban': 'Shadowban',
        'Klangwellen-Hacking': 'Audio-Hacking',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text

def fix_spanish(text):
    """Fix Spanish translations"""
    if not text:
        return text
    
    replacements = {
        # Slang
        'derramando el té': 'contando los secretos',
        'relación de situación': 'situationship',
        'postear y desaparecer': 'postear y ghostear',
        'postear y fantasma': 'postear y ghostear',
        'hacerse viral': 'viralizarse',
        'sin gorra': 'en serio',
        'energía de personaje principal': 'main character energy',
        'viviendo sin pagar alquiler': 'no puedo dejar de pensar en',
        'lo está dando': 'tiene vibes de',
        
        # TikTok terms
        'Tiktok': 'TikTok',
        'vistas': 'views',
        'seguidores': 'followers',
        'creador de contenido': 'creador',
        'algoritmo': 'algoritmo',
        'interacción': 'engagement',
        
        # Common fixes
        'deslizándose en los DMs': 'entrando al DM',
        'estrategia de crecimiento': 'estrategia de growth',
        'fantasma': 'ghost',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text

def fix_french(text):
    """Fix French translations"""
    if not text:
        return text
    
    replacements = {
        # Slang
        'renverser le thé': 'révéler les secrets',
        'relation de situation': 'situationship',
        'poster et disparaître': 'poster et ghoster',
        'devenir viral': 'devenir viral',
        'sans casquette': 'sérieux',
        'énergie de personnage principal': 'main character energy',
        "vivre sans payer de loyer": "j'arrive pas à oublier",
        'il donne': 'ça donne des vibes',
        
        # TikTok terms
        'Tiktok': 'TikTok',
        'vues': 'views',
        'abonnés': 'followers',
        'créateur de contenu': 'créateur',
        'algorithme': 'algorithme',
        'engagement': 'engagement',
        
        # Common fixes
        'glisser dans les DMs': 'glisser dans les DMs',
        'stratégie de croissance': 'stratégie de growth',
        'fantôme': 'ghost',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text

def fix_portuguese(text):
    """Fix Portuguese translations"""
    if not text:
        return text
    
    replacements = {
        # Slang
        'derramando o chá': 'contando os segredos',
        'relação de situação': 'situationship',
        'postar e sumir': 'postar e ghostar',
        'viralizar': 'viralizar',
        'sem boné': 'sério',
        'energia de personagem principal': 'main character energy',
        'morando de aluguel grátis': 'não consigo parar de pensar',
        'está dando': 'tá com vibes de',
        
        # TikTok terms
        'Tiktok': 'TikTok',
        'visualizações': 'views',
        'seguidores': 'followers',
        'criador de conteúdo': 'criador',
        'algoritmo': 'algoritmo',
        'engajamento': 'engajamento',
        
        # Common fixes
        'mandar DM': 'mandar DM',
        'estratégia de crescimento': 'estratégia de growth',
        'fantasma': 'ghost',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text

def fix_russian(text):
    """Fix Russian translations"""
    if not text:
        return text
    
    replacements = {
        # Slang - use transliteration or natural Russian
        'проливая чай': 'раскрываю секреты',
        'ситуационные отношения': 'ситуэйшеншип',
        'постить и призрак': 'постить и пропадать',
        'постить и исчезать': 'постить и пропадать',
        'стать вирусным': 'залететь',
        'без шапки': 'без шуток',
        'энергия главного героя': 'энергия главного героя',
        'жить бесплатно': 'не выходит из головы',
        'это даёт': 'это даёт вайбы',
        
        # TikTok terms
        'Тикток': 'TikTok',
        'тикток': 'TikTok',
        'просмотры': 'просмотры',
        'подписчики': 'подписчики',
        'креатор': 'креатор',
        'алгоритм': 'алгоритм',
        'вовлечённость': 'вовлечённость',
        
        # Common fixes
        'в личку': 'в личку',
        'стратегия роста': 'стратегия роста',
        'призрак': 'ghost',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text

def fix_korean(text):
    """Fix Korean translations"""
    if not text:
        return text
    
    replacements = {
        # Slang - mix of Korean and English loanwords
        '차를 엎지르는': '남들 모르는 얘기',
        '상황 관계': '상황관계',
        '게시하고 사라지기': '올리고 사라지기',
        '게시하고 유령': '올리고 고스트',
        '바이럴 되다': '떡상하다',
        '모자 없이': '진짜로',
        '주인공 에너지': '주인공 에너지',
        '공짜로 살기': '머리에서 안 떠나',
        '그것은 주고 있다': '분위기가',
        
        # TikTok terms
        '틱톡': 'TikTok',
        '조회수': '조회수',
        '팔로워': '팔로워',
        '크리에이터': '크리에이터',
        '알고리즘': '알고리즘',
        '참여도': '참여도',
        
        # Common fixes
        'DM으로 미끄러지기': 'DM으로 슬라이딩',
        '성장 전략': '성장 전략',
        '유령': '고스트',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text

def fix_japanese(text):
    """Fix Japanese translations"""
    if not text:
        return text
    
    replacements = {
        # Slang - use katakana for loanwords
        'お茶をこぼす': '裏話を暴露',
        '状況関係': 'シチュエーションシップ',
        '投稿して幽霊': '投稿してゴースト',
        '投稿して消える': '投稿してゴースト',
        'バズる': 'バズる',
        'キャップなし': 'マジで',
        '主役のエネルギー': '主役オーラ',
        '家賃無しで住む': '頭から離れない',
        'それを与えている': '〜な感じ',
        
        # TikTok terms
        'ティックトック': 'TikTok',
        'ティクトク': 'TikTok',
        'ビュー': '再生数',
        'フォロワー': 'フォロワー',
        'クリエイター': 'クリエイター',
        'アルゴリズム': 'アルゴリズム',
        'エンゲージメント': 'エンゲージメント',
        
        # Common fixes
        'DMに滑り込む': 'DMイン',
        '成長戦略': 'グロース戦略',
        '幽霊': 'ゴースト',
    }
    
    for wrong, right in replacements.items():
        text = text.replace(wrong, right)
    
    return text

def fix_file(filename, fix_func):
    """Fix translations in a file"""
    print(f"Fixing {filename}...")
    
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fix visual styles
    for item in data['visualStyles']:
        item['title'] = fix_func(item['title'])
        if item.get('info'):
            item['info'] = fix_func(item['info'])
    
    # Fix hooks
    for item in data['hooks']:
        item['idea'] = fix_func(item['idea'])
        if item.get('notes'):
            item['notes'] = fix_func(item['notes'])
    
    # Fix scripts
    for item in data['scripts']:
        item['paragraph1'] = fix_func(item['paragraph1'])
        item['paragraph2'] = fix_func(item['paragraph2'])
        if item.get('notes'):
            item['notes'] = fix_func(item['notes'])
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Fixed {filename}")

def main():
    fixes = [
        ('src/data/contentDataDe.json', fix_german),
        ('src/data/contentDataEs.json', fix_spanish),
        ('src/data/contentDataFr.json', fix_french),
        ('src/data/contentDataPt.json', fix_portuguese),
        ('src/data/contentDataRu.json', fix_russian),
        ('src/data/contentDataKr.json', fix_korean),
        ('src/data/contentDataJp.json', fix_japanese),
    ]
    
    for filename, fix_func in fixes:
        fix_file(filename, fix_func)
    
    print("\n✅ All translation files improved!")
    print("\nKey improvements:")
    print("- Gen Z slang sounds more natural")
    print("- English terms kept where Gen Z uses them")
    print("- TikTok-specific terms corrected")
    print("- Awkward literal translations fixed")

if __name__ == '__main__':
    main()
