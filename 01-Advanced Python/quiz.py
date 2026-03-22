"""
PYTHON İLERİ SEVİYE ÖZELLİKLER SINAVI
======================================

Bu sınav Python decorator'ları ve ileri seviye özellikler hakkındaki bilginizi test eder.
Her soruyu seçtiğiniz şıkkın harfini (a, b, c veya d) yazarak cevaplayın.

Başarılar! 🎓
"""

import sys


class Quiz:
    """Python bilgisini test etmek için basit bir sınav uygulaması."""
    
    def __init__(self):
        """Soruları oluştur ve puanı takip et."""
        self.puan = 0
        self.toplam_soru = 0
        self.sorular = self.sorulari_olustur()
    
    def sorulari_olustur(self):
        """
        Sınav sorularını oluştur.
        
        Returns:
            list: Soru sözlüklerinin listesi
        """
        return [
            {
                "soru": "Python'da decorator'ın ana amacı nedir?",
                "secenekler": {
                    "a": "Fonksiyonları silmek",
                    "b": "Fonksiyonların kodunu değiştirmeden davranışlarını değiştirmek veya genişletmek",
                    "c": "Yeni sınıflar oluşturmak",
                    "d": "Modülleri içe aktarmak"
                },
                "dogru": "b",
                "aciklama": "Decorator'lar, orijinal fonksiyon kodunu değiştirmeden işlevsellik eklemek için fonksiyonları sarar."
            },
            {
                "soru": "Hangi decorator bir metodu parantez olmadan çağırmanıza izin verir (person.name() yerine person.name)?",
                "secenekler": {
                    "a": "@staticmethod",
                    "b": "@classmethod",
                    "c": "@property",
                    "d": "@abstractmethod"
                },
                "dogru": "c",
                "aciklama": "@property, bir metodu parantez olmadan çağırmanıza izin vererek bir nitelik gibi erişilebilir hale getirir."
            },
            {
                "soru": "@classmethod'un ilk parametresi nedir?",
                "secenekler": {
                    "a": "self",
                    "b": "cls",
                    "c": "class",
                    "d": "instance"
                },
                "dogru": "b",
                "aciklama": "@classmethod, ilk parametre olarak 'self' (örnek) değil, 'cls' (sınıfın kendisi) alır."
            },
            {
                "soru": "@staticmethod ne zaman kullanılmalıdır?",
                "secenekler": {
                    "a": "Örnek değişkenlerine erişmeniz gerektiğinde",
                    "b": "Sınıf değişkenlerini değiştirmeniz gerektiğinde",
                    "c": "Örnek veya sınıf verilerine erişmeyen bir yardımcı fonksiyona ihtiyaç duyduğunuzda",
                    "d": "Soyut metotlar oluşturmak istediğinizde"
                },
                "dogru": "c",
                "aciklama": "@staticmethod, self veya cls'ye erişime ihtiyaç duymayan yardımcı fonksiyonlar içindir."
            },
            {
                "soru": "@abstractmethod metotları olan bir sınıfı örneklendirmeye çalışırsanız ne olur?",
                "secenekler": {
                    "a": "Sorunsuz çalışır",
                    "b": "Python bir TypeError hatası verir",
                    "c": "Soyut metotlar otomatik olarak uygulanır",
                    "d": "Sınıf final hale gelir"
                },
                "dogru": "b",
                "aciklama": "Uygulanmamış soyut metotları olan bir sınıfı örneklendiremezsiniz - Python TypeError hatası verir."
            },
            {
                "soru": "@property ile @setter kullanmanın amacı nedir?",
                "secenekler": {
                    "a": "Değişkenleri sabit yapmak",
                    "b": "Nitelik değerlerini ayarlarken doğrulama mantığı eklemek",
                    "c": "Nitelikleri silmek",
                    "d": "Statik metotlar oluşturmak"
                },
                "dogru": "b",
                "aciklama": "@setter, özelliklere değer atarken doğrulama ve mantık eklemenize olanak tanır."
            },
            {
                "soru": "Üst üste yığılmış decorator'lar hangi sırayla uygulanır?\n\n@decorator1\n@decorator2\ndef func():\n    pass",
                "secenekler": {
                    "a": "Önce decorator1, sonra decorator2",
                    "b": "Önce decorator2, sonra decorator1",
                    "c": "Aynı anda uygulanırlar",
                    "d": "Sadece en üstteki decorator uygulanır"
                },
                "dogru": "b",
                "aciklama": "Decorator'lar aşağıdan yukarıya uygulanır: fonksiyona en yakın decorator önce uygulanır."
            },
            {
                "soru": "@final decorator'ı neyi belirtir?",
                "secenekler": {
                    "a": "Metodun veya sınıfın override edilmemesi/alt sınıflandırılmaması gerektiğini",
                    "b": "Metodun sınıftaki son metot olduğunu",
                    "c": "Sınıfın tamamlandığını ve kullanıma hazır olduğunu",
                    "d": "Metodun en son çağrılacağını"
                },
                "dogru": "a",
                "aciklama": "@final, bir metodun override edilmemesi veya bir sınıfın alt sınıflandırılmaması gerektiğini belirtir."
            },
            {
                "soru": "@classmethod için yaygın bir kullanım durumu nedir?",
                "secenekler": {
                    "a": "Yardımcı fonksiyonlar oluşturmak",
                    "b": "Alternatif yapıcılar (factory metotları) oluşturmak",
                    "c": "Metotları özel yapmak",
                    "d": "Kalıtımı önlemek"
                },
                "dogru": "b",
                "aciklama": "@classmethod, Date.from_string() gibi alternatif yapıcılar için yaygın olarak kullanılır."
            },
            {
                "soru": "@override decorator'ı neye yardımcı olur?",
                "secenekler": {
                    "a": "Metotların daha hızlı çalışmasını sağlar",
                    "b": "Metotların çağrılmasını engeller",
                    "c": "Bir üst sınıf metodunu override ettiğinizi düşündüğünüzde ama etmediğinizde hataları yakalamanıza yardımcı olur",
                    "d": "Soyut metotları otomatik olarak uygular"
                },
                "dogru": "c",
                "aciklama": "@override, bir üst sınıf metodunu override ettiğinizi açıkça belirtir ve tip denetleyicilerin hataları yakalamasına yardımcı olur."
            }
        ]
    
    def soruyu_goster(self, soru_no, soru_verisi):
        """
        Tek bir soruyu seçenekleriyle birlikte göster.
        
        Args:
            soru_no (int): Soru numarası
            soru_verisi (dict): Soru detaylarını içeren sözlük
        """
        print(f"\n{'='*70}")
        print(f"Soru {soru_no}/{len(self.sorular)}")
        print(f"{'='*70}")
        print(f"\n{soru_verisi['soru']}\n")
        
        for secenek, metin in sorted(soru_verisi['secenekler'].items()):
            print(f"  {secenek}) {metin}")
        print()
    
    def cevap_al(self):
        """
        Kullanıcının cevabını al.
        
        Returns:
            str: Kullanıcının cevabı (a, b, c veya d)
        """
        while True:
            cevap = input("Cevabınız (a/b/c/d): ").strip().lower()
            if cevap in ['a', 'b', 'c', 'd']:
                return cevap
            print("❌ Geçersiz giriş. Lütfen a, b, c veya d girin.")
    
    def cevabi_kontrol_et(self, kullanici_cevabi, soru_verisi):
        """
        Kullanıcının cevabının doğru olup olmadığını kontrol et.
        
        Args:
            kullanici_cevabi (str): Kullanıcının cevabı
            soru_verisi (dict): Soru detaylarını içeren sözlük
            
        Returns:
            bool: Doğruysa True, yanlışsa False
        """
        dogru = soru_verisi['dogru']
        dogru_mu = kullanici_cevabi == dogru
        
        if dogru_mu:
            print("\n✅ Doğru! Aferin!")
            self.puan += 1
        else:
            print(f"\n❌ Yanlış. Doğru cevap: {dogru}")
        
        print(f"💡 Açıklama: {soru_verisi['aciklama']}")
        return dogru_mu
    
    def sonuclari_goster(self):
        """Sınav sonuçlarını göster."""
        yuzde = (self.puan / self.toplam_soru) * 100
        
        print("\n" + "="*70)
        print("SINAV TAMAMLANDI!")
        print("="*70)
        print(f"\nPuanınız: {self.puan}/{self.toplam_soru} (%{yuzde:.1f})")
        
        # Puana göre geri bildirim ver
        if yuzde == 100:
            print("\n🌟 Mükemmel puan! Python decorator ustasısınız! 🌟")
        elif yuzde >= 80:
            print("\n🎉 Harika iş! Güçlü bir anlayışa sahipsiniz!")
        elif yuzde >= 60:
            print("\n👍 İyi iş! Kaçırdığınız konuları gözden geçirin.")
        elif yuzde >= 40:
            print("\n📚 Öğrenmeye devam edin! Eğitimi tekrar gözden geçirin.")
        else:
            print("\n💪 Pes etmeyin! Eğitimi çalışın ve tekrar deneyin.")
        
        print("\n" + "="*70)
    
    def calistir(self):
        """Sınavı çalıştır."""
        print("\n" + "="*70)
        print("PYTHON İLERİ SEVİYE ÖZELLİKLER SINAVI")
        print("="*70)
        print("\nBu sınav, eğitimde ele alınan Python decorator'ları ve")
        print("ileri seviye özellikler hakkındaki anlayışınızı test edecek.")
        print(f"\nToplam Soru: {len(self.sorular)}")
        print("\nHadi başlayalım!\n")
        
        input("Başlamak için Enter'a basın... ")
        
        self.toplam_soru = len(self.sorular)
        
        for i, soru_verisi in enumerate(self.sorular, 1):
            self.soruyu_goster(i, soru_verisi)
            kullanici_cevabi = self.cevap_al()
            self.cevabi_kontrol_et(kullanici_cevabi, soru_verisi)
            
            if i < self.toplam_soru:
                input("\nBir sonraki soruya geçmek için Enter'a basın... ")
        
        self.sonuclari_goster()


def main():
    """Sınavı çalıştırmak için ana fonksiyon."""
    quiz = Quiz()
    
    try:
        quiz.calistir()
    except KeyboardInterrupt:
        print("\n\n⚠️  Sınav kesildi. Hoşça kalın!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {e}")
        sys.exit(1)
    
    # Tekrar denemek isteyip istemediklerini sor
    print("\nSınavı tekrar çözmek ister misiniz?")
    tekrar = input("Tekrar denemek için 'evet' yazın, çıkmak için başka bir şey: ").strip().lower()
    
    if tekrar == 'evet':
        print("\n" * 2)
        main()
    else:
        print("\n👋 Sınavı çözdüğünüz için teşekkürler! Python öğrenmeye devam edin! 🐍")


if __name__ == "__main__":
    main()
