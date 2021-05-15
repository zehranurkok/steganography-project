 # PIL modulunu goruntunun pikselini
# cikarmak ve uzerinde degisiklik yapmak icin kullanacagiz
from PIL import Image

import speech_recognition as sr

sr.__version__

r = sr.Recognizer()

audiodata = sr.AudioFile("data/voicerecord.wav")

with audiodata as source:
    audio = r.record(source)

result = r.recognize_google(audio, language="en-US")

 
# Kodlama verilerini 8 bitlik binary sayiya donusturuyoruz
# Herbir karakter icin ASCII degerleri alinacak
def genData(data):
 
        # Verilen verinin binary kod halinde 
        # liste icerisine atilmasi
        newd = []
 
        for i in data:
            newd.append(format(ord(i), '08b'))
        return newd
 
# Pikseller 8 bitlik binary sayilara donustutulur
# ve tekrar dondurulur.
def modPix(pix, data):
 
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
 
    for i in range(lendata):
 
        # Tek seferde 3 piksel cikarma islemi
        pix = [value for value in imdata.__next__()[:3] +
                                imdata.__next__()[:3] +
                                imdata.__next__()[:3]]
 
        # Piksel degerlerini tek icin 1 
        # Cift icin 0 olacak sekilde degistiriyoruz
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
 
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1
 
        # Her 3lu setin 9. pikseli okumayi
        # daha fazla surdurup surdurmeyecegimizi 
        # belirlemek icindir.
        # 0 okumaya devam et anlamina gelirken,
        # 1 mesajin bittigini gosterir.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
 
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1
 
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]
 
def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
 
    for pixel in modPix(newimg.getdata(), data):
 
        # Duzenlenen yeni piksellerin, 
        # yeni bir resim icerisine yerlestirilmesi
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
 
# Verilerin resim icerisine kodlanmasi (steganografi)
def encode():
    img = input("Resim ismini giriniz (uzantısı ile birlikte) : ")
    image = Image.open(img, 'r')
 
    print("Sistemde bulunan ses kaydından alınan veri gizleniyor...")
    data = result
    if (len(data) == 0):
        raise ValueError('Boş veri girildi')
 
    newimg = image.copy()
    encode_enc(newimg, data)
 
    new_img_name = input("Yeni resimin ismini giriniz (uzantısı ile birlikte) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
 
# Resim icerisinde gizli olan verilerin 
# cozumlenmesi (steganaliz)
def decode():
    img = input("Resim ismini giriniz (uzantısı ile birlikte) : ")
    image = Image.open(img, 'r')
 
    data = ''
    imgdata = iter(image.getdata())
 
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                imgdata.__next__()[:3] +
                                imgdata.__next__()[:3]]
 
        # ikili veri dizisi
        binstr = ''
 
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'
 
        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data
 
# Main Fonksiyonu
def main():
    a = int(input("-- Steganografi İşlemi --\n"
                        "1. Encode\n2. Decode\n"))
    if (a == 1):
        encode()
 
    elif (a == 2):
        print("Kodlanan metin :  " + decode())
    else:
        raise Exception("Doğru giriş yapınız")
 
# Surucu Kodu
if __name__ == '__main__' :
 
    # Main fonksiyonun cagirilmasi
    main()
