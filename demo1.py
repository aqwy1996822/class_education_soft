import pygame, sys
from pygame.locals import *
import cv2
import numpy as np
import csv
import time
today=str(time.strftime("%Y/%m/%d")).replace('/0','/')
print (today)

def null2zero(data_list):
    new_data_list=[]
    for i in range(len(data_list)):
        item=data_list[i]
        if i>1:
            for j in range(len(item)):
                if item[j]=='':
                    item[j] ='0'
        new_data_list.append(item)
        # print(item)
    return new_data_list
def getLastWeek():
    import calendar
    import datetime
    today = datetime.date.today()
    oneday = datetime.timedelta(days = 1)
    dates_list=[]
    m1=calendar.MONDAY
    m7 = calendar.SUNDAY
    today -= oneday
    while today.weekday() != m7:
        today -= oneday
    while today.weekday()!=m1:
        nextMonday = today.strftime('%Y/%m/%d').replace('/0','/')
        today -= oneday
        dates_list.append(nextMonday)
    nextMonday = today.strftime('%Y/%m/%d').replace('/0', '/')
    dates_list.append(nextMonday)
    return dates_list

def img_deal(input_img):
    img = cv2.imread(input_img, cv2.IMREAD_UNCHANGED)
    img = cv2.resize(img, (75, 75), interpolation=cv2.INTER_AREA)
    rows, cols, channel = img.shape

    # 创建一张4通道的新图片，包含透明通道，初始化是透明的
    img_new = np.zeros((rows, cols, 4), np.uint8)
    img_new[:, :, 0:3] = img[:, :, 0:3]

    # 创建一张单通道的图片，设置最大内接圆为不透明，注意圆心的坐标设置，cols是x坐标，rows是y坐标
    img_circle = np.zeros((rows, cols, 1), np.uint8)
    img_circle[:, :, :] = 0  # 设置为全透明
    img_circle = cv2.circle(img_circle, (int(cols / 2), int(rows / 2)), int(min(rows, cols) / 2), (255),-1)  # 设置最大内接圆为不透明

    # 图片融合
    img_new[:, :, 3] = img_circle[:, :, 0]

    # 保存图片
    cv2.imwrite(input_img + ".png", img_new)
    img = pygame.image.load(input_img + ".png")
    return img

def init():
    screen.fill((245, 245, 245))
    pygame.draw.rect(screen,(240,128,128),[0, 0, 1280, 90])
    # 绘制一个空心矩形
    #表格标题
    draw_rect(screen, BLACK, GRAY2, [19, 115, 972, 67], 1)
    draw_text_box(screen, [95, 145], '上节还课', BLACK, 30)
    draw_text_box(screen, [305, 145], '本节答题', BLACK, 30)
    draw_text_box(screen, [810, 145], '本节进步', BLACK, 30)
    draw_text_box(screen, [932, 145], '总积分', BLACK, 30)

    draw_rect(screen, BLACK, GRAY2, [1008, 115, 252, 67], 1)
    draw_text_box(screen, [1135, 145], '上周总榜', BLACK, 30)

    mouse_position_list, star_home_position_list = draw_student_list(screen, [20, 190, 970, 70])
    draw_text_box(screen,[400, 47],'Welcome to DANBA',WHITE,45)
    return mouse_position_list, star_home_position_list


def draw_rect(screen, color_out, color_in, position, size):
    # 绘制一个空心矩形
    pygame.draw.rect(screen, color_out, position, size)
    # 绘制一个矩形
    pygame.draw.rect(screen, color_in,[position[0] + size, position[1] + size, position[2] - size - 1, position[3] - size - 1])

