from PIL import Image
import pyautogui
import keyboard
import time

paint_colors = []
color_positions = []


def get_image():
    with Image.open('furry.png') as img:
        img = img.convert('RGB')
        width, height = img.size
        pixels = list(img.getdata())
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return pixels


def find_pallette():

    print('Please hover over each color on the color pallette and tap p, press f when done')
    i = 0
    while True:
        if keyboard.is_pressed('f'): 
            break
        if keyboard.is_pressed('p'):
            x, y = pyautogui.position()
            color_positions.append([x, y])
            R, G, B = pyautogui.pixel(x, y)
            paint_colors.append((R, G, B))
            print(f'Color: {R, G, B} saved at {x, y}')
            time.sleep(1)
    


def change_colors(pixels):
    for i in range(len(pixels[0])):
        for j in range(len(pixels[1])):
            pixel_color = tuple(pixels[i][j])

            # Find the closest MS Paint color to this pixel's color using Euclidean distance - then change to
            closest_color = min(paint_colors, key=lambda x: sum((a - b)**2 for a, b in zip(x, pixel_color)))
        
            pixels[i][j] = closest_color




def draw(pixels):
    #get mouse pos
    start_x, start_y = pyautogui.position()
    pyautogui.PAUSE = 0.001
    current_color = None
    
    # go through and draw each pixel, havent added color yet
    for i in range(len(pixels)):
        for j in range(len(pixels[i])):
            if keyboard.is_pressed('q'):
                print('Stopped drawing')
                break
            pixel_color = pixels[i][j]
            closest_color = min(paint_colors, key=lambda x: sum((a - b)**2 for a, b in zip(x, pixel_color)))
            color_position = color_positions[paint_colors.index(closest_color)]
            if closest_color == (255, 255, 255):
                continue
            if closest_color != current_color:
                pyautogui.moveTo(color_position)
                pyautogui.click()
                pyautogui.moveTo(start_x + j, start_y + i)
                pyautogui.click()
                current_color = closest_color
            else:
                pyautogui.moveTo(start_x + j, start_y + i)
                pyautogui.click()
            


def main():
    #not working atm
    find_pallette()
    print('Place mouse where top left of image should be and then press P to begin')
    while True:
        if keyboard.is_pressed('p'):  
            print('You Pressed A Key!')
            #turns image into pixels
            pixels = get_image()
            #changes colors to paint friendly ones
            change_colors(pixels)
            # draws dem pixels
            draw(pixels)
            print('Drawing finished!')
            break  

if __name__ == '__main__':
    main()