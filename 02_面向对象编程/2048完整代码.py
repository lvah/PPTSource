"""
文件名: .py
创建时间: 2019-01-05 09:
作者: lvah
联系方式: 976131979@qq.com
代码描述:


"""

import curses
import random
from itertools import chain


class GameField(object):
    def __init__(self, width=4, height=4, win_score=2048):
        self.width = width
        self.height = height
        self.score = 0  # 当前得分
        self.highscore = 0  # 最高分
        self.win_score = win_score
        # 存储判断各个方向是否可移动的函数?
        self.moves = {}
        self.moves['Left'] = self.is_move_left
        self.moves['Right'] = self.is_move_right
        self.moves['Up'] = self.is_move_up
        self.moves['Down'] = self.is_move_down
        #  # 存储执行各个方向移动的函数?
        self.movesDict = {}
        self.movesDict['Left'] = self.move_left
        self.movesDict['Right'] = self.move_right
        self.movesDict['Up'] = self.move_up
        self.movesDict['Down'] = self.move_down

    # 重置棋盘， 重新开始游戏时， 执行的操作;
    def reset(self):
        # 2). 是否要更新最高分, 当前分数为0；
        if self.score > self.highscore:
            self.highscore = self.score
        self.score = 0

        # 3). 创建棋盘的数据， 默认情况下时4*4， 数值全为0；
        self.field = [[0 for j in range(self.height)] for i in range(self.width)]

        self.random_create()
        self.random_create()

    # 开始游戏时， 棋盘数据会随机生成2或者4，
    def random_create(self):
        # field[0][2] = 2
        while True:
            firstIndex = random.choice(range(self.height))
            secondIndex = random.choice(range(self.width))
            if self.field[firstIndex][secondIndex] == 0:
                value = random.choice([2, 4, 2, 2, 2])
                self.field[firstIndex][secondIndex] = value
                break

    # 画棋盘
    def draw(self, stdstr):
        def draw_sep():
            # print("+-----" * 4 + '+')
            stdstr.addstr("+-----" * self.width + '+' + '\n')

        # 2. 画每一行的格子
        def draw_one_row(row):  # [0, 2, 0, 0]   |    |  2  |    |    |
            stdstr.addstr("".join(['|  %d  ' % (item) if item != 0 else '|     ' for item in row]) + '|\n')

        stdstr.clear()
        stdstr.addstr(''.center(42, "*")+'\n')
        stdstr.addstr('2048游戏'.center(40, '*')+'\n')
        stdstr.addstr(''.center(42, '*')+'\n')
        # 3. 绘制棋盘
        for row in self.field:
            draw_sep()
            draw_one_row(row)
        draw_sep()
        stdstr.addstr("\n当前分数: %s" % (self.score))
        stdstr.addstr("\n当前最高分数: %s" % (self.highscore))
        stdstr.addstr(" \n游戏帮助: 上下左右键  (R)estart E(xit) ")
        if self.is_win():
            stdstr.addstr("\n游戏胜利\n")
        if self.is_gameover():
            stdstr.addstr("游戏失败\n")

    def is_win(self):
        # return max(chain(*self.field)) >= 2048
        return max(chain(*self.field)) >= self.win_score

    def is_gameover(self):
        return not any([self.is_move_left(self.field),
                        self.is_move_right(self.field),
                        self.is_move_up(self.field),
                        self.is_move_down(self.field)])


    def is_row_left(self, row):  # [0, 2,2,0]
        # 任意两个元素可以向左移动？
        def is_change(index):  # index时索引值， [0,1,2,3]
            # - 如果第一个数值为0， 第二个数值不为0， 则说明可以向左移动；
            if row[index] == 0 and row[index + 1] != 0:
                return True
            # - 如果第一个数值不为0， 第二个数值与第一个元素相等， 则说明可以向左移动；
            if row[index] != 0 and row[index + 1] == row[index]:
                return True
            return False

        # 只要这一行的任意两个元素可以向左移动， 则返回True;
        return any([is_change(index) for index in range(self.width-1)])



    def invert(self, field):
        """矩阵的反转"""
        return [row[::-1] for row in field]


    def transpose(self, field):
        """实现矩阵的转置"""
        # zip: 实现
        # *field对列表进行解包;
        return [ list(row) for row in zip(*field)]



    def is_move_left(self, field):
        # 只要棋盘的任意一行可以向左移动， 就返回True；
        return any([self.is_row_left(row) for row in field])
    def is_move_right(self, field):
        # 对棋盘的每一行元素进行反转;
        invertField = self.invert(field)
        return  self.is_move_left(invertField)

    def is_move_up(self, field):
        # 对棋盘的每一行元素进行转置;
        transposeField = self.transpose(field)
        return  self.is_move_left( transposeField)

    def is_move_down(self, field):
        # 判断能否向下移动, 也就是对于元素进行转置, 判断转置后的棋盘能否向右移动;
        # 对棋盘的每一行元素进行反转;
        transposeField = self.transpose(field)
        return self.is_move_right(transposeField)

    # 1). 先把这一行的非0 数字向前放， 0向后放；   ==== [2, 2, 2, 2]
    def tight(self, row):  # [2,0,2,0]
        return sorted(row, key=lambda x: 1 if x == 0 else 0)

    # 2). 依次循环判断两个数是否相等， 如果相等， 第一个*2， 第二个数为0；  【4， 0， 4， 0】
    def merge(self, row):
        for index in range(self.width-1):
            if row[index] == row[index + 1]:
                row[index] *= 2
                row[index + 1] = 0
                # 如果合并完成， 分数增加row[index]
                self.score += row[index]
        return row

    def move_row_left(self, row):
        return self.tight(self.merge(self.tight(row)))

    def move_left(self, field):
         return [self.move_row_left(row) for row in field]

    def move_right(self, field):
        field = self.invert(field)
        return self.invert(self.move_left(field))

    def move_up(self, field):
        field = self.transpose(field)
        return self.transpose(self.move_left(field))

    def move_down(self, field):
        field = self.transpose(field)
        return self.transpose(self.move_right(field))


    def move(self, direction):
        # 1). 判断这个方向是否可以移动?
        # 2). 执行移动的操作
        # 3). 再随机生成一个2或者4

        # 确保是上下左右的按键
        if direction in self.moves:
            # 1).判断这个方向是否可以移动?
            if self.moves[direction](self.field):
                self.field = self.movesDict[direction](self.field)
                self.random_create()
        else:
            return False


