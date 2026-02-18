# Translation Issues to Fix Manually

## Critical Issues (Should Fix)

### 1. Russian - Too Formal
**Problem:** Russian translations sound too formal/robotic
**Example:** 
- Current: "Вы не сумасшедшие" (You are not crazy - formal)
- Better: "Ты не дурак" (You're not stupid - casual)

**Affected:** ~50 scripts

### 2. Japanese - Character Issues
**Problem:** Some characters may display incorrectly
**Check:** Line 3 in contentDataJp.json has "偽" - verify this is correct

### 3. Korean - Mixed Formality
**Problem:** Mix of formal (존칭) and informal (반말) speech
**Should be:** Consistently informal (반말) for Gen Z audience

### 4. All Languages - "Ich habe bei der Schulung..."
**Problem:** German "Es stellte sich heraus..." sounds like news report
**Better:** "Stellt euch vor, meine Sitznachbarin..." (more conversational)

## Medium Priority (Nice to Have)

### 5. CTA Scripts (Viral Plug) - Tone Check
The most important 10-15 CTA scripts should sound:
- **German:** Young, energetic, not corporate
- **Spanish:** Latin American Spanish (not Spain)
- **French:** Casual "tu" form, not formal "vous"
- **Portuguese:** Brazilian Portuguese
- **Russian:** Informal "ты" not formal "вы"
- **Korean:** 반말 (banmal) not 졌옙 (jondaemal)
- **Japanese:** タメ口 (tameguchi) not 敬語 (keigo)

### 6. Emoji Usage
Some translations may have lost emoji context. Check that:
- ✨ 🎀 💖 🎯 etc. are preserved
- Emotional tone matches original

## Low Priority (Optional)

### 7. Visual Style Titles
Example German:
- "Weißer Titel + weißer Absatz:" 
- Could be: "Weißer Titel + weißer Text:"

### 8. Hook Categories
Category names are still English:
- "Ex TikTok" → Translate or keep?
- "Professor" → Translate or keep?
- Recommendation: Keep English for brand recognition

## Files to Review Priority

1. **contentDataRu.json** - Most formal, needs casual tone
2. **contentDataJp.json** - Check character encoding
3. **contentDataKr.json** - Fix formality consistency
4. **contentDataDe.json** - Check CTA scripts tone

## Quick Test Phrases

Test these specific phrases in each language:

| English | Should Feel Like |
|---------|-----------------|
| "spilling the tea" | Best friend gossiping |
| "she's viral" | Cool app name, not corporate |
| "algorithm" | Tech-savvy creator term |
| "blow up" | Exciting, not explosion |

## My Recommendation

**Don't fix everything manually!** Instead:

1. ✅ **Fix Russian** - Too formal, impacts credibility
2. ✅ **Fix Korean formality** - Mixed speech levels are confusing
3. ⚠️ **Sample check** - Pick 5 random scripts from each language, read aloud
4. ❌ **Ignore the rest** - "Good enough" for launch

## Want me to create specific fixes?

I can create targeted fixes for:
- [ ] Russian informal tone conversion
- [ ] Korean formality standardization  
- [ ] Top 20 CTA scripts tone improvement

Just say which ones!
