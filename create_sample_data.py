"""
Create sample Excel data files for testing templates
"""

import pandas as pd
import os
from datetime import datetime, timedelta
import random

# Create data directory
os.makedirs('data/samples', exist_ok=True)


def create_bsh_sample_data():
    """Create sample BSH media monitoring data."""
    print("Creating BSH sample data...")

    firms = ['BSH', 'Arçelik', 'Vestel', 'Beko', 'Profilo']
    media_types = ['Basın', 'İnternet', 'Televizyon', 'Radyo']
    media_scopes = ['Ulusal', 'Yerel', 'Bölgesel']
    cities = ['İSTANBUL', 'ANKARA', 'İZMİR', 'BURSA', 'ANTALYA', 'ADANA']

    data = []

    for _ in range(100):
        row = {
            'Mecra': random.choice(media_types),
            'Firma': random.choice(firms),
            'Yayın Tarihi': datetime.now() - timedelta(days=random.randint(1, 30)),
            'Analiz Tarihi': datetime.now() - timedelta(days=random.randint(0, 5)),
            'Medya Kapsam': random.choice(media_scopes),
            'Medya Tür': random.choice(['Gazete', 'Dergi', 'Portal', 'Blog', 'TV', 'Radyo']),
            'Medya Adı': f'Medya {random.randint(1, 20)}',
            'Başlık': f'Haber Başlığı {random.randint(1, 100)}',
            'Sayfa No': random.randint(1, 50),
            'Beyaz Eşya Olay Açıklama': 'Örnek olay açıklaması',
            'Beyaz Eşya Ürün Kategorisi': random.choice(['KURUMSAL', 'ÜRÜN', 'HİZMET']),
            'Beyaz Eşya Ürün Gruplandırması': random.choice(['KURUMSAL', 'ÜRÜN', 'HİZMET']),
            'Editör': random.choice(['OLUMLU', 'OLUMSUZ', 'NÖTR']),
            'StxCm': round(random.uniform(1, 100), 2),
            'Sayfa/Adet': round(random.uniform(0.001, 1.0), 3),
            'Erişim': random.randint(1000, 100000),
            'Reklam Eşdeğeri': round(random.uniform(100, 10000), 2),
            'Medya Tiraj': random.randint(1000, 50000),
            'Medya Peryod': random.choice(['GÜNLÜK', 'HAFTALIK', 'AYLIK']),
            'Medya İçerik': random.choice(['SİYASİ', 'EKONOMİ', 'MAGAZIN', 'SPOR']),
            'Medya Şehir': random.choice(cities),
            'Bahis Ağırlığı': random.choice(['FİRMAYA ÖZEL', 'KISA BAHİS', 'GENİŞ BAHİS']),
            'Kupür Tipi': 'HABER',
            'Görsel Malzeme': random.choice(['DİĞER', 'FOTOĞRAF', 'İNFOGRAFİK']),
            'Boyut ': random.choice(['KÜÇÜK', 'ORTALAMA', 'BÜYÜK']),
            'Algı': random.choice(['YÜKSEK', 'ORTA', 'DÜŞÜK']),
            'Görünürlük': random.choice(['BAŞLIKTA', 'ALTTA', 'İÇERİKTE']),
            ' Medya Grup Adı': f'Medya Grup {random.randint(1, 10)}',
            'Net Etki': random.randint(100, 20000)
        }
        data.append(row)

    df = pd.DataFrame(data)
    output_path = 'data/samples/BSH_Sample_Data.xlsx'
    df.to_excel(output_path, index=False)
    print(f"[OK] Created: {output_path} ({len(df)} rows)")

    return df


def create_sanofi_sample_data():
    """Create sample Sanofi pharmaceutical data."""
    print("\nCreating Sanofi sample data...")

    firms = [
        'SANOFI', 'PFIZER', 'ASTRAZENECA', 'BAYER', 'NOVARTIS',
        'NOVO NORDISK', 'ABDİ İBRAHİM', 'AMGEN', 'ECZACIBAŞI İLAÇ',
        'İLKO', 'ROCHE', 'JOHNSON & JOHNSON'
    ]

    data = []

    for firm in firms:
        positive = random.randint(10, 50)
        negative = random.randint(5, 25)
        total = positive + negative

        row = {
            'FİRMALAR': firm,
            'OLUMLU': positive,
            'OLUMSUZ': negative,
            'TOTAL': total
        }
        data.append(row)

    df = pd.DataFrame(data)
    df = df.sort_values('TOTAL', ascending=False).reset_index(drop=True)

    output_path = 'data/samples/Sanofi_Sample_Data.xlsx'
    df.to_excel(output_path, index=False)
    print(f"[OK] Created: {output_path} ({len(df)} rows)")

    return df


def create_socar_sample_data():
    """Create sample SOCAR energy sector data."""
    print("\nCreating SOCAR sample data...")

    categories = [
        'Kurumsal Haberler', 'Ürün ve Hizmetler', 'Sosyal Sorumluluk',
        'Yatırımlar', 'İnsan Kaynakları', 'Çevre ve Enerji',
        'Finansal Sonuçlar', 'Ortaklıklar'
    ]

    regions = [
        'İstanbul', 'Ankara', 'İzmir', 'Bursa', 'Antalya',
        'Adana', 'Gaziantep', 'Konya', 'Kocaeli'
    ]

    media_types = ['Basın', 'İnternet', 'Televizyon', 'Radyo', 'Sosyal Medya']

    data = []

    # Category data
    for category in categories:
        row = {
            'Kategori': category,
            'Toplam Haber': random.randint(20, 100),
            'Erişim': random.randint(50000, 500000),
            'Net Etki': random.randint(5000, 50000),
            'Bölge': None,
            'Medya Türü': None,
            'Algı': None,
            'Haber Sayısı': None
        }
        data.append(row)

    # Regional data
    for region in regions:
        row = {
            'Kategori': None,
            'Toplam Haber': random.randint(10, 80),
            'Erişim': random.randint(20000, 300000),
            'Net Etki': None,
            'Bölge': region,
            'Medya Türü': None,
            'Algı': None,
            'Haber Sayısı': None
        }
        data.append(row)

    # Media type data
    for media_type in media_types:
        row = {
            'Kategori': None,
            'Toplam Haber': random.randint(30, 120),
            'Erişim': None,
            'Net Etki': None,
            'Bölge': None,
            'Medya Türü': media_type,
            'Algı': None,
            'Haber Sayısı': None
        }
        data.append(row)

    df = pd.DataFrame(data)

    output_path = 'data/samples/SOCAR_Sample_Data.xlsx'
    df.to_excel(output_path, index=False)
    print(f"[OK] Created: {output_path} ({len(df)} rows)")

    return df


if __name__ == '__main__':
    print("=" * 60)
    print("Creating Sample Data Files")
    print("=" * 60)

    create_bsh_sample_data()
    create_sanofi_sample_data()
    create_socar_sample_data()

    print("\n" + "=" * 60)
    print("[OK] All sample data files created!")
    print("=" * 60)
    print("\nFiles created in: data/samples/")
    print("  1. BSH_Sample_Data.xlsx")
    print("  2. Sanofi_Sample_Data.xlsx")
    print("  3. SOCAR_Sample_Data.xlsx")
    print("\nYou can now test the templates with these sample files.")
