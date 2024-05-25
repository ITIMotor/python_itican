import ctypes

from iticanwrapper.bin import importDLL
from enum import Enum

__all__ = ['OpenType', 'OpenMode', 'MessageType', 'TxMode', 'CANMessage', 'ITICANChannel']

_debug_mode = False

_CAN_Clock_Frequency_MHz = 80


class OpenType(Enum):
    Classic_CAN = 0
    FD_CAN = 1
    FD_CAN_BRS = 2
    FD_CAN_NO_ISO = 3


class OpenMode(Enum):
    Normal = 0
    Listen = 1
    Loopback = 2


class MessageType(Enum):
    Classic_CAN = 0
    Remote = 1
    FD_CAN = 16
    FD_BRS_CAN = 24


class TxMode(Enum):
    Normal = 0
    AUTO_SEND = 1
    QUEUE_SEND = 2


class CANMessage:

    def __init__(self, can_id, can_type, can_extended, can_data):
        self.id_ = can_id
        self.type_: MessageType = can_type
        self.extended_ = can_extended
        self.data_ = can_data


initialization_error = "this instance is not acquired from ITICANChannel's static method"


class ITICANChannel:

    def __init__(self, pointer):
        self.chn_pointer = pointer
        self._inner_flag = False

    @staticmethod
    def find_all_channels(chn_names_output: list, chn_count_output: list):
        """
        查找所有通道引用名
        :param chn_names_output: 清空 list 后，传出存在的所有通道索引名的列表
        :param chn_count_output: 清空 list 后，传出通道索引个数，保存在 index=0 处
        :return:
        """
        chn_names_output.clear()
        chn_count_output.clear()
        str_temp = ctypes.create_string_buffer(500)
        chn_count = ctypes.c_int()
        result = importDLL.dll.findAllChannels(str_temp, ctypes.byref(chn_count))
        str_temp_ = str_temp.value.decode('utf-8')

        for item in str_temp_.split('\t'):
            chn_names_output.append(item)
        chn_count_output.append(chn_count.value)
        if _debug_mode:
            print("debug:finAllChannels函数调用结果:", result)
            print("通道索引:", str_temp_.value)
            print("通道数量:", chn_count.value)
        return result

    @staticmethod
    def get_channel(chn_container: list, chn_index: str):
        """
        获取通道
        @param chn_container: 用于传出通道实例对象，清空 list 后，保存在 index=0 处
        @param chn_index: 目标通道对应索引名
        @return: getLastError 错误码
        """
        chn_container.clear()
        # 转换参数
        str_temp = ctypes.create_string_buffer(500)
        str_temp.value = str(chn_index).encode('utf-8')
        int_param = ctypes.c_int32(0)
        chn_ptr = ctypes.c_void_p()
        # 发起dll调用
        result = importDLL.dll.getChannel(ctypes.byref(chn_ptr), str_temp.value, int_param)
        if result == 0:
            instance = ITICANChannel(chn_ptr)
            instance._inner_flag = True
            chn_container.append(instance)
        return result

    @staticmethod
    def get_last_error(error_code, error_specification_output: list):
        """
        解析错误码
        :param error_code: 其他函数返回值（错误码）
        :param error_specification_output: 清空 list，在 index=0 处填入错误描述
        :return:
        """
        str_temp = ctypes.create_string_buffer(500)
        error_code_temp = ctypes.c_int32(error_code)
        result = importDLL.dll.getLastError(str_temp, ctypes.byref(error_code_temp))
        str_temp_ = str_temp.value.decode('utf-8')
        error_specification_output.clear()
        error_specification_output.append(str_temp_)
        return result

    def open_channel(self, open_type: OpenType, open_mode: OpenMode):
        """
        开启通道
        @param open_type: OpenType
        @param open_mode: OpenMode
        @return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        type_ = 0
        mode_ = 0
        if open_type == OpenType.Classic_CAN:
            type_ = 0
        elif open_type == OpenType.FD_CAN:
            type_ = 1
        elif open_type == OpenType.FD_CAN_BRS:
            type_ = 2
        elif open_type == OpenType.FD_CAN_NO_ISO:
            type_ = 3

        if open_mode == OpenMode.Normal:
            mode_ = 0
        elif open_mode == OpenMode.Listen:
            mode_ = 1
        elif open_mode == OpenMode.Loopback:
            mode_ = 2

        # 转换参数
        type_param = ctypes.c_int32(type_)
        mode_param = ctypes.c_int32(mode_)

        # 发起dll调用
        result = importDLL.dll.openChannel(self.chn_pointer, type_param, mode_param)

        return result

    # 关闭通道  none
    def close_channel(self):
        """
        关闭通道
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        result = importDLL.dll.closeChannel(self.chn_pointer)
        return result

    def get_channel_name(self, chn_name_output: list):
        """

        :param chn_name_output: list ; 清空 list 后，获取通道索引名称，保存在 index=0 处
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        chn_name_output.clear()
        str_temp = ctypes.create_string_buffer(500)
        result = importDLL.dll.getChannelName(self.chn_pointer, str_temp)
        chn_name = str_temp.value.decode('utf-8')
        chn_name_output.append(chn_name)
        return result

    def set_baud_rate(self, baud_rate):
        """
        设置通道仲裁段波特率
        :param baud_rate: uint64 ; 仲裁段波特率参数
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        baud_rate_ = ctypes.c_uint64(baud_rate)
        result = importDLL.dll.setBaudRate(self.chn_pointer, baud_rate_)
        return result

    def set_custom_baud_rate(self, brp, ts1, ts2, sjw):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        base = 0xA0000000
        tq = int(brp * 1000 / _CAN_Clock_Frequency_MHz)
        ts1 -= 1
        ts2 -= 1
        base += tq * 0x100000000
        base += sjw * 0x10000
        base += ts1 * 0x100
        base += ts2
        result = self.set_baud_rate(base)
        return result

    def get_baud_rate(self, baud_rate_output: list):
        """
        获取仲裁段波特率
        :param baud_rate_output: list ; 传出仲裁段波特率，清空 list 后，保存仲裁段波特率在 index=0 处
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        baud_rate_ = ctypes.c_uint64(0)
        result = importDLL.dll.getBaudRate(self.chn_pointer, ctypes.byref(baud_rate_))
        if result == 0:
            baud_rate_output.clear()
            baud_rate_output.append(baud_rate_.value)
        return result

    def set_fd_baud_rate(self, baud_rate_input: int):
        """
        设置数据段波特率
        :param baud_rate_input: 数据段波特率参数
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        baud_rate_ = ctypes.c_uint64(baud_rate_input)
        result = importDLL.dll.setFdBaudRate(self.chn_pointer, baud_rate_)
        return result

    def set_custom_fd_baud_rate(self, brp, ts1, ts2, sjw, tdc_o):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        base = 0xA0000000
        tdc = 0
        if tdc_o > 0:
            tdc = 1
        tq = int(brp * 1000 / _CAN_Clock_Frequency_MHz)
        ts1 -= 1
        ts2 -= 1
        tdc_o -= 1
        sjw -= 1
        base += tdc * 0x80000000000000
        base += tdc_o * 0x10000000000
        base += tq * 0x2000
        base += ts1 * 0x100
        base += ts2 * 0x10
        base += sjw
        result = self.set_fd_baud_rate(base)
        return result

    def get_fd_baud_rate(self, baud_rate_output: list):
        """
        获取数据段波特率参数
        :param baud_rate_output: list ; 传出数据段波特率参数，清空 list 后， 保存在 index=0 处
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        baud_rate_ = ctypes.c_uint64(0)
        result = importDLL.dll.getBaudRate(self.chn_pointer, ctypes.byref(baud_rate_))
        if result == 0:
            baud_rate_output.clear()
            baud_rate_output.append(baud_rate_.value)
        return result

    def get_custom_baud_rate(self, custom_baud_rate_str_output: list):
        """
        获取自定义波特率
        :param custom_baud_rate_str_output: list ; 传出字符串形式的波特率参数，清空 list， 保存在 index=0 的位置
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        str_temp = ctypes.create_string_buffer(500)
        result = importDLL.dll.getCustomBaudRate(self.chn_pointer, str_temp)
        if result == 0:
            baud_rate_ = str_temp.value.decode('utf-8')
            custom_baud_rate_str_output.append(baud_rate_)
        return result

    def set_message(self, one_message: CANMessage, timeout=0):
        """
        设置一条 CAN 消息
        :param one_message: CAN 消息（CANMessage）
        :param timeout: 设置 CAN 消息操作的超时时间，底层使用队列缓冲则该参数无效（底层使用队列缓冲）
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        can_id_ = ctypes.c_uint32(one_message.id_)
        message_type_ = ctypes.c_uint8(one_message.type_.value)
        is_extended_ = ctypes.c_uint8(one_message.extended_)
        data_array_ = (ctypes.c_uint8 * len(one_message.data_))(*(one_message.data_))
        date_length_ = ctypes.c_uint8(len(one_message.data_))
        timeout_ = ctypes.c_int32(timeout)
        result = importDLL.dll.setMessage(self.chn_pointer, can_id_, message_type_, is_extended_, data_array_,
                                          date_length_,
                                          timeout_)
        return result

    def set_messages(self, messages_container: list, items_output: list, timeout=0):
        """
        设置多条 CAN 消息
        :param messages_container: list ; 容纳多条 CAN 消息（CANMessage）
        :param items_output: list ; 传出设置成功的 CAN 消息的个数，清空 list 后，保存到 index=0 处
        :param timeout: 设置单条 CAN 消息的超时时间
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        error_flag = False
        items_output.clear()
        counter = 0
        for can_msg in messages_container:
            result = self.set_message(can_msg, timeout)
            if result == 0:
                counter += 1
            else:
                items_output.append(counter)
                return result
        items_output.append(counter)
        return 0

    def get_message_count(self, message_count_output: list):
        """
        传出已接收CAN消息个数
        :param message_count_output: list ; 传出传出已接收CAN消息个数，清空 list，保存在 index=0 处
        :return: getLastError 错误码
        """
        if not self._inner_flag:
            raise TypeError(initialization_error)
        count_temp = ctypes.c_int32(0)
        result = importDLL.dll.getMessageCount(self.chn_pointer, ctypes.byref(count_temp))
        if result == 0:
            val = count_temp.value
            message_count_output.clear()
            message_count_output.append(val)
        return result

    def get_message(self, one_message_output: list, timeout=0):

        if not self._inner_flag:
            raise TypeError(initialization_error)
        id_temp = ctypes.c_uint32(0)
        message_type_temp = ctypes.c_uint8(0)
        can_extended_temp = ctypes.c_uint8(0)
        transmitted_temp = ctypes.c_uint8(0)  # no output
        timestamp_temp = ctypes.c_uint64(0)  # no output
        data_temp = (ctypes.c_uint8 * 64)()
        data_l_temp = ctypes.c_uint8(0)
        timeout_temp = ctypes.c_int32(timeout)

        result = importDLL.dll.getMessage(self.chn_pointer, ctypes.byref(id_temp), ctypes.byref(message_type_temp),
                                          ctypes.byref(can_extended_temp), ctypes.byref(transmitted_temp),
                                          ctypes.byref(timestamp_temp), data_temp, ctypes.byref(data_l_temp),
                                          timeout_temp)
        if result == 0:
            data_list = list(data_temp)[:data_l_temp.value]
            one_message_output.clear()
            one_message_output.append(
                CANMessage(id_temp.value, MessageType(message_type_temp.value), can_extended_temp.value, data_list[:]))
        return result

    def get_messages(self, messages_container: list, items_in_output: list, timeout: int = 0):

        if not self._inner_flag:
            raise TypeError(initialization_error)
        messages_container.clear()
        counter = 0
        for i in range(items_in_output[0]):
            one_message = []
            rt_val = self.get_message(one_message, timeout)
            if rt_val == 0:
                messages_container.append(one_message[0])
                counter += 1
            else:
                items_in_output[0] = counter
                return rt_val
        items_in_output[0] = counter
        return 0

    def check_if_termination_supported(self, check_result: list):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        supported_temp = ctypes.c_uint8(0)
        result = importDLL.dll.isTerminationSupported(self.chn_pointer, ctypes.byref(supported_temp))
        if result == 0:
            check_result.clear()
            check_result.append(supported_temp.value != 0)
        return result

    def set_termination(self, enable: bool):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        result = 0
        if enable:
            result = importDLL.dll.setTermination(self.chn_pointer, ctypes.c_uint8(1))
        else:
            result = importDLL.dll.setTermination(self.chn_pointer, ctypes.c_uint8(0))
        return result

    def check_if_termination_enabled(self, enabled_output: list):

        if not self._inner_flag:
            raise TypeError(initialization_error)
        enabled_temp = ctypes.c_uint8(0)
        result = importDLL.dll.isTerminationEnabled(self.chn_pointer, ctypes.byref(enabled_temp))
        if result == 0:
            enabled_output.clear()
            enabled_output.append(enabled_temp.value != 0)
        return result

    def check_if_echo_message_supported(self, check_result: list):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        supported_temp = ctypes.c_uint8(0)
        result = importDLL.dll.isEchoMessageSupported(self.chn_pointer, ctypes.byref(supported_temp))
        if result == 0:
            check_result.clear()
            check_result.append(supported_temp.value != 0)
        return result

    def set_echo_message(self, enable: bool):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        result = 0
        if enable:
            result = importDLL.dll.setTermination(self.chn_pointer, ctypes.c_uint8(1))
        else:
            result = importDLL.dll.setTermination(self.chn_pointer, ctypes.c_uint8(0))
        return result

    def check_if_echo_message_enabled(self, check_result: list):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        enabled_temp = ctypes.c_uint8(0)
        result = importDLL.dll.isEchoMessageEnabled(self.chn_pointer, ctypes.byref(enabled_temp))
        if result == 0:
            check_result.clear()
            check_result.append(enabled_temp.value != 0)
        return result

    def bus_error_report(self, enable: bool):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        result = 0
        if enable:
            result = importDLL.dll.setBusErrorReport(self.chn_pointer, ctypes.c_uint8(1))
        else:
            result = importDLL.dll.setBusErrorReport(self.chn_pointer, ctypes.c_uint8(0))
        return result

    def apply_settings(self, temporary: bool):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        result = 0
        if temporary:
            result = importDLL.dll.applySettings(self.chn_pointer, ctypes.c_uint8(1))
        else:
            result = importDLL.dll.applySettings(self.chn_pointer, ctypes.c_uint8(0))
        return result

    def check_if_tx_mode_supported(self, mode: TxMode, check_result):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        mode_temp = ctypes.c_uint8(mode.value)
        supported_temp = ctypes.c_uint8(0)
        result = importDLL.dll.isTxModeSupported(self.chn_pointer, mode_temp, ctypes.byref(supported_temp))
        if result == 0:
            check_result.clear()
            check_result.append(supported_temp.value != 0)
        return result

    def set_tx_mode(self, mode: TxMode):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        mode_temp = ctypes.c_uint8(mode.value)
        result = importDLL.dll.setTxMode(self.chn_pointer, mode_temp)
        return result

    def set_tx_timing(self, can_id, period):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        can_id_temp = ctypes.c_uint32(can_id)
        period_temp = ctypes.c_int32(period)
        result = importDLL.dll.setTxTiming(self.chn_pointer, can_id_temp, period_temp)
        return result

    def check_if_blink_supported(self, check_result: list):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        supported_temp = ctypes.c_uint8(0)
        result = importDLL.dll.isBlinkSupported(self.chn_pointer, ctypes.byref(supported_temp))
        if result == 0:
            check_result.clear()
            check_result.append(supported_temp.value != 0)
        return result

    def set_channel_blink(self, enable: bool):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        result = 0
        if enable:
            result = importDLL.dll.blinkChannel(self.chn_pointer, ctypes.c_uint8(1))
        else:
            result = importDLL.dll.blinkChannel(self.chn_pointer, ctypes.c_uint8(0))
        return result

    def check_if_channel_blinking(self, check_result: list):
        if not self._inner_flag:
            raise TypeError(initialization_error)
        status = ctypes.c_uint8(0)
        result = importDLL.dll.isChannelBlinking(self.chn_pointer, ctypes.byref(status))
        if result == 0:
            check_result.clear()
            check_result.append(status.value != 0)
        return result


if __name__ == '__main__':

    chn_index_s = []
    chn_count = []
    target_chn_container0 = []
    target_chn_container1 = []

    rt = ITICANChannel.find_all_channels(chn_index_s, chn_count)
    chn0 = ITICANChannel.get_channel(target_chn_container0, chn_index_s[0])

    rt1 = target_chn_container0[0].open_channel(OpenType.FD_CAN, OpenMode.Normal)
    chn_name = []
    rt2 = target_chn_container0[0].get_channel_name(chn_name)
    rt3 = target_chn_container0[0].set_custom_baud_rate(4, 34, 5, 4)
    rt4 = target_chn_container0[0].set_custom_fd_baud_rate(2, 15, 4, 4, 16)
    baud_rate = []
    rt5 = target_chn_container0[0].get_baud_rate(baud_rate)
    data = [1, 2, 3, 4, 5, 6]
    can_msg = CANMessage(1, MessageType.Classic_CAN, 0, data)
    rt3 = target_chn_container0[0].set_message(can_msg, 10)

    err_spec = []
    rrt = ITICANChannel.get_last_error(-189, err_spec)
    cc = ITICANChannel(1)
    cc.instance_test()

    print()
    print(chn_index_s)
    print(chn_count)
