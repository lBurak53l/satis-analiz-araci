import csv
from collections import defaultdict
from pathlib import Path


def satis_verilerini_yukle(dosya_yolu: str) -> list[dict]:
    kayitlar = []
    yol = Path(dosya_yolu)

    if not yol.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {dosya_yolu}")

    with yol.open(mode="r", encoding="utf-8", newline="") as f:
        okuyucu = csv.DictReader(f)
        for satir in okuyucu:
            adet = int(satir["adet"])
            birim_fiyat = float(satir["birim_fiyat"])
            kayitlar.append(
                {
                    "tarih": satir["tarih"].strip(),
                    "urun": satir["urun"].strip(),
                    "bolge": satir["bolge"].strip(),
                    "adet": adet,
                    "birim_fiyat": birim_fiyat,
                    "toplam_tutar": adet * birim_fiyat,
                }
            )

    return kayitlar


def satis_ozeti_hesapla(kayitlar: list[dict]) -> dict:
    toplam_ciro = sum(k["toplam_tutar"] for k in kayitlar)
    toplam_islem = len(kayitlar)
    ortalama_sepet = toplam_ciro / toplam_islem if toplam_islem > 0 else 0.0

    urun_ciro = defaultdict(float)
    bolge_ciro = defaultdict(float)

    for k in kayitlar:
        urun_ciro[k["urun"]] += k["toplam_tutar"]
        bolge_ciro[k["bolge"]] += k["toplam_tutar"]

    return {
        "toplam_ciro": round(toplam_ciro, 2),
        "toplam_islem": toplam_islem,
        "ortalama_sepet": round(ortalama_sepet, 2),
        "urun_bazli_ciro": dict(sorted(urun_ciro.items(), key=lambda x: x[1], reverse=True)),
        "bolge_bazli_ciro": dict(sorted(bolge_ciro.items(), key=lambda x: x[1], reverse=True)),
    }


def raporu_yazdir(ozet: dict) -> None:
    print("=== SATIŞ PERFORMANS ÖZETİ ===")
    print(f"Toplam İşlem Sayısı : {ozet['toplam_islem']}")
    print(f"Toplam Ciro          : {ozet['toplam_ciro']:,.2f} TL")
    print(f"Ortalama Sepet Tutarı: {ozet['ortalama_sepet']:,.2f} TL")

    print("\n--- Ürün Bazlı Ciro ---")
    for urun, tutar in ozet["urun_bazli_ciro"].items():
        print(f"  * {urun}: {tutar:,.2f} TL")

    print("\n--- Bölge Bazlı Ciro ---")
    for bolge, tutar in ozet["bolge_bazli_ciro"].items():
        print(f"  * {bolge}: {tutar:,.2f} TL")


def main() -> None:
    veri_dosyasi = Path(__file__).resolve().parent.parent / "data" / "satislar.csv"
    kayitlar = satis_verilerini_yukle(str(veri_dosyasi))
    ozet = satis_ozeti_hesapla(kayitlar)
    raporu_yazdir(ozet)


if __name__ == "__main__":
    main()