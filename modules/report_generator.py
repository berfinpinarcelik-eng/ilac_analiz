from fpdf import FPDF
import io
from datetime import datetime

def turkish_to_ascii(text: str) -> str:
    """Türkçe karakterleri ASCII karşılıklarına çevir (fpdf latin-1 fallback için)."""
    table = str.maketrans("İıŞşĞğÇçÖöÜü", "IiSsGgCcOoUu")
    return text.translate(table)

def generate_pdf_report(drug_name: str, analysis_text: str) -> bytes:
    """
    Analiz sonucunu PDF olarak oluştur ve bytes döndür.
    """
    pdf = FPDF()
    pdf.add_page()

    # Türkçe karakter desteği için font (Proje klasöründen yükle)
    import os
    font_path = os.path.join(os.getcwd(), "assets", "fonts")
    
    regular_font = os.path.join(font_path, "DejaVuSans.ttf")
    bold_font = os.path.join(font_path, "DejaVuSans-Bold.ttf")
    
    # Font varlığına göre font ailesini seç
    use_dejavu = os.path.exists(regular_font) and os.path.exists(bold_font)
    
    if use_dejavu:
        pdf.add_font("DejaVu", "", regular_font, uni=True)
        pdf.add_font("DejaVu", "B", bold_font, uni=True)
        font_family = "DejaVu"
    else:
        # Font yoksa Unicode karakterleri desteklenmeyen fontlar yerine ASCII'ye çevirip Arial kullan
        font_family = "Arial"
        drug_name = turkish_to_ascii(drug_name)
        analysis_text = turkish_to_ascii(analysis_text)
    
    # Başlık ve Metinleri Hazırla
    title_text = "İlaç Analiz Raporu"
    warning_header = "⚠️ BU RAPOR BİLGİLENDİRME AMAÇLIDIR. TIBBİ TAVSİYE DEĞİLDİR. İLAÇ KULLANMADAN ÖNCE DOKTORUNUZA DANIŞINIZ."
    
    if not use_dejavu:
        title_text = turkish_to_ascii(title_text)
        warning_header = turkish_to_ascii(warning_header).replace("⚠️", "!")
        drug_name = turkish_to_ascii(drug_name)
        analysis_text = turkish_to_ascii(analysis_text)
    
    # Başlık
    pdf.set_font(font_family, "B", 16)
    pdf.cell(0, 12, f"{title_text}: {drug_name}", ln=True, align="C")
    pdf.set_font(font_family, "", 10)
    pdf.cell(0, 8, f"Oluşturulma: {datetime.now().strftime('%d.%m.%Y %H:%M')}", ln=True, align="C")
    pdf.ln(5)

    # Uyarı kutusu
    pdf.set_fill_color(255, 243, 205)
    pdf.set_font(font_family, "B", 10)
    pdf.multi_cell(0, 8, warning_header, fill=True)
    pdf.ln(5)

    # Analiz içeriği
    pdf.set_font(font_family, "", 11)
    # Markdown başlıklarını temizle
    clean_text = analysis_text.replace("##", "").replace("**", "").replace("*", "")
    pdf.multi_cell(0, 7, clean_text)

    # PDF'i bytes olarak döndür
    pdf_output = pdf.output(dest="S")
    if isinstance(pdf_output, str):
        return pdf_output.encode("latin-1")
    return bytes(pdf_output)
