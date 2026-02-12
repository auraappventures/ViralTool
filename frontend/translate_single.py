#!/usr/bin/env python3
"""
Translate contentData.json to a single language - for testing
"""
import json
from deep_translator import GoogleTranslator
import time
import sys

# Supported languages
LANGUAGES = {
    'de': ('german', 'contentDataDe.json'),
    'es': ('spanish', 'contentDataEs.json'),
    'fr': ('french', 'contentDataFr.json'),
    'pt': ('portuguese', 'contentDataPt.json'),
    'ru': ('russian', 'contentDataRu.json'),
    'ko': ('korean', 'contentDataKr.json'),
    'ja': ('japanese', 'contentDataJp.json')
}

def translate_batch(translator, texts, batch_size=5):
    """Translate multiple texts with rate limiting"""
    results = []
    for i, text in enumerate(texts):
        if not text:
            results.append(text)
            continue
        try:
            result = translator.translate(text)
            results.append(result)
            if (i + 1) % batch_size == 0:
                time.sleep(1)  # Rate limit every batch
        except Exception as e:
            print(f"Error translating: {e}")
            results.append(text)
    return results

def translate_language(lang_code):
    """Translate content to a single language"""
    if lang_code not in LANGUAGES:
        print(f"Unsupported language code: {lang_code}")
        print(f"Supported: {list(LANGUAGES.keys())}")
        return
    
    lang_name, filename = LANGUAGES[lang_code]
    
    print(f"Loading source file...")
    with open('src/data/contentData.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"\nTranslating to {lang_name.upper()} ({lang_code})...")
    print(f"Items to translate: {len(data['visualStyles'])} styles + {len(data['hooks'])} hooks + {len(data['scripts'])} scripts")
    
    translator = GoogleTranslator(source='en', target=lang_code)
    
    # Translate visual styles
    print("\n1. Translating Visual Styles...")
    visual_styles = []
    for i, style in enumerate(data['visualStyles']):
        print(f"   {i+1}/{len(data['visualStyles'])}: {style['title'][:30]}...", end=' ', flush=True)
        new_style = style.copy()
        new_style['title'] = translator.translate(style['title'])
        if style.get('info'):
            new_style['info'] = translator.translate(style['info'])
        visual_styles.append(new_style)
        print("✓")
        time.sleep(0.2)
    
    # Translate hooks
    print("\n2. Translating Hooks...")
    hooks = []
    for i, hook in enumerate(data['hooks']):
        print(f"   {i+1}/{len(data['hooks'])}: {hook['idea'][:30]}...", end=' ', flush=True)
        new_hook = hook.copy()
        new_hook['idea'] = translator.translate(hook['idea'])
        if hook.get('notes'):
            new_hook['notes'] = translator.translate(hook['notes'])
        hooks.append(new_hook)
        print("✓")
        time.sleep(0.2)
    
    # Translate scripts
    print("\n3. Translating Scripts...")
    scripts = []
    for i, script in enumerate(data['scripts']):
        print(f"   {i+1}/{len(data['scripts'])}: {script['paragraph1'][:30]}...", end=' ', flush=True)
        new_script = script.copy()
        new_script['paragraph1'] = translator.translate(script['paragraph1'])
        new_script['paragraph2'] = translator.translate(script['paragraph2'])
        if script.get('notes'):
            new_script['notes'] = translator.translate(script['notes'])
        scripts.append(new_script)
        print("✓")
        time.sleep(0.2)
    
    # Save
    translated_data = {
        'visualStyles': visual_styles,
        'hooks': hooks,
        'scripts': scripts
    }
    
    filepath = f'src/data/{filename}'
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(translated_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✓ Saved to {filepath}")
    print(f"Translation to {lang_name} complete!")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 translate_single.py <language_code>")
        print(f"Supported codes: {list(LANGUAGES.keys())}")
        sys.exit(1)
    
    translate_language(sys.argv[1])
