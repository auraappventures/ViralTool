#!/usr/bin/env python3
"""
Fix brand name capitalization in translations
"""
import json
import re

def fix_brand_names(text):
    """Fix brand name capitalization"""
    if not text:
        return text
    
    # Fix TikTok capitalization
    text = re.sub(r'\btiktok\b', 'TikTok', text, flags=re.IGNORECASE)
    text = re.sub(r'\btik tok\b', 'TikTok', text, flags=re.IGNORECASE)
    
    # Fix She's Viral capitalization (keep as is in non-Latin scripts)
    text = re.sub(r"she's viral", "She's Viral", text, flags=re.IGNORECASE)
    text = re.sub(r"she's viral", "She's Viral", text, flags=re.IGNORECASE)
    
    return text

def process_file(filepath):
    """Process a translation file"""
    print(f"Processing {filepath}...")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Fix visual styles
    for item in data['visualStyles']:
        item['title'] = fix_brand_names(item['title'])
        if item.get('info'):
            item['info'] = fix_brand_names(item['info'])
    
    # Fix hooks
    for item in data['hooks']:
        item['idea'] = fix_brand_names(item['idea'])
        if item.get('notes'):
            item['notes'] = fix_brand_names(item['notes'])
    
    # Fix scripts
    for item in data['scripts']:
        item['paragraph1'] = fix_brand_names(item['paragraph1'])
        item['paragraph2'] = fix_brand_names(item['paragraph2'])
        if item.get('notes'):
            item['notes'] = fix_brand_names(item['notes'])
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ Fixed brand names in {filepath}")

def main():
    files = [
        'src/data/contentDataDe.json',
        'src/data/contentDataEs.json',
        'src/data/contentDataFr.json',
        'src/data/contentDataPt.json',
        'src/data/contentDataRu.json',
        'src/data/contentDataKr.json',
        'src/data/contentDataJp.json',
    ]
    
    for filepath in files:
        process_file(filepath)
    
    print("\n✅ Brand name capitalization fixed in all files!")

if __name__ == '__main__':
    main()
