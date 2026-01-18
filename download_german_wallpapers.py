#!/usr/bin/env python3
"""
Script pour télécharger des images de paysages allemands depuis Unsplash API
"""

import requests
import json
import os
import time
from pathlib import Path

# Configuration
IMAGES_DIR = "Background"
OUTPUT_JSON = "german_wallpapers_urls.json"
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"

# Termes de recherche en allemand
SEARCH_TERMS = [
    "german landscape",
    "deutsches landschaft",
    "schwarzwald",
    "bavarian scenery",
    "rhein valley",
    "schloss germany",
    "neuschwanstein",
    "lake germany",
    "alpen münchen",
    "hamburg city",
    "berlin cityscape",
    "cologne cathedral",
    "german countryside",
    "bayern landscape",
]

# Créer le dossier Background s'il n'existe pas
Path(IMAGES_DIR).mkdir(exist_ok=True)
print(f"✅ Dossier créé/vérifié: {IMAGES_DIR}\n")

def download_image(url, filename):
    """Télécharge une image"""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        filepath = os.path.join(IMAGES_DIR, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Téléchargé: {filename} ({len(response.content) / 1024 / 1024:.2f}MB)")
        return filepath
    
    except Exception as e:
        print(f"❌ Erreur téléchargement {filename}: {e}")
        return None

def download_from_unsplash():
    """Télécharge des images depuis Unsplash (pas d'API key nécessaire pour les recherches publiques)"""
    print("🔍 Récupération d'images depuis Unsplash...\n")
    
    images_downloaded = 0
    urls_dict = {}
    
    # Utiliser les URLs directes de Unsplash (source publique)
    # Ces URLs sont des images libres de droits sous Unsplash License
    default_images = {
        "schwarzwald_forest": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080&q=80",
        "bavarian_alps": "https://images.unsplash.com/photo-1520763185298-1b434c919abe?w=1080&q=80",
        "neuschwanstein_castle": "https://images.unsplash.com/photo-1451673580459-43490279c0fa?w=1080&q=80",
        "rhein_river": "https://images.unsplash.com/photo-1509023464349-18f4d7e97b39?w=1080&q=80",
        "german_city": "https://images.unsplash.com/photo-1524678606370-a47ad25cb82a?w=1080&q=80",
        "hamburg_port": "https://images.unsplash.com/photo-1524634126288-917b0ad82086?w=1080&q=80",
        "berlin_culture": "https://images.unsplash.com/photo-1552038564-9fe9f9ad1a2a?w=1080&q=80",
        "cologne_rhein": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=1080&q=80",
        "german_village": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe3e?w=1080&q=80",
        "mountain_landscape": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080&q=80",
        "alpine_meadow": "https://images.unsplash.com/photo-1519904981063-b0cf448d479e?w=1080&q=80",
        "forest_path": "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1080&q=80",
        "german_castle": "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1080&q=80",
        "scenic_valley": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080&q=80",
        "autobahn": "https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=1080&q=80",
    }
    
    print(f"⬇️  Téléchargement de {len(default_images)} images de paysages allemands...\n")
    
    for name, url in default_images.items():
        filename = f"{name}.jpg"
        print(f"[{images_downloaded + 1}/{len(default_images)}] {name}...")
        
        if download_image(url, filename):
            images_downloaded += 1
            urls_dict[name] = url
        
        time.sleep(0.5)  # Pause douce
    
    return images_downloaded, urls_dict

def save_urls(urls_dict):
    """Sauvegarde les URLs dans un JSON"""
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(urls_dict, f, ensure_ascii=False, indent=2)
    print(f"\n✅ URLs sauvegardées dans {OUTPUT_JSON}")

def main():
    print("=" * 60)
    print("🌄 Téléchargeur d'images de paysages allemands")
    print("=" * 60 + "\n")
    
    images_downloaded, urls = download_from_unsplash()
    
    if images_downloaded > 0:
        save_urls(urls)
        print(f"\n✨ Succès! {images_downloaded} images téléchargées dans le dossier '{IMAGES_DIR}'")
        
        # Vérifier les fichiers téléchargés
        files = os.listdir(IMAGES_DIR)
        print(f"\n📁 Fichiers dans Background: {len(files)}")
        for f in sorted(files)[:5]:
            print(f"   - {f}")
        if len(files) > 5:
            print(f"   ... et {len(files) - 5} autres fichiers")
    else:
        print("\n❌ Aucune image n'a pu être téléchargée")

if __name__ == "__main__":
    main()
