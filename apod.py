import utility
import requests
from bs4 import BeautifulSoup
import pyimgur
from PIL import Image

CLIENT_ID = "TOKEN"
USERNAME_MV = "USER"
PASSWORD_MV = "PASS"


def main():
    browser = utility.login(USERNAME_MV, PASSWORD_MV)
    data = {}
    r = requests.get("http://observatorio.info/")
    soup = BeautifulSoup(r.content, "lxml")
    title = soup.find('h1', 'intro')
    description = soup.find('div', 'lead main icn-enlarge').find('p')
    image = soup.find('div', 'col-sm-12 aq-first aq-last text-center icn-enlarge').find('a')
    video = soup.find('div', 'col-sm-12 aq-first aq-last text-center icn-enlarge').find('iframe')
    if image is not None:
        r = requests.get(image['href'])
        with open("imagen.jpg", "wb") as code:
            code.write(r.content)
        imagen = Image.open("./imagen.jpg")
        imagen.save("./imagen_comprimida.jpg", quality=90)
        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image("./imagen_comprimida.jpg", title="Astronomic Picture of Day")
        data['image'] = uploaded_image.link
    if video is not None:
        data['video'] = video['src']
    data['title'] = title.text
    data['description'] = description.text

    title = data['title']
    explanation = data['description']
    message = '[b]{}[/b]\n\n{}\n\n'.format(title, explanation)
    if 'image' in data:
        message += '[img]{}[/img]\n\n{}'.format(data['image'], image['href'])
    else:
        if 'youtube' in data['video']:
            video = data['video'].lstrip('https://www.youtube.com/embed/')
            message += '[video]https://www.youtube.com/watch?v={}[/video]'.format(video)
        else:
            message = message + "\nDebido a capacidades del foro de mediavida, me es imposible insertar el siguiente enlace. Haz clic si deseas ver el contenido: " + \
                      data['video']
    utility.post(message, 555411, browser)  # post de ciencia
    # utility.post(message, 550851, browser) # El interno


if __name__ == '__main__':
    main()
