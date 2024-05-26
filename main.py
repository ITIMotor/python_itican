# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import time
import threading

from iticanwrapper import ITICANChannel
from iticanwrapper import MessageType
from iticanwrapper import OpenType
from iticanwrapper import OpenMode
from iticanwrapper import CANMessage
from iticanwrapper import TxMode


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


def ListenMessageTest(chn):
    counter=0
    while True:
        can_msg = []
        rt = chn.get_message(can_msg, 5000)
        if rt == 0:
            counter += 1
            print(counter,can_msg[0].id_, can_msg[0].type_, can_msg[0].extended_, can_msg[0].data_)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    chn_index_s = []
    chn_count = []
    error_spec = []
    rt = ITICANChannel.find_all_channels(chn_index_s, chn_count)
    ITICANChannel.get_last_error(rt, error_spec)
    print("所有通道索引：", chn_index_s)
    print("检索通道个数：", chn_count)
    print("检查错误状态：", error_spec)
    ITICANChannel.get_last_error(rt, error_spec)
    print("检查错误状态：", error_spec)
    target_chn_container0 = []
    rt = ITICANChannel.get_channel(target_chn_container0, chn_index_s[0])
    ITICANChannel.get_last_error(rt, error_spec)
    print("获取通道引用：", target_chn_container0)
    print("检查错误状态：", error_spec)
    chn_name = []
    rt = target_chn_container0[0].get_channel_name(chn_name)
    print("获取通道索引：", chn_name)
    ITICANChannel.get_last_error(rt, error_spec)
    print("检查错误状态：", error_spec)
    rt = target_chn_container0[0].open_channel(OpenType.FD_CAN, OpenMode.Normal)
    rt = target_chn_container0[0].set_baud_rate(500000)  # 500k 仲裁段波特率
    ITICANChannel.get_last_error(rt, error_spec)
    print("检查错误状态：", error_spec)
    rt = target_chn_container0[0].set_fd_baud_rate(2000000)  # 2M 数据段波特率
    ITICANChannel.get_last_error(rt, error_spec)
    print("检查错误状态：", error_spec)
    rt = target_chn_container0[0].apply_settings(True)
    ITICANChannel.get_last_error(rt, error_spec)
    print("检查错误状态：", error_spec)
    data = [1, 2, 3, 4, 5, 6,7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,20]
    can_msg = CANMessage(1, MessageType.FD_BRS_CAN, 0, data)
    listenThread = threading.Thread(target=ListenMessageTest, args=(target_chn_container0[0],))
    listenThread.daemon = True
    listenThread.start()
    for i in range(50000):
        rt = target_chn_container0[0].set_message(can_msg, 0)
        if rt != 0:
            break
    ITICANChannel.get_last_error(rt, error_spec)
    print("检查错误状态：", error_spec)
    input()
    rt=target_chn_container0[0].close_channel()
    ITICANChannel.get_last_error(rt, error_spec)
    print("检查错误状态：", error_spec)

    print()
    print(chn_index_s)
    print(chn_count)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