def get_total():
    with open("./data/class.csv", 'r') as f:
        reader = csv.reader(f)
        data_list = []
        for item in reader:
            data_list.append(item[1:])
        data_list=null2zero(data_list)


        students_name_list=data_list[1]
        class_grade_list=[]
        for item in data_list[2:]:
            class_grade_list.append([int(i) for i in item])
    # print(class_grade_list)
    class_total=np.sum(class_grade_list, axis=0)

    with open("./data/home.csv", 'r') as f:
        reader = csv.reader(f)
        data_list = []
        for item in reader:
            data_list.append(item[1:])
        data_list = null2zero(data_list)

        home_grade_list=[]
        for item in data_list[2:]:
            home_grade_list.append([int(i) for i in item])
    # print(home_grade_list)
    home_total=np.sum(home_grade_list, axis=0)

    with open("./data/process.csv", 'r') as f:
        reader = csv.reader(f)
        data_list = []
        for item in reader:
            data_list.append(item[1:])
        data_list = null2zero(data_list)

        process_grade_list=[]
        for item in data_list[2:]:
            process_grade_list.append([int(i) for i in item])
    # print(process_grade_list)
    process_total=np.sum(process_grade_list, axis=0)

    total_grade_list=[process_total[i]*2+home_total[i]*1.5+class_total[i] for i in  range(len(class_total))]
    return total_grade_list



def draw_result_list(screen, position, num):
    pygame.draw.rect(screen, BLACK, [position[0] - 1, position[1] - 1, position[2] + 2, num * position[3] + 2], 1)

    result_list = ['还课冠军', ' ', '答题冠军', ' ', '进步冠军', ' ']
    LastWeek_list=getLastWeek()

    with open("./data/class.csv", 'r') as f:
        reader = csv.reader(f)
        data_list=[]
        for item in reader:
            data_list.append(item)
        data_list = null2zero(data_list)

    class_students_name = data_list[1][1:]
    students_num=len(class_students_name)
    date_list = [str(i[0]) for i in data_list]
    class_total=[0]*students_num
    for date in date_list:
        if date in LastWeek_list:
            # print(date)
            # print(data_list[date_list.index(date)])
            class_total=[class_total[i]+int(data_list[date_list.index(date)][1:][i]) for i in range(len(class_total))]
            # class_total+=data_list[date_list.index(date)][1:]
            # print(class_total)
    class_max_index=class_total.index(max(class_total))
    result_list[3]=class_students_name[class_max_index]

    print('home')
    with open("./data/home.csv", 'r') as f:
        reader = csv.reader(f)
        data_list=[]
        for item in reader:
            data_list.append(item)
        data_list = null2zero(data_list)

    home_students_name = data_list[1][1:]
    students_num=len(home_students_name)
    date_list = [str(i[0]) for i in data_list]
    home_total=[0]*students_num
    for date in date_list:
        if date in LastWeek_list:
            # print(date)
            # print(data_list[date_list.index(date)])
            home_total=[home_total[i]+int(data_list[date_list.index(date)][1:][i]) for i in range(len(home_total))]
            # class_total+=data_list[date_list.index(date)][1:]
            # print(home_total)
    home_max_index=home_total.index(max(home_total))
    result_list[1]=home_students_name[home_max_index]


    with open("./data/process.csv", 'r') as f:
        reader = csv.reader(f)
        data_list=[]
        for item in reader:
            data_list.append(item)
        data_list = null2zero(data_list)

    process_students_name = data_list[1][1:]
    students_num=len(process_students_name)
    date_list = [str(i[0]) for i in data_list]
    process_total=[0]*students_num
    for date in date_list:
        if date in LastWeek_list:
            process_total=[process_total[i]+int(data_list[date_list.index(date)][1:][i]) for i in range(len(process_total))]
            # class_total+=data_list[date_list.index(date)][1:]
            # print(process_total)
    process_max_index=process_total.index(max(process_total))
    result_list[5]=process_students_name[process_max_index]



    for i in range(num):
        if i %2== 0:
            list_color = WHITE
        else:
            list_color = GRAY3
        pygame.draw.rect(screen, list_color, [position[0], position[1] + i * position[3], position[2], position[3]])
        name = result_list[i]
        draw_text_box(screen, [position[0] + position[2]*0.5, position[1] + int((i + 0.5) * position[3])], name, BLACK, 25)


