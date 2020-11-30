import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as md

# 数据预处理函数，将日期格式为'%Y/%m/%d'转化为'%Y-%m-%d'格式
def dmy2ymd(dmy):
    dmy = str(dmy, encoding='utf-8')
    date = dt.datetime.strptime(dmy, '%Y/%m/%d').date()
    ymd = date.strftime('%Y-%m-%d')
    return ymd

# 日期，开盘价格，最高价格，最低价格，收盘价格
# 其中 M8[D]代表datetime64类型：将表中元素转化为日期类型 f8表示float64
# converters表示对数据进行预处理，我们可以先定义一个函数， 这里的converters是一个字典, 表示第一列使用函数dmy2ymd函数来进行预处理
dates, opening_prices, highest_prices, lowest_prices, closing_prices \
    = np.loadtxt(
        'MSFT19972012_1.csv',
        delimiter=',', usecols=(0,1, 2, 3, 4), unpack=True,
        dtype='M8[D],f8,f8,f8,f8', converters={0: dmy2ymd})

for i in range(len(opening_prices) -2):
    # 创建图形对象 相当于创建一个画布
    plt.rcParams['figure.figsize'] = (2.8, 2.8)  # 设置figure_size尺寸
    plt.rcParams['figure.dpi'] = 200  # 分辨率
    plt.rcParams['savefig.dpi'] = 200  # 图片像素
    plt.figure()

    # 获得坐标轴
    ax = plt.gca()

    # 设置y轴左边刻度范围
    plt.ylim(0, 300)
    dates, opening_prices, highest_prices, lowest_prices, closing_prices \
        = np.loadtxt(
        'MSFT19972012.csv',
        delimiter=',', usecols=(0, 1, 2, 3, 4), unpack=True,
        dtype='M8[D],f8,f8,f8,f8', converters={0: dmy2ymd})
    # 坐标轴主刻度 以周一作为主刻度
    # ax.xaxis.set_major_locator(md.WeekdayLocator())

    if (dates[i] + 2 != dates[i + 2]):
        # xy轴边框不可见 x,y轴刻度不可见
        plt.axis('off')
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        continue
    for j in range(i, i+3):
        # 将日期标准化成numpy的日期

        # plt.axis('off')
        ax.xaxis.set_minor_locator(md.DayLocator())
        ax.xaxis.set_major_formatter(md.DateFormatter('%y/%m/%d'))

        dates = dates.astype(md.datetime.datetime)
        # 比较收盘价格和开盘价格，大于等于0.01则返回true，反之返回false
        rise = closing_prices[j] - opening_prices[j] >= 0.01

        # 比较开盘价格和收盘价格，大于等于0.01则返回true,反之返回false
        fall = opening_prices[j] - closing_prices[j] >= 0.01

        fc = np.zeros(dates.size, dtype='3f4')

        ec = np.zeros(dates.size, dtype='3f4')

        # 设置K线颜色
        fc[rise] = (1, 1, 1)
        fc[fall] = (0, 0.5, 0)
        ec[rise] = (1, 0, 0)
        ec[fall] = (0, 0.5, 0)

        plt.bar(dates[j], highest_prices[j] - lowest_prices[j], 0, lowest_prices[j], color=fc,
               edgecolor=ec)
        plt.bar(dates[j], closing_prices[j] - opening_prices[j], 0.2, opening_prices[j], color=fc,
                edgecolor=ec)

        # xy轴边框不可见 x,y轴刻度不可见
        # plt.axis('off')
        # ax.axes.get_xaxis().set_visible(False)
        # ax.axes.get_yaxis().set_visible(False)

        # 将其居中
        plt.margins(1.0, 1.0)

    #如果将savefig放在show后将会显示空白图片，因为放在后面，相当于重新创建了一个空白坐标对象
    plt.gcf().autofmt_xdate()
    plt.savefig('./data/'+str(i+1)+'.png')
    plt.show()
    plt.clf()