def get_user_action(stdstr):
    # 获取用户键盘输入的内容
    action = stdstr.getch()
    if action == curses.KEY_UP:
        return 'Up'
    if action == curses.KEY_DOWN:
        return 'Down'
    if action == curses.KEY_LEFT:
        # stdstr.addstr("left")
        return 'Left'
    if action == curses.KEY_RIGHT:
        # stdstr.addstr("right")
        return 'Right'
    # 获取字母r的ASCII码
    if action == ord('r'):
        # stdstr.addstr("重新开始")
        return 'Restart'
    if action == ord('e'):
        # stdstr.addstr("退  出")
        return 'Exit'


def main(stdstr):
    game_field = GameField(width=6, height=6, win_score=8)

    def init():
        game_field.reset()
        game_field.draw(stdstr)
        return 'Game'

    def game():
        # 重新绘制棋盘
        game_field.draw(stdstr)
        action = get_user_action(stdstr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'
        if game_field.move(action):
            # move函数
            if game_field.is_win():
                return 'Win'
            if game_field.is_gameover():
                return 'Gameover'
        return 'Game'

    def not_game():
        action = get_user_action(stdstr)
        if action == 'Restart':
            return 'Init'
        if action == 'Exit':
            return 'Exit'

    state = 'Init'

    state_dict = {
        'Init': init,
        'Game': game,
        'Win':not_game,
        'Gameover':not_game,
        'Exit': exit
    }

    while True:
        state = state_dict[state]()


        # if state == 'Init':
        #     # 通过初始化函数， 进入游戏状态;
        #     state = init()
        # if state == 'Game':
        #     # 执行game函数， 判断用户的操作；
        #     # 1). 继续游戏; (upo, down, left, right)
        #     # 2). 重新开始；(R)
        #     # 3). 退出;(Q)
        #
        #     state = game()
        #
        # if state == 'Win':
        #     # 没有进行游戏， 只有两种状态;
        #     # 1). 重新开始；(R)
        #     # 2). 退出;(Q)
        #     state = not_game()
        # if state == 'Gameover':
        #     state = not_game()
        # if state == 'Exit':
        #     exit()

curses.wrapper(main)
