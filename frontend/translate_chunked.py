#!/usr/bin/env python3
"""
Translate contentData.json in chunks with progress saving
"""
import json
from deep_translator import GoogleTranslator
import time
import sys
import os

LANGUAGES = {
    'de': ('german', 'contentDataDe.json'),
    'es': ('spanish', 'contentDataEs.json'),
    'fr': ('french', 'contentDataFr.json'),
    'pt': ('portuguese', 'contentDataPt.json'),
    'ru': ('russian', 'contentDataRu.json'),
    'ko': ('korean', 'contentDataKr.json'),
    'ja': ('japanese', 'contentDataJp.json')
}

def load_progress(lang_code):
    """Load existing progress if any"""
    progress_file = f'src/data/.progress_{lang_code}.json'
    if os.path.exists(progress_file):
        with open(progress_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def save_progress(lang_code, data):
    """Save progress to temp file"""
    progress_file = f'src/data/.progress_{lang_code}.json'
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def translate_text(translator, text, retries=3):
    """Translate with retry"""
    if not text:
        return text
    for i in range(retries):
        try:
            return translator.translate(text)
        except Exception as e:
            if i == retries - 1:
                print(f"Failed: {e}")
                return text
            time.sleep(2)
    return text

def translate_language(lang_code):
    """Translate entire content for one language"""
    if lang_code not in LANGUAGES:
        print(f"Invalid language code: {lang_code}")
        return False
    
    lang_name, filename = LANGUAGES[lang_code]
    filepath = f'src/data/{filename}'
    
    print(f"\n{'='*60}")
    print(f"TRANSLATING TO {lang_name.upper()}")
    print('='*60)
    
    # Load source
    with open('src/data/contentData.json', 'r', encoding='utf-8') as f:
        source = json.load(f)
    
    # Check for existing progress
    progress = load_progress(lang_code)
    if progress:
        print(f"Found existing progress, resuming...")
        translated = progress
    else:
        translated = {'visualStyles': [], 'hooks': [], 'scripts': []}
    
    translator = GoogleTranslator(source='en', target=lang_code)
    
    # Translate Visual Styles
    if len(translated['visualStyles']) < len(source['visualStyles']):
        start = len(translated['visualStyles'])
        print(f"\nTranslating Visual Styles ({start}/{len(source['visualStyles'])} done)...")
        for i in range(start, len(source['visualStyles'])):
            style = source['visualStyles'][i]
            print(f"  {i+1}/{len(source['visualStyles'])}: {style['title'][:35]}...", end=' ', flush=True)
            new_style = style.copy()
            new_style['title'] = translate_text(translator, style['title'])
            if style.get('info'):
                new_style['info'] = translate_text(translator, style['info'])
            translated['visualStyles'].append(new_style)
            print("✓")
            time.sleep(0.1)
        save_progress(lang_code, translated)
    
    # Translate Hooks
    if len(translated['hooks']) < len(source['hooks']):
        start = len(translated['hooks'])
        print(f"\nTranslating Hooks ({start}/{len(source['hooks'])} done)...")
        for i in range(start, len(source['hooks'])):
            hook = source['hooks'][i]
            print(f"  {i+1}/{len(source['hooks'])}: {hook['idea'][:35]}...", end=' ', flush=True)
            new_hook = hook.copy()
            new_hook['idea'] = translate_text(translator, hook['idea'])
            if hook.get('notes'):
                new_hook['notes'] = translate_text(translator, hook['notes'])
            translated['hooks'].append(new_hook)
            print("✓")
            time.sleep(0.1)
        save_progress(lang_code, translated)
    
    # Translate Scripts
    if len(translated['scripts']) < len(source['scripts']):
        start = len(translated['scripts'])
        print(f"\nTranslating Scripts ({start}/{len(source['scripts'])} done)...")
        for i in range(start, len(source['scripts'])):
            script = source['scripts'][i]
            if i % 10 == 0:
                print(f"  {i+1}/{len(source['scripts'])}: {script['paragraph1'][:35]}...", end=' ', flush=True)
            new_script = script.copy()
            new_script['paragraph1'] = translate_text(translator, script['paragraph1'])
            new_script['paragraph2'] = translate_text(translator, script['paragraph2'])
            if script.get('notes'):
                new_script['notes'] = translate_text(translator, script['notes'])
            translated['scripts'].append(new_script)
            if i % 10 == 0:
                print("✓")
            time.sleep(0.05)
            # Save every 50 scripts
            if (i + 1) % 50 == 0:
                save_progress(lang_code, translated)
        save_progress(lang_code, translated)
    
    # Final save
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(translated, f, indent=2, ensure_ascii=False)
    
    # Clean up progress file
    progress_file = f'src/data/.progress_{lang_code}.json'
    if os.path.exists(progress_file):
        os.remove(progress_file)
    
    print(f"\n✓ {lang_name} translation complete! Saved to {filepath}")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 translate_chunked.py <lang_code|all>")
        print(f"Supported: {list(LANGUAGES.keys())} or 'all'")
        sys.exit(1)
    
    lang = sys.argv[1]
    
    if lang == 'all':
        for code in LANGUAGES.keys():
            translate_language(code)
            time.sleep(5)  # Pause between languages
    else:
        translate_language(lang)

if __name__ == '__main__':
    main()
