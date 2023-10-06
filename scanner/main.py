from time import strftime, localtime
from sys import argv

SAVE_RECOGNIZED_IMAGES = False       # Сохранять изображения, попадающие в программу?
IMAGES_DIRECTORY = ''         # Если да, то в какую папку? Папка должна существовать


def get_image_from_clipboard():
    """Возвращает объект Image из модуля PIL, если в буфере обмена находится изображение.
    Сохраняет изображение в директорию IMAGES_DIRECTORY, если SAVE_RECOGNIZED_IMAGES"""
    from PIL import ImageGrab
    img = ImageGrab.grabclipboard()
    if img is not None:
        if SAVE_RECOGNIZED_IMAGES:
            img_name = f'{strftime("%d.%m %H-%M-%S", localtime())}.png'
            img.save((f'{IMAGES_DIRECTORY}'
                      f'{"/" if IMAGES_DIRECTORY[-1:] != "/" else ""}'
                      f'{img_name}')
                     if IMAGES_DIRECTORY else img_name, 'PNG')
            print(f'Изображение успешно сохранено под именем "{img_name}" в папку {IMAGES_DIRECTORY}')
        return img
    else:
        print('В буфере обмена нет изображений...')


def recognize_text(img, language):
    """Использует модуль pytesseract как интерфейс для Google Tesseract и распознаёт текст на переданном изображении"""
    from pytesseract import image_to_string
    return image_to_string(img, lang=language, config='--psm 6')


def main():
    selected_lang = argv[-1]
    while True:
        if selected_lang in ('eng', 'rus'):
            image = get_image_from_clipboard()
            if image is not None:
                print(recognize_text(image, selected_lang))
            break
        else:
            selected_lang = input('Выберите язык из доступных (eng, rus) (по умолчанию eng): ') or 'eng'


if __name__ == '__main__':
    main()
