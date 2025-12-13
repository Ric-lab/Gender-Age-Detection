import os
import urllib.request
import time

def download_sample_data():
    data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        
    print(f"Baixando imagens de exemplo para: {data_dir}")
    print("Isso pode levar alguns instantes...")
    
    # Lista de URLs públicas (Unsplash/Pexels) simulando o dataset UTKFace
    # Nomes formatados como: [idade]_[genero]_[raca]_[data].jpg
    # Genero: 0=Masculino, 1=Feminino
    # NOTA: As idades são estimadas para fins de teste.
    
    samples = [
        # Homens
        {"url": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=400", "name": "30_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=400", "name": "25_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1504257432389-52343af06ae3?w=400", "name": "35_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=400", "name": "28_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1492562080023-ab3db95bfbce?w=400", "name": "40_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1506634572416-48cdfe530110?w=400", "name": "20_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=400", "name": "18_0_1_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1534308143481-c55f00be8bd7?w=400", "name": "22_0_1_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1583864697784-a0efc8379f7d?w=400", "name": "15_0_0_2017.jpg"}, # Menor
        {"url": "https://images.unsplash.com/photo-1548372290-8d01b6c8e78c?w=400", "name": "45_0_0_2017.jpg"},
        
        # Mulheres
        {"url": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?w=400", "name": "22_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=400", "name": "28_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400", "name": "24_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400", "name": "26_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=400", "name": "19_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1524504388940-b1c1722653e1?w=400", "name": "16_1_3_2017.jpg"}, # Menor
        {"url": "https://images.unsplash.com/photo-1549351512-c5e12b11e283?w=400", "name": "14_1_1_2017.jpg"}, # Menor
        {"url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?w=400", "name": "20_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=400", "name": "23_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1589156280159-27698a70f29e?w=400", "name": "21_1_1_2017.jpg"},
        
        # Mais idosos e variados
        {"url": "https://images.unsplash.com/photo-1463453091185-61582044d556?w=400", "name": "55_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1511485977113-f34c92461ad9?w=400", "name": "60_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1551843021-d7563d3f08b8?w=400", "name": "50_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=400", "name": "32_1_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1562159482-592762283a00?w=400", "name": "27_0_2_2017.jpg"},
        
         # Crianças / Jovens
        {"url": "https://images.unsplash.com/photo-1519238263496-6361937a2d50?w=400", "name": "10_0_0_2017.jpg"},
        {"url": "https://images.unsplash.com/photo-1503919545885-7f494927f99a?w=400", "name": "8_1_0_2017.jpg"}
    ]
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    for i, sample in enumerate(samples):
        try:
            path = os.path.join(data_dir, sample["name"])
            req = urllib.request.Request(sample["url"], headers=headers)
            with urllib.request.urlopen(req) as response:
                with open(path, 'wb') as out_file:
                    out_file.write(response.read())
            print(f"[{i+1}/{len(samples)}] Baixado: {sample['name']}")
            time.sleep(0.5) # Evitar rate limit
        except Exception as e:
            print(f"Erro ao baixar {sample['url']}: {e}")

    print("\nDownload concluído! Agora há imagens suficientes para um teste mais 'real'.")
    print("Execute 'python src/train.py' para treinar com estes dados.")

if __name__ == "__main__":
    download_sample_data()
