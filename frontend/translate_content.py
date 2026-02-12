#!/usr/bin/env python3
"""
Translate contentData.json to multiple languages
"""
import json
from deep_translator import GoogleTranslator
import os

# Languages to translate to
LANGUAGES = {
    'de': 'german',      # German
    'es': 'spanish',     # Spanish
    'fr': 'french',      # French
    'pt': 'portuguese',  # Portuguese
    'ru': 'russian',     # Russian
    'ko': 'korean',      # Korean
    'ja': 'japanese'     # Japanese
}

def translate_text(text, target_lang):
    """Translate text to target language"""
    if not text or text == '-' or text.strip() == '':
        return text
    try:
        translator = GoogleTranslator(source='en', target=target_lang)
        return translator.translate(text)
    except Exception as e:
        print(f"Error translating '{text[:50]}...' to {target_lang}: {e}")
        return text

def translate_visual_styles(visual_styles, target_lang):
    """Translate visual styles section"""
    translated = []
    for style in visual_styles:
        new_style = style.copy()
        new_style['title'] = translate_text(style['title'], target_lang)
        if style.get('info'):
            new_style['info'] = translate_text(style['info'], target_lang)
        translated.append(new_style)
    return translated

def translate_hooks(hooks, target_lang):
    """Translate hooks section"""
    translated = []
    for hook in hooks:
        new_hook = hook.copy()
        new_hook['idea'] = translate_text(hook['idea'], target_lang)
        if hook.get('notes'):
            new_hook['notes'] = translate_text(hook['notes'], target_lang)
        translated.append(new_hook)
    return translated

def translate_scripts(scripts, target_lang):
    """Translate scripts section"""
    translated = []
    for script in scripts:
        new_script = script.copy()
        new_script['paragraph1'] = translate_text(script['paragraph1'], target_lang)
        new_script['paragraph2'] = translate_text(script['paragraph2'], target_lang)
        if script.get('notes'):
            new_script['notes'] = translate_text(script['notes'], target_lang)
        translated.append(new_script)
    return translated

def translate_content(data, target_lang):
    """Translate all content to target language"""
    print(f"Translating to {LANGUAGES[target_lang]} ({target_lang})...")
    
    translated_data = {
        'visualStyles': translate_visual_styles(data['visualStyles'], target_lang),
        'hooks': translate_hooks(data['hooks'], target_lang),
        'scripts': translate_scripts(data['scripts'], target_lang)
    }
    
    return translated_data

def main():
    # Read source file
    with open('src/data/contentData.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"Loaded {len(data['visualStyles'])} visual styles")
    print(f"Loaded {len(data['hooks'])} hooks")
    print(f"Loaded {len(data['scripts'])} scripts")
    print()
    
    # Translate to each language
    for lang_code, lang_name in LANGUAGES.items():
        print(f"\n{'='*60}")
        print(f"Processing {lang_name.upper()}")
        print('='*60)
        
        # Translate content
        translated = translate_content(data, lang_code)
        
        # Determine filename
        if lang_code == 'de':
            filename = 'contentDataDe.json'
        elif lang_code == 'es':
            filename = 'contentDataEs.json'
        elif lang_code == 'fr':
            filename = 'contentDataFr.json'
        elif lang_code == 'pt':
            filename = 'contentDataPt.json'
        elif lang_code == 'ru':
            filename = 'contentDataRu.json'
        elif lang_code == 'ko':
            filename = 'contentDataKr.json'
        elif lang_code == 'ja':
            filename = 'contentDataJp.json'
        else:
            filename = f'contentData_{lang_code}.json'
        
        filepath = f'src/data/{filename}'
        
        # Write translated file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(translated, f, indent=2, ensure_ascii=False)
        
        print(f"✓ Saved to {filepath}")
    
    print(f"\n{'='*60}")
    print("Translation complete!")
    print('='*60)

if __name__ == '__main__':
    main()
