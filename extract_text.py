from pypdf import PdfReader
import pytesseract
from PIL import Image
import io
import sys

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_and_recognize_text(pdf_path, output_file, lang='eng'):
    """
    Извлекает изображения из PDF и распознает текст с указанным языком.

    Параметры:
    pdf_path (str): путь к PDF файлу
    output_file (str): путь к выходному текстовому файлу
    lang (str): язык распознавания. Примеры:
        'eng' - английский
        'rus' - русский
        'rus+eng' - русский и английский
        'deu' - немецкий
        'fra' - французский
    """
    reader = PdfReader(pdf_path)
    print(f"Прочитан {pdf_path}")
    print(f"Язык распознавания: {lang}")

    with open(output_file, 'w', encoding='utf-8') as text_file:
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]

            print(f"Страница {page_num + 1}: ", end='')

            for count, image_file_object in enumerate(page.images):
                try:
                    image = Image.open(io.BytesIO(image_file_object.data))

                    confidence = check_confidence(image, lang)
                    # Распознавание с дополнительными параметрами
                    text = pytesseract.image_to_string(
                        # image=processed_image, 
                        image=image, 
                        lang=lang,
                        config=custom_config_rus
                    )
#                    text_file.write(f"Изображение {count + 1}:\n")
                    text_file.write(text)
#                    text_file.write("\n" + "-"*50 + "\n")
                    print(f"распознано {len(text)} знаков, точность распознавания {int(confidence)}%")

                except Exception as e:
                    text_file.write(f"Ошибка при обработке изображения {count + 1}: {str(e)}\n")
    print(f"Распознанный текст записан в {output_file}")


def check_confidence(image, lang='rus'):
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    confidences = [int(conf) for conf in data['conf'] if conf != '-1']
    return sum(confidences) / len(confidences) if confidences else 0

# Для русского языка
pdf_file = sys.argv[1]
output_file = pdf_file[:len(pdf_file)-3] + "txt"
custom_config_rus = r'--oem 3 --psm 6 -c preserve_interword_spaces=0'
extract_and_recognize_text(pdf_file, output_file, lang='rus+eng')
