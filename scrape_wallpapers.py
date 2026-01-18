#!/usr/bin/env python3
"""
Script pour récupérer les images de paysages allemands depuis best-wallpaper.net
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from urllib.parse import urljoin
import time

# URL à scraper
BASE_URL = "https://fr.best-wallpaper.net/Search/q=paysage_allemagne"

# Dossier de destination
IMAGES_DIR = "Background"
os.makedirs(IMAGES_DIR, exist_ok=True)

def get_wallpapers(url):
    """Récupère les URLs des wallpapers depuis le site"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        wallpapers = []
        
        # Chercher tous les éléments image dans les résultats de recherche
        # Adapter les sélecteurs CSS selon la structure du site
        for img_container in soup.find_all('div', class_='thumb-item'):
            try:
                # Chercher le lien vers la page de l'image
                link = img_container.find('a')
                if link and link.get('href'):
                    wallpapers.append(link['href'])
            except Exception as e:
                print(f"Erreur lors du parsing d'une image: {e}")
                continue
        
        return wallpapers
    
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la requête: {e}")
        return []

def get_image_url_1080p(wallpaper_page_url):
    """Récupère l'URL 1080p d'une page de wallpaper"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(wallpaper_page_url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Chercher le lien de téléchargement 1080p
        # Adapter selon la structure du site
        download_links = soup.find_all('a', href=True)
        
        for link in download_links:
            href = link.get('href', '')
            # Chercher les URLs contenant "1080"
            if '1080' in href or '1920' in href:
                return href
        
        return None
    
    except Exception as e:
        print(f"Erreur lors de la récupération de {wallpaper_page_url}: {e}")
        return None

def download_image(url, filename):
    """Télécharge une image"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        
        filepath = os.path.join(IMAGES_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Téléchargé: {filename}")
        return filepath
    
    except Exception as e:
        print(f"❌ Erreur téléchargement {filename}: {e}")
        return None

def save_urls_to_json(urls_dict):
    """Sauvegarde les URLs dans un fichier JSON"""
    output_file = "german_wallpapers_1080.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(urls_dict, f, ensure_ascii=False, indent=2)
    print(f"\n✅ URLs sauvegardées dans {output_file}")

def main():
    print("🔍 Récupération des images de paysages allemands...")
    print(f"Source: {BASE_URL}\n")
    
    # Étape 1: Récupérer les pages des wallpapers
    wallpaper_pages = get_wallpapers(BASE_URL)
    print(f"Trouvé {len(wallpaper_pages)} wallpapers\n")
    
    if not wallpaper_pages:
        print("Aucun wallpaper trouvé. Le site a peut-être changé de structure.")
        return
    
    # Étape 2: Pour chaque page, récupérer l'URL 1080p
    urls_dict = {}
    count = 0
    
    for idx, page_url in enumerate(wallpaper_pages[:20]):  # Limiter à 20 pour commencer
        print(f"[{idx+1}/{len(wallpaper_pages[:20])}] Traitement: {page_url}")
        
        # Assurer que l'URL est complète
        full_url = urljoin(BASE_URL, page_url) if not page_url.startswith('http') else page_url
        
        # Récupérer l'URL 1080p
        image_url = get_image_url_1080p(full_url)
        
        if image_url:
            count += 1
            key = f"paysage_allemagne_{count}"
            urls_dict[key] = image_url
            print(f"  ✅ URL trouvée: {image_url[:60]}...")
            
            # Télécharger l'image
            filename = f"wallpaper_{count:03d}.jpg"
            download_image(image_url, filename)
        else:
            print(f"  ⚠️ Pas d'URL 1080p trouvée")
        
        # Pause pour ne pas surcharger le serveur
        time.sleep(1)
    
    # Étape 3: Sauvegarder les URLs
    if urls_dict:
        save_urls_to_json(urls_dict)
        print(f"\n📊 Total: {count} images trouvées")
    else:
        print("\n❌ Aucune image 1080p n'a pu être récupérée")

if __name__ == "__main__":
    main()
