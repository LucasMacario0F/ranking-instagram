import instaloader
import json
import time
from datetime import datetime
import csv

# Configuração Anti-Ban
L = instaloader.Instaloader(
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    sleep=True,
    request_timeout=300
)

# Lista de Perfis (ADICIONE SEUS 150 @S AQUI)
COMPETIDORES = ["integraamericana", "integrapiracicaba","omelhordointeriordesp","laucomfome","guia.piracicaba","dicasinteriordesp","rioclaro.dicas","dicasdesampasp","splovers","itu_dicas"]  # Substitua pelos seus

# Tempo de Delay Calculado Automaticamente
DELAY = 24 * 3600 / 150  # Divide 24h pelos 150 perfis → ~576s (9.6min) por perfil

def log(mensagem):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {mensagem}")

def carregar_valores():
    try:
        with open('values.csv', mode='r') as f:
            return {row['username']: float(row['valor']) for row in csv.DictReader(f)}
    except:
        return {}

def coletar_dados():
    rankings = []
    valores = carregar_valores()
    
    for username in COMPETIDORES:
        try:
            start_time = time.time()
            log(f"Coletando @{username}...")
            
            profile = instaloader.Profile.from_username(L.context, username)
            profile_pic = profile.get_profile_pic_url().replace("s150x150", "s320x320")
            
            rankings.append({
                "username": username,
                "followers": profile.followers,
                "profile_pic": profile_pic,
                "valor_reels": valores.get(username, 0)
            })
            
            elapsed = time.time() - start_time
            time.sleep(max(0, DELAY - elapsed))  # Respeita o rate limit
            
        except Exception as e:
            log(f"ERRO em @{username}: {str(e)}")
            continue
    
    # Salva os dados
    with open('data/rankings.json', 'w', encoding='utf-8') as f:
        json.dump(rankings, f, indent=2)

if __name__ == "__main__":
    coletar_dados()