# 这是一个示例 Python 脚本。

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import iticanwrapper
from iticanwrapper import itican_py_wrapper


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
    chn_index_s = []
    chn_count = []
    target_chn_container0 = []
    target_chn_container1 = []

    rt = itican_py_wrapper.ITICANChannel.find_all_channels(chn_index_s, chn_count)
    chn0 = ITICANChannel.get_channel(target_chn_container0, chn_index_s[0])
    if chn0 == 0:
        target_chn_container0[0].instance_test()
    chn1 = ITICANChannel.get_channel(target_chn_container1, chn_index_s[1])
    if chn1 == 0:
        target_chn_container1[0].instance_test()

    rt1 = target_chn_container0[0].open_channel(OpenType.FD_CAN, OpenMode.Normal)
    chn_name = []
    rt2 = target_chn_container0[0].get_channel_name(chn_name)
    data = [1, 2, 3, 4, 5, 6]
    can_msg = CANMessage(1, MessageType.Classic_CAN, 0, data)
    rt3 = target_chn_container0[0].set_message(can_msg, 10)

    err_spec = []
    rrt = ITICANChannel.get_last_error(-189, err_spec)

    cc = ITICANChannel(0)
    cc.instance_test()

    print()
    print(chn_index_s)
    print(chn_count)

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
