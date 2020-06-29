#!/user/bin/python
#-*-coding:utf-8-*-
import pygame, sys
import os     #文件操作的库，用于判断图片是否正确
import time  #时间库
import pymysql
from pygame.locals import * #引入一些常量名
pathleft = r'images\看图识词20题'  #题图的路径
pathright = r'images\识词辨图'
path1 = r'images\arrow'        #箭头的路径
path3 = r'images\元素'         #正确，错误图案的路径
pygame.init()
font1 = pygame.font.Font("C:/Windows/Fonts/simhei.ttf",30)  #提示语字体
font2 = pygame.font.Font("C://Windows//Fonts//STHUPO.TTF",36)#计分字体
BLACK = (0,0,0)
wordcolor = (0,255,255)                          #蓝青色
tipscolor = (0,110,250)                          #左下角提示语颜色

class ShowImage(pygame.sprite.Sprite):             #加载图片的类
    def __init__(self,screen):
        pygame.sprite.Sprite.__init__(self)
        self.target_surface = screen
        self.image = None
        self.rect = None
    def load(self,filename,left,top,width=None):
        self.image = pygame.image.load(filename).convert_alpha()
        rect = self.image.get_rect()              # 获取图片信息
        if(width!=None):
            imageheight = int(rect.height * width / rect.width)  # 转化不允许浮点数，需要转化为int型
            self.image = pygame.transform.smoothscale(self.image, (width, imageheight), )  # 转化大小为100左右
        else:
            width = rect.width
            imageheight = rect.height
        self.rect = left,top,width,imageheight

