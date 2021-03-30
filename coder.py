from PIL import Image
import random as rnd


def encode(file_name, key, text):
    image = Image.open(file_name)
    image_data = list(image.getdata())
    image_length = len(image_data)

    image_bin_data = []
    for tp in image_data:
        r, g, b = tp[0], tp[1], tp[2]
        rgb_bin = []
        for color in [r, g, b]:
            color_bin = bin(color)[2:]
            if len(color_bin) < 8:
                color_bin = '0' * (8 - len(color_bin)) + color_bin
            rgb_bin.append(color_bin)
        image_bin_data.append((rgb_bin[0], rgb_bin[1], rgb_bin[2]))

    def char_to_bin(c):
        c_n = ord(c)
        if c_n > 1039:  # для русских букв
            c_n -= 848
        return bin(c_n)

    text_bin_data = list(map(char_to_bin, text))
    text_bin_data.append('0b00000000')  # конец текста

    rnd.seed(key)

    for letter_bin in text_bin_data:
        letter_bin = letter_bin[2:]
        if len(letter_bin) < 8:
            letter_bin = '0' * (8 - len(letter_bin)) + letter_bin

        rand_pos = rnd.randrange(image_length)

        [r, g, b] = image_bin_data[rand_pos]
        r = r[:-3] + letter_bin[0:3]
        g = g[:-2] + letter_bin[3:5]
        b = b[:-3] + letter_bin[5:8]
        image_bin_data[rand_pos] = [r, g, b]

    encoded_image_data = []
    for (r, g, b) in image_bin_data:
        encoded_image_data.append((int(r, 2), int(g, 2), int(b, 2)))

    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(encoded_image_data)
    encoded_image.save(file_name[0:-4] + '_encoded' + file_name[-4:])


def decode(file_name, key):
    encoded_image = Image.open(file_name)
    encoded_image_data = list(encoded_image.getdata())
    encoded_image_length = len(encoded_image_data)

    encoded_image_bin_data = []
    for tp in encoded_image_data:
        r, g, b = tp[0], tp[1], tp[2]
        rgb_bin = []
        for color in [r, g, b]:
            color_bin = bin(color)[2:]
            if len(color_bin) < 8:
                color_bin = '0' * (8 - len(color_bin)) + color_bin
            rgb_bin.append(color_bin)
        encoded_image_bin_data.append((rgb_bin[0], rgb_bin[1], rgb_bin[2]))

    def bin_to_char(n_b):
        c_n = int(n_b, 2)
        if c_n > 191:  # для русских букв
            c_n += 848
        return chr(c_n)

    rnd.seed(key)

    decoded_text_bin_data = []
    while True:
        rand_pos = rnd.randrange(encoded_image_length)
        [r, g, b] = encoded_image_bin_data[rand_pos]
        decoded_letter_bin = '0b' + r[-3:] + g[-2:] + b[-3:]
        if decoded_letter_bin == '0b00000000':
            break
        decoded_text_bin_data.append(decoded_letter_bin)

    decoded_text = ''.join(map(bin_to_char, decoded_text_bin_data))

    file_out = open(file_name[0:-12] + '_decoded.txt', 'wt', encoding='utf-8')
    file_out.write(decoded_text)
    file_out.close()

    return decoded_text
