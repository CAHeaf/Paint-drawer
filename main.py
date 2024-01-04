from PIL import Image
import pyautogui
import keyboard
import time

paint_colors = [
        (0, 0, 0), (127, 127, 127), (136, 0, 21), (237, 28, 36), (255, 127, 39),
        (255, 242, 0), (34, 177, 76), (0, 162, 232), (63, 72, 204), (163, 73, 164),
        (255, 255, 255), (195, 195, 195), (185, 122, 87), (255, 174, 201), (255, 201, 14),
        (239, 228, 176), (181, 230, 29), (153, 217, 234), (112, 146, 190), (200, 191, 231)
        ]
color_positions = [[760, 60], [780, 60], [800, 60], [825, 60], [850, 60], [875, 60],
                   [900, 60], [916, 60], [937, 60], [960, 60], [760, 83], [780, 83], 
                   [800, 83], [825, 83], [850, 83], [875, 83], [900, 83],
                   [916, 83], [937, 83], [960, 83]]


def get_image():
    with Image.open('plant.png') as img:
        img = img.convert('RGB')
        width, height = img.size
        pixels = list(img.getdata())
        pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return pixels


def find_pallette():

    print('Please hover over the middle of white on the color pallette and tap p')
    while True:
        if keyboard.is_pressed('p'):
            white_x, white_y = pyautogui.position()
            break
    time.sleep(1)     
    print('Please hover over the middle of black on the color pallette and tap p')
    while True:
        if keyboard.is_pressed('p'):
            black_x, black_y = pyautogui.position()
            break
    time.sleep(1)             
    distance = abs(black_y - white_y)     

          
    create_pallette(black_x, black_y, white_y, white_x, distance)
    
def create_pallette(black_x, black_y, white_y, white_x, distance):
    for i in range(len(color_positions)):
        print(distance)
        if i <= 9:
           color_positions[i][0] = black_x + distance * i + (distance * 0.1)
           color_positions[i][1] = black_y
        elif i > 9:
           color_positions[i][0] = white_x + distance * i + (distance * 0.1)
           color_positions[i][1] = white_y
        color_positions[10][0] = white_x
        color_positions[10][1] = white_y
        print(color_positions[i])



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
    pyautogui.PAUSE = 0.01
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
    #find_pallette()
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