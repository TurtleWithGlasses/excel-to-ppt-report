import pandas as pd

def load_and_process_data(file_path, sheet_name):
    try:
        # Excel verisini yükle
        data = pd.read_excel(file_path, sheet_name=sheet_name)

        # Gerekli sütunları kontrol et
        required_columns = ["Firma", "Erişim", "StxCm", "Reklam Eşdeğeri", "Editör"]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            raise KeyError(f"Missing columns in Excel data: {missing_columns}")

        # Editör sütunundaki verileri normalize et
        data["Editör"] = data["Editör"].str.strip().str.upper()

        # Olumlu ve Olumsuz sayısını hesapla
        olumlu_negatif = data.groupby(["Firma", "Editör"]).size().unstack(fill_value=0)

        # Summary oluştur
        summary = olumlu_negatif.reset_index()
        summary = summary.rename(columns={"OLUMLU": "Pozitif", "OLUMSUZ": "Negatif"})
        summary["Toplam"] = summary["Pozitif"] + summary["Negatif"]

        # Diğer metrikleri ekle
        metrics = data.groupby("Firma").agg({
            "Erişim": "sum",
            "StxCm": "sum",
            "Reklam Eşdeğeri": "sum"
        }).reset_index()

        # Merge işlemi
        summary = summary.merge(metrics, on="Firma", how="left")
        summary.rename(columns={"Firma": "Kurum", "StxCm": "STXCM"}, inplace=True)

        # Sadece gerekli sütunları bırak
        summary = summary[["Kurum", "Toplam", "Pozitif", "Negatif", "Erişim", "STXCM", "Reklam Eşdeğeri"]]

        # Toplam sütununa göre sıralama (Büyükten küçüğe)
        summary = summary.sort_values(by="Toplam", ascending=False)

        # Sıralanmış tabloyu kontrol için yazdır
        print("Sıralanmış tablo:")
        print(summary.head())  # İlk 5 satırı kontrol edin

        # Sayısal sütunları formatla
        summary["Erişim"] = summary["Erişim"].apply(lambda x: f"{x:,.0f}")
        summary["Reklam Eşdeğeri"] = summary["Reklam Eşdeğeri"].apply(lambda x: f"{x:,.0f}")
        summary["STXCM"] = summary["STXCM"].apply(lambda x: f"{x:,.2f}")

        return summary

    except KeyError as e:
        print(f"Missing column in Excel data: {e}")
        return None
    except Exception as e:
        print(f"Error processing Excel data: {e}")
        return None