class GameInterface():
    def __init__(self):
        self.screen = pygame.display.set_mode((800,600),FULLSCREEN) #主屏幕
        pygame.display.set_caption("Happy Learning")  # 左上角名字
        self.number = 1
        self.fmenu = 0
        self.score = 0
        self.boolmenu = True
        self.boolquestion = False
        self.t = ShowImage(self.screen)
        self.t.load(path3 + '\\correct.png', 200, 100)  # 导入正确图案
        self.f = ShowImage(self.screen)
        self.f.load(path3+'\\wrong.png',200,100)          #错误图案
        self.framerate = pygame.time.Clock()              #建立一个时钟对象来帮助追踪时间
        self.menugroup = pygame.sprite.Group()
        self.questiongroup = pygame.sprite.Group()
        self.alertgroup = pygame.sprite.Group()         #提示对错的精灵组
        self.arrow()
        self.menu()
        self.main()

    def menu(self):
        rpath = path3  # 首页上各图片的路径
        self.p1 = ShowImage(self.screen)
        self.p1.load(rpath + '\个人信息.png', 330, 100)  # 参数为filename，left，top
        self.p2 = ShowImage(self.screen)
        self.p2.load(rpath + '\看图识词.png', 125, 250)
        self.p3 = ShowImage(self.screen)
        self.p3.load(rpath + '\识词辨图.png', 525, 250)
        self.p4 = ShowImage(self.screen)
        self.p4.load(rpath + '\听词辨图.png', 330, 400)  # 注：英文命名的文件开头要加反斜线（转义字符），中文不用
        self.p5 = ShowImage(self.screen)
        self.p5.load(rpath + '\\righttop.png', 600, 0)  # 首页右上图
        self.p6 = ShowImage(self.screen)
        self.p6.load(rpath + '\\leftdown.png', 0, 420)  # 首页左下图

    def print_text(self,font, x, y, text, color=(255, 255, 255), shadow=True):  # 显示文字函数，用于显示分数,shadow表示阴影,不给颜色默认为白色
        if shadow:
            imgText = font.render(text, True, (BLACK))
            self.screen.blit(imgText, (x - 2, y - 2))
        imgText = font.render(text, True, color)
        self.screen.blit(imgText, (x, y))

    def question(self,path):    #载入题目图片
        Path = path + '\\' + str(self.number)
        self.center = ShowImage(self.screen)
        self.center.load(os.path.join(Path,os.listdir(Path)[0]), 335, 245,110)#参数分别为路径，左坐标、上坐标、宽度
        self.up = ShowImage(self.screen)
        self.up.load(os.path.join(Path,os.listdir(Path)[1]), 330, 50,100)
        self.down = ShowImage(self.screen)
        self.down.load(os.path.join(Path,os.listdir(Path)[2]), 330, 450,100)
        self.left = ShowImage(self.screen)
        self.left.load(os.path.join(Path,os.listdir(Path)[3]), 140, 250,100)
        self.right = ShowImage(self.screen)
        self.right.load(os.path.join(Path,os.listdir(Path)[4]), 540, 250,100)

    def arrow(self):
        self.upa = ShowImage(self.screen)
        self.upa.load(os.path.join(path1,os.listdir(path1)[0],),350,150,60)
        self.downa = ShowImage(self.screen)
        self.downa.load(os.path.join(path1,os.listdir(path1)[1]),350,355,60)
        self.lefta = ShowImage(self.screen)
        self.lefta.load(os.path.join(path1,os.listdir(path1)[2]),250,260,80)
        self.righta = ShowImage(self.screen)
        self.righta.load(os.path.join(path1,os.listdir(path1)[3]),450,260,80)

    def questionupdate(self):
        self.questiongroup.empty()
        self.questiongroup.add(self.upa, self.downa, self.lefta, self.righta)
        self.question(self.P)
        self.questiongroup.add(self.up, self.down, self.left, self.right, self.center)

    def finish(self):
        timenow = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        co = pymysql.connect('121.36.64.222', user='root', passwd='123456', db='game')
        cursor = co.cursor()
        sql = """insert into gamelog
                (time,number,score)
                values(\"{time}\",{number},{score})""".format(time=timenow,number=self.number-1,score=self.score)

        print(sql)
        try:
            # 执行SQL语句
            cursor.execute(sql)
            co.commit()  #事务是访问和更新数据库的一个程序执行单元，必须有，否则指令不生效
            print("上传成功！")
        except:
            # 如果发生错误则执行回滚操作
            co.rollback()
        cursor.close()  # 先关闭游标
        co.close()  # 再关闭数据库连接
        self.questiongroup.empty()
        self.questiongroup.draw(self.screen)
        self.alertgroup.empty()
        self.alertgroup.draw(self.screen)
        self.print_text(font1,275,290,"已结束，即将返回首页",tipscolor)
        pygame.display.update()
        pygame.time.delay(2000)
        self.number = 0
        self.menugroup.add(self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)
        self.boolmenu = True
        self.boolquestion = False

    def main(self):
        goback = ShowImage(self.screen)
        goback.load(path3+"\返回.png",640,455,100)   #返回按钮
        self.menugroup.add(self.p1,self.p2,self.p3,self.p4,self.p5,self.p6)
        while True:
            self.framerate.tick(30)                           #更新时钟
            # ticks = pygame.time.get_ticks()  # 得到以毫秒为间隔的时间
            self.screen.fill((255, 255, 255))  # 背景填充为白色
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  #退出pygame模块
                    sys.exit()     #退出程序
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if(self.fmenu == 0):
                            self.fmenu = 1
                        elif(self.number <= 20):
                            P = self.P + "//" + str(self.number)
                            if(len(os.listdir(P)[1].split("#")) == 2):
                                self.score += 1
                                # self.questiongroup.empty()
                                self.alertgroup.empty()
                                self.alertgroup.add(self.t)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                            else:
                                self.alertgroup.empty()
                                self.alertgroup.add(self.f)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                    elif event.key == pygame.K_DOWN:
                        if(self.fmenu == 0):
                            self.fmenu = 2
                        elif(self.number <= 20):
                            P = self.P + "//" + str(self.number)
                            if(len(os.listdir(P)[2].split("#")) == 2):
                                self.score += 1
                                self.alertgroup.empty()
                                self.alertgroup.add(self.t)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                            else:
                                self.alertgroup.empty()
                                self.alertgroup.add(self.f)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                    elif event.key == pygame.K_LEFT:
                        if(self.fmenu == 0):
                            self.fmenu = 3
                            self.boolmenu = False
                            self.boolquestion = True
                            self.P = pathleft
                            self.questionupdate()
                        elif(self.number <= 20):
                            P = self.P + "//" + str(self.number)
                            if(len(os.listdir(P)[3].split("#")) == 2):
                                self.score += 1
                                self.alertgroup.empty()
                                self.alertgroup.add(self.t)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                            else:
                                self.alertgroup.empty()
                                self.alertgroup.add(self.f)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                    elif event.key == pygame.K_RIGHT:
                        if(self.fmenu == 0):
                            self.fmenu = 4
                            self.boolmenu = False
                            self.boolquestion = True
                            self.questionupdate()
                        elif(self.number <= 20):
                            P = self.P + "//" + str(self.number)
                            if(len(os.listdir(P)[4].split("#")) == 2):
                                self.score += 1
                                self.alertgroup.empty()
                                self.alertgroup.add(self.t)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                            else:
                                self.alertgroup.empty()
                                self.alertgroup.add(self.f)
                                self.alertgroup.draw(self.screen)
                                pygame.display.update()
                                pygame.time.delay(1000)
                                self.number += 1
                                if self.number <= 20:
                                    self.questionupdate()
                                else:
                                    self.finish()
                    elif event.key == pygame.K_ESCAPE:
                        self.screen = pygame.display.set_mode((800, 600),0,32)
                    elif event.key == pygame.K_F1:
                        self.screen = pygame.display.set_mode((800,600),FULLSCREEN)
                elif event.type == MOUSEBUTTONDOWN:  # 鼠标点击事件
                    presseed = pygame.mouse.get_pressed()
                    if presseed[0] == 1 and self.boolquestion:
                        pos = pygame.mouse.get_pos()
                        # print(pos)
                        if pos[0] >= 640 and pos[0] <= 737:  # 判断按钮位置
                            if pos[1] >= 455 and pos[1] <= 528:
                                self.questiongroup.empty()
                                self.menugroup.add(self.p1, self.p2, self.p3, self.p4, self.p5, self.p6)
                                self.fmenu = 0
                                self.score = 0
                                self.number = 1
                                self.boolmenu = True
                                self.boolquestion = False
            if self.boolmenu:
                # self.menugroup.update(ticks)   #update为自定义方法，这里未定义
                self.menugroup.draw(self.screen)
            elif self.boolquestion:
                self.questiongroup.add(goback)
                self.questiongroup.draw(self.screen)
                self.print_text(font2, 20, 20, "得分：" + str(self.score), wordcolor)
            pygame.display.update()

game = GameInterface()
