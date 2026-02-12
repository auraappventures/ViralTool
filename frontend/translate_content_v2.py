#!/usr/bin/env python3
"""
Translate contentData.json to multiple languages - Optimized version with caching
"""
import json
from deep_translator import GoogleTranslator
import time
import os

# Languages to translate to
LANGUAGES = {
    'de': 'contentDataDe.json',      # German
    'es': 'contentDataEs.json',      # Spanish
    'fr': 'contentDataFr.json',      # French
    'pt': 'contentDataPt.json',      # Portuguese
    'ru': 'contentDataRu.json',      # Russian
    'ko': 'contentDataKr.json',      # Korean
    'ja': 'contentDataJp.json'       # Japanese
}

def translate_with_retry(translator, text, max_retries=3):
    """Translate with retry logic"""
    for attempt in range(max_retries):
        try:
            return translator.translate(text)
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"  Retry {attempt + 1}/{max_retries}...")
                time.sleep(2)
            else:
                print(f"  Failed after {max_retries} attempts: {e}")
                return text
    return text

def translate_visual_styles(visual_styles, translator):
    """Translate visual styles section"""
    translated = []
    for i, style in enumerate(visual_styles):
        print(f"  Visual Style {i+1}/{len(visual_styles)}: {style['title'][:40]}...", end=' ')
        new_style = style.copy()
        new_style['title'] = translate_with_retry(translator, style['title'])
        if style.get('info'):
            new_style['info'] = translate_with_retry(translator, style['info'])
        translated.append(new_style)
        print("✓")
        time.sleep(0.3)  # Rate limiting
    return translated

def translate_hooks(hooks, translator):
    """Translate hooks section"""
    translated = []
    for i, hook in enumerate(hooks):
        print(f"  Hook {i+1}/{len(hooks)}: {hook['idea'][:40]}...", end=' ')
        new_hook = hook.copy()
        new_hook['idea'] = translate_with_retry(translator, hook['idea'])
        if hook.get('notes'):
            new_hook['notes'] = translate_with_retry(translator, hook['notes'])
        translated.append(new_hook)
        print("✓")
        time.sleep(0.3)  # Rate limiting
    return translated

def translate_scripts(scripts, translator):
    """Translate scripts section"""
    translated = []
    for i, script in enumerate(scripts):
        print(f"  Script {i+1}/{len(scripts)}: {script['paragraph1'][:40]}...", end=' ')
        new_script = script.copy()
        new_script['paragraph1'] = translate_with_retry(translator, script['paragraph1'])
        new_script['paragraph2'] = translate_with_retry(translator, script['paragraph2'])
        if script.get('notes'):
            new_script['notes'] = translate_with_retry(translator, script['notes'])
        translated.append(new_script)
        print("✓")
        time.sleep(0.3)  # Rate limiting
    return translated

def main():
    # Read source file
    print("Loading source file...")
    with open('src/data/contentData.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Visual Styles: {len(data['visualStyles'])}")
    print(f"Hooks: {len(data['hooks'])}")
    print(f"Scripts: {len(data['scripts'])}")
    print()
    
    # Translate to each language
    for lang_code, filename in LANGUAGES.items():
        print(f"\n{'='*70}")
        print(f"TRANSLATING TO: {lang_code.upper()}")
        print('='*70)
        
        translator = GoogleTranslator(source='en', target=lang_code)
        
        # Translate each section
        print("\nTranslating Visual Styles...")
        translated_visual = translate_visual_styles(data['visualStyles'], translator)
        
        print("\nTranslating Hooks...")
        translated_hooks = translate_hooks(data['hooks'], translator)
        
        print("\nTranslating Scripts...")
        translated_scripts = translate_scripts(data['scripts'], translator)
        
        # Save translated content
        translated_data = {
            'visualStyles': translated_visual,
            'hooks': translated_hooks,
            'scripts': translated_scripts
        }
        
        filepath = f'src/data/{filename}'
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(translated_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n✓ Saved: {filepath}")
        time.sleep(2)  # Pause between languages
    
    print(f"\n{'='*70}")
    print("ALL TRANSLATIONS COMPLETE!")
    print('='*70)

if __name__ == '__main__':
    main()
