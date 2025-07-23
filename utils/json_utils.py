# utils/json_utils.py
import re
import json

def extract_json_block(text: str) -> dict:
    """
    Extrahiert am Ende eines Texts einen JSON-Block, z.B.:
    ... "json"
    
    Wird genutzt, um Agree/Disagree-Antworten der Agents zu parsen.
    """
    try:
        return json.loads(text[text.rfind('{'):])
    except Exception:
        return {}

# Beispiel-Fallbacks für strukturierte Antworten:
def partial_extract(text: str) -> dict:
    data = {}
    m = re.search(r'"agree":\s*(true|false)', text)
    if m:
        data['agree'] = m.group(1) == 'true'
    m2 = re.findall(r'"open_issues"\s*:\s*\[(.*?)\]', text)
    if m2:
        issues = [i.strip().strip('"') for i in m2[0].split(',')]
        data['open_issues'] = issues
    return data