def draw_student_list(screen, position):
    num = len(students_name)
    pygame.draw.rect(screen, BLACK, [position[0] - 1, position[1] - 1, position[2] + 2, num * position[3] + 2], 1)
    mouse_position_list = []
    star_home_position_list = []
    total_grade_list=get_total()
    for i in range(num):
        if i % 2 == 0:
            list_color = WHITE
        else:
            list_color = GRAY3
        pygame.draw.rect(screen, list_color, [position[0], position[1] + i * position[3], position[2], position[3]])
        mouse_position = [position[0], position[1] + i * position[3], position[0] + position[2],
                          position[1] + i * position[3] + position[3]]
        mouse_position_list.append(mouse_position)
        # pygame.draw.circle(screen, GRAY2, [position[0] + 200, position[1] + int((i + 0.5) * position[3])], 35)
        name = students_name[sort_index[i]]
        last_class_grade=process_list_last[sort_index[i]]
        process_grade=process_list_process[sort_index[i]]
        process = process_list[sort_index[i]]
        # draw_text_box(screen, [position[0] + 350, position[1] + int((i + 0.5) * position[3])], process, BLACK, 35)
        draw_text_box(screen, [position[0] + 180, position[1] + int((i + 0.5) * position[3])], name, BLACK, 30)
        draw_text_box(screen, [position[0] + 50, position[1] + int((i + 0.5) * position[3])], last_class_grade, BLACK, 30)
        draw_text_box(screen, [position[0] + 800, position[1] + int((i + 0.5) * position[3])], process_grade, BLACK,30)


        #总分
        totoal_grade=int(total_grade_list[sort_index[i]])
        draw_text_box(screen, [position[0] + 910, position[1] + int((i + 0.5) * position[3])], totoal_grade, BLACK, 30)
        # img = img_deal('star.jpg')
        img = pygame.image.load("./resource/star.png")
        screen.blit(img, (position[0] +75, position[1] + int((i + 0.5) * position[3] - 30)))
        star_home_position_list.append([position[0] + 11, position[1] + int((i + 0.5) * position[3]) - 30])
    return mouse_position_list, star_home_position_list

def draw_text_box(screen,position,text,color,size):
    fontObj = pygame.font.Font('./resource/wryh.ttf', size)
    textSurfaceObj = fontObj.render(str(text), True, color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = (position[0],position[1])
    screen.blit(textSurfaceObj, textRectObj)

def draw_process_list(screen, position, num):
    mouse_position_list=[]
    for i in range(num):
        if i % 2 == 0:
            list_color = RED
        else:
            list_color = BLUE
        process = process_list[sort_index[i]]

        pading = 10
        pygame.draw.rect(screen, list_color,[position[0] + 220, position[1] + i * position[3] + pading, process*25, position[3] - 2 * pading])
        mouse_position = [position[0] + 220, position[1] + i * position[3] + pading, 490+position[0] + 220, position[3] - 2 * pading+position[1] + i * position[3] + pading]
        mouse_position_list.append(mouse_position)
        draw_text_box(screen, [position[0] + 350, position[1] + int((i + 0.5) * position[3])], process, BLACK, 35)
    return mouse_position_list

pygame.init()
FPS = 120
fpsClock = pygame.time.Clock()
screen = pygame.display.set_mode((1280,720), FULLSCREEN, 32)
# screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('DANBA')
starimg = pygame.image.load("./resource/star.png")
wuyaimg= pygame.image.load("./resource/wuya.png")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 99, 71)
DARKGREEN = (85, 107, 47)
GREEN = (127, 255, 170)
BLUE = (64, 224, 208)
GRAY1 = (230, 230, 230)
GRAY2 = (200, 200, 200)
GRAY3 = (220, 220, 220)

with open("./data/class.csv", 'r') as f:
    reader = csv.reader(f)
    data_list = []
    for item in reader:
        data_list.append(item)
    data_list = null2zero(data_list)

