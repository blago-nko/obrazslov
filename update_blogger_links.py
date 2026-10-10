#!/usr/bin/env python3
import os
import re
import sys
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# --- КОНФИГУРАЦИЯ ---
BLOGGER_BASE_URL = "https://obraz-slov.blogspot.com" 
CONTENT_DIR = "content/posts/"                      

def get_fresh_image_url(blogger_slug):
    url = f"{BLOGGER_BASE_URL}/{blogger_slug}.html"
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code != 200:
            print(f"⚠️ Пост {blogger_slug} не найден (Code {resp.status_code})")
            return None
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        # Ищем первую картинку внутри контента поста
        img_tag = soup.find('img') 
        
        if not img_tag or not img_tag.get('src'):
            print(f"ℹ️ В посте {blogger_slug} нет картинок.")
            return None
            
        src = img_tag['src']
        
        # Фильтруем служебные иконки Blogger
        if 'blogger.googleusercontent.com' in src or 'blogspot.com' in src:
             return src
        else:
             imgs = soup.find_all('img')
             for i in imgs:
                 s = i.get('src', '')
                 if 'blogger.googleusercontent.com' in s:
                     return s
                     
        return None

    except Exception as e:
        print(f"❌ Ошибка при запросе {url}: {e}")
        return None

def update_markdown_files():
    updated_count = 0
    
    for filename in os.listdir(CONTENT_DIR):
        if not filename.endswith('.md'):
            continue
            
        filepath = os.path.join(CONTENT_DIR, filename)
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        blogger_slug = filename[:-3] 
        
        print(f"\n🔄 Обработка: {filename} (Slug: {blogger_slug})")
        
        fresh_url = get_fresh_image_url(blogger_slug)
        
        if not fresh_url:
            print("   -> Пропускаю (нет свежей ссылки)")
            continue
            
        pattern = r'(image:\s*)([^\n]+)'
        
        def replacer(match):
            prefix = match.group(1)
            old_val = match.group(2)
            
            if old_val.strip() == fresh_url:
                return match.group(0)
                
            print(f"   ✅ ЗАМЕНА:\n      OLD: {old_val}\n      NEW: {fresh_url}")
            return f'{prefix}{fresh_url}'
            
        new_content = re.sub(pattern, replacer, content, count=1)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_count += 1
            
    print(f"\n✨ Готово. Обновлено файлов: {updated_count}")

if __name__ == "__main__":
    try:
        import requests
        from bs4 import BeautifulSoup
    except ImportError:
        print("Установите зависимости: pip install requests beautifulsoup4")
        sys.exit(1)
        
    update_markdown_files()