students_name = data_list[1][1:]
num = len(students_name)
sort_index=range(num)


star_move_target_come = []
star_move_position_come = []
wuya_move_target_come=[]
wuya_move_position_come=[]


while True:
    #读数据
    with open("./data/class.csv", 'r') as f:
        reader = csv.reader(f)
        data_list=[]
        for item in reader:
            data_list.append(item)
        data_list = null2zero(data_list)

    date_list = [str(i[0]) for i in data_list[2:]]
    if today in date_list:
        date_index = date_list.index(today)
        print('date_index', date_index)
    else:
        new_data = [str(today)]
        for i in range(num):
            new_data.append(0)
        data_list.append(new_data)
        # with open("./data/class.csv", 'w') as f:
        #     csv_write = csv.writer(f)
        #     csv_write.writerows(data_list)
        date_index = len(date_list)
        # print('date_index', date_index)

    process_list=list(map(int,data_list[date_index+2][1:]))




    with open("./data/home.csv", 'r') as f:
        reader = csv.reader(f)
        data_list_home=[]
        for item in reader:
            data_list_home.append(item)
        data_list_home = null2zero(data_list_home)

    date_list = [str(i[0]) for i in data_list_home[2:]]
    if today in date_list:
        date_index = date_list.index(today)
        print('date_index', date_index)
    else:
        new_data = [str(today)]
        for i in range(num):
            new_data.append(0)
        data_list_home.append(new_data)
        date_index = len(date_list)
        print('date_index', date_index)
    process_list_last = list(map(int, data_list_home[date_index+2][1:]))


    with open("./data/process.csv", 'r') as f:
        reader = csv.reader(f)
        data_list_process=[]
        for item in reader:
            data_list_process.append(item)
        data_list_process = null2zero(data_list_process)

    date_list = [str(i[0]) for i in data_list_process[2:]]
    if today in date_list:
        date_index = date_list.index(today)
        print('date_index', date_index)
    else:
        new_data = [str(today)]
        for i in range(num):
            new_data.append(0)
        data_list_process.append(new_data)
        date_index = len(date_list)
        print('date_index', date_index)

    process_list_process= list(map(int, data_list_process[date_index+2][1:]))

    #初始化
    mouse_position_list, star_home_position_list=init()
    draw_result_list(screen, [1010, 190, 250, 50], 6)
    mouse_position_list=draw_process_list(screen, [30, 190, 900, 70], 7)
    print('mouse_position_list',mouse_position_list)




    # 获取事件
    for event in pygame.event.get():
        # 判断事件是否为退出事件
        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
            # 退出pygame
            pygame.quit()
            # 退出系统
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index == 0:
                        pos = pygame.mouse.get_pos()
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        for i in range(len(mouse_position_list)):
                            mouse_position = mouse_position_list[i]
                            if mouse_x < mouse_position[2] and mouse_x > mouse_position[0] and mouse_y < mouse_position[3] and mouse_y > mouse_position[1] and process_list[sort_index[i]]<20:
                                process_list[sort_index[i]] = process_list[sort_index[i]] + 1
                                star_move_target_come.append(star_home_position_list[i])
                                star_move_position_come.append([1280, star_home_position_list[i][1]])

                                sound_win = pygame.mixer.Sound('./resource/win.ogg')
                                sound_win.play()
                                break
                        #上节还课分数
                        for i in range(len(mouse_position_list)):
                            mouse_position = mouse_position_list[i]
                            if mouse_x < 100 and mouse_x > 50 and mouse_y < mouse_position[3] and mouse_y > mouse_position[1]:
                                process_list_last[sort_index[i]] = process_list_last[sort_index[i]] + 1
                                break
                        #本节进步分数
                        for i in range(len(mouse_position_list)):
                            mouse_position = mouse_position_list[i]
                            if mouse_x < 850 and mouse_x > 750 and mouse_y < mouse_position[3] and mouse_y > mouse_position[1]:
                                process_list_process[sort_index[i]] = process_list_process[sort_index[i]] + 1
                                break
                    elif index == 2:
                        pos = pygame.mouse.get_pos()
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        for i in range(len(mouse_position_list)):
                            mouse_position = mouse_position_list[i]
                            if mouse_x < mouse_position[2] and mouse_x > mouse_position[0] and mouse_y < mouse_position[3] and mouse_y > mouse_position[1]and process_list[sort_index[i]]>0:
                                process_list[sort_index[i]] = process_list[sort_index[i]] - 1
                                wuya_move_target_come.append([1280, star_home_position_list[i][1]])
                                wuya_move_position_come.append(star_home_position_list[i])

                                sound_lose = pygame.mixer.Sound('./resource/wuya.ogg')
                                sound_lose.play()
                                break
                        # 上节还课分数
                        for i in range(len(mouse_position_list)):
                            mouse_position = mouse_position_list[i]
                            if mouse_x < 100 and mouse_x > 50 and mouse_y < mouse_position[3] and mouse_y > mouse_position[1] and process_list_last[sort_index[i]] >0:
                                process_list_last[sort_index[i]] = process_list_last[sort_index[i]] - 1
                                break
                        # 进步分数
                        for i in range(len(mouse_position_list)):
                            mouse_position = mouse_position_list[i]
                            if mouse_x < 850 and mouse_x > 750 and mouse_y < mouse_position[3] and mouse_y > \
                                    mouse_position[1] and process_list_process[sort_index[i]] > 0:
                                process_list_process[sort_index[i]] = process_list_process[sort_index[i]] - 1
                                break
    done_stars_num=0
    done_wuya_num=0

    for i in range(len(star_move_target_come)):
        if abs(star_move_position_come[i][0] - star_move_target_come[i][0]) < 25:
            done_stars_num+=1
    for i in range(len(wuya_move_target_come)):
        if abs(wuya_move_position_come[i][0] - wuya_move_target_come[i][0]) < 25:
            done_wuya_num+=1

    for i in range(len(star_move_target_come)):
        if star_move_position_come[i][0] > star_move_target_come[i][0] and abs(star_move_position_come[i][0] - star_move_target_come[i][0]) > 25:
            star_move_position_come[i][0] = star_move_position_come[i][0] - 20
            screen.blit(starimg, (star_move_position_come[i][0], star_move_position_come[i][1]))
    for i in range(len(wuya_move_target_come)):
        if wuya_move_position_come[i][0]<wuya_move_target_come[i][0] and abs(wuya_move_position_come[i][0]-wuya_move_target_come[i][0])>25:
            wuya_move_position_come[i][0]=wuya_move_position_come[i][0]+20
            screen.blit(wuyaimg, (wuya_move_position_come[i][0],wuya_move_position_come[i][1]))

    # 排序
    if done_stars_num==len(star_move_position_come) and done_wuya_num==len(wuya_move_position_come):
        process_list = np.array(process_list)
        sort_index = np.argsort(-process_list)
        process_list_sort = []
        students_name_sort = []
        for i in range(len(sort_index)):
            process_list_sort.append(process_list[sort_index[i]])
            students_name_sort.append(students_name[sort_index[i]])
        # process_list = process_list_sort
        # students_name = students_name_sort
    # 绘制屏幕内容
    pygame.display.update()
    fpsClock.tick(FPS)
    with open("./data/class.csv", 'w+', newline='', encoding="utf-8") as f:
        # f.write(x)
        data_list[-1][1:]=process_list
        csv_write = csv.writer(f)
        csv_write.writerows(data_list)

    with open("./data/home.csv", 'w+', newline='', encoding="utf-8") as f:
        # f.write(x)
        data_list_home[-1][1:]=process_list_last
        csv_write = csv.writer(f)
        csv_write.writerows(data_list_home)

    with open("./data/process.csv", 'w+', newline='', encoding="utf-8") as f:
        # f.write(x)
        data_list_process[-1][1:]=process_list_process
        csv_write = csv.writer(f)
        csv_write.writerows(data_list_process)
