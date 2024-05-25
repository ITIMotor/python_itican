import ctypes
from ctypes import c_int32, c_char_p, c_uint64, c_uint32, c_uint8, c_void_p

import os

current_path = os.path.realpath(__file__)

bin_directory = os.path.abspath(os.path.join(os.path.dirname(current_path)))

bin_path = os.path.join(bin_directory, 'itican.dll')

# 加载DLL
dll = ctypes.CDLL(bin_path, ctypes.RTLD_GLOBAL)
buffer_size = 200

# 定义函数参数和返回类型

# DLLExport int32_t findAllChannels(char *str, int32_t *chnCount);
dll.findAllChannels.argtypes = [c_char_p, ctypes.POINTER(c_int32)]
dll.findAllChannels.restype = c_int32

# DLLExport int32_t getLastError(char *error, int32_t *eventNum);
dll.getLastError.argtypes = [c_char_p, ctypes.POINTER(c_int32)]
dll.getLastError.restype = c_int32

# DLLExport int32_t getChannel(void **channel, char *device, int32_t chnIndex);
dll.getChannel.argtypes = [ctypes.POINTER(c_void_p), c_char_p, c_int32]
dll.getChannel.restype = c_int32

# DLLExport int32_t openChannel(void *channel, int32_t type, int32_t mode);
dll.openChannel.argtypes = [c_void_p, c_int32, c_int32]
dll.openChannel.restype = c_int32

# DLLExport int32_t closeChannel(void *channel);
dll.closeChannel.argtypes = [c_void_p]
dll.closeChannel.restype = c_int32

# DLLExport int32_t getChannelName(void *channel, char *name);
dll.getChannelName.argtypes = [c_void_p, c_char_p]
dll.getChannelName.restype = c_int32

# DLLExport int32_t setBaudRate(void *channel, uint64_t baudRate);
dll.setBaudRate.argtypes = [c_void_p, c_uint64]
dll.setBaudRate.restype = c_int32

# DLLExport int32_t getBaudRate(void *channel, uint64_t *baudRate);
dll.getBaudRate.argtypes = [c_void_p, ctypes.POINTER(c_uint64)]
dll.getBaudRate.restype = c_int32

# DLLExport int32_t setFdBaudRate(void *channel, uint64_t baudRate);
dll.setFdBaudRate.argtypes = [c_void_p, c_uint64]
dll.setFdBaudRate.restype = c_int32

# DLLExport int32_t getFdBaudRate(void *channel, uint64_t *baudRate);
dll.getFdBaudRate.argtypes = [c_void_p, ctypes.POINTER(c_uint64)]
dll.getFdBaudRate.restype = c_int32

# DLLExport int32_t setCustomBaudRate(void *channel, char *baudRate);
dll.setCustomBaudRate.argtypes = [c_void_p, c_char_p]
dll.setCustomBaudRate.restype = c_int32

# DLLExport int32_t getCustomBaudRate(void *channel, char *baudRate);
dll.getCustomBaudRate.argtypes = [c_void_p, c_char_p]
dll.getCustomBaudRate.restype = c_int32

# DLLExport int32_t setMessage(void *channel, uint32_t id, uint8_t type, uint8_t extended, uint8_t *data, uint8_t dataLength, int32_t timeout);
dll.setMessage.argtypes = [c_void_p, c_uint32, c_uint8, c_uint8, ctypes.POINTER(c_uint8), c_uint8, c_int32]
dll.setMessage.restype = c_int32

# DLLExport int32_t setMessages(void *channel, uint32_t *id, uint8_t *type, uint8_t *extended, uint8_t *data, uint8_t *dataLength, uint32_t *items, int32_t timeout);
dll.setMessages.argtypes = [c_void_p, ctypes.POINTER(c_uint32), ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint8),
                            ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint32), c_int32]
dll.setMessages.restype = c_int32

# DLLExport int32_t getMessageCount(void *channel, int32_t *count);
dll.getMessageCount.argtypes = [c_void_p, ctypes.POINTER(c_int32)]
dll.getMessageCount.restype = c_int32

# DLLExport int32_t getMessage(void *channel, uint32_t *id, uint8_t *type, uint8_t *extended, uint8_t *transmitted, uint64_t *timestamp, uint8_t *data, uint8_t *dataLength, int32_t timeout);
dll.getMessage.argtypes = [c_void_p, ctypes.POINTER(c_uint32), ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint8),
                           ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint64), ctypes.POINTER(c_uint8),
                           ctypes.POINTER(c_uint8), c_int32]
dll.getMessage.restype = c_int32

# DLLExport int32_t getMessages(void *channel, uint32_t *id, uint8_t *type, uint8_t *extended, uint8_t *transmitted, uint64_t *timestamp, uint8_t *data, uint8_t *dataLength, uint32_t *items, int32_t timeout);
dll.getMessages.argtypes = [c_void_p, ctypes.POINTER(c_uint32), ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint8),
                            ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint64), ctypes.POINTER(c_uint8),
                            ctypes.POINTER(c_uint8), ctypes.POINTER(c_uint32), c_int32]
dll.getMessages.restype = c_int32

# DLLExport int32_t isTerminationSupported(void *channel, uint8_t *supported);
dll.isTerminationSupported.argtypes = [c_void_p, ctypes.POINTER(c_uint8)]
dll.isTerminationSupported.restype = c_int32

# DLLExport int32_t setTermination(void *channel, uint8_t enabled);
dll.setTermination.argtypes = [c_void_p, c_uint8]
dll.setTermination.restype = c_int32

# DLLExport int32_t isTerminationEnabled(void *channel, uint8_t *enabled);
dll.isTerminationEnabled.argtypes = [c_void_p, ctypes.POINTER(c_uint8)]
dll.isTerminationEnabled.restype = c_int32

# DLLExport int32_t isEchoMessageSupported(void *channel, uint8_t *supported);
dll.isEchoMessageSupported.argtypes = [c_void_p, ctypes.POINTER(c_uint8)]
dll.isEchoMessageSupported.restype = c_int32

# DLLExport int32_t setEchoMessage(void *channel, uint8_t echo);
dll.setEchoMessage.argtypes = [c_void_p, c_uint8]
dll.setEchoMessage.restype = c_int32

# DLLExport int32_t isEchoMessageEnabled(void *channel, uint8_t *echo);
dll.isEchoMessageEnabled.argtypes = [c_void_p, ctypes.POINTER(c_uint8)]
dll.isEchoMessageEnabled.restype = c_int32

# DLLExport int32_t setBusErrorReport(void *channel, uint8_t enabled);
dll.setBusErrorReport.argtypes = [c_void_p, c_uint8]
dll.setBusErrorReport.restype = c_int32

# DLLExport int32_t applySettings(void *channel, uint8_t temporary);
dll.applySettings.argtypes = [c_void_p, c_uint8]
dll.applySettings.restype = c_int32

# DLLExport int32_t isTxModeSupported(void *channel, uint8_t mode, uint8_t *supported);
dll.isTxModeSupported.argtypes = [c_void_p, c_uint8, ctypes.POINTER(c_uint8)]
dll.isTxModeSupported.restype = c_int32

# DLLExport int32_t setTxMode(void *channel, uint8_t mode);
dll.setTxMode.argtypes = [c_void_p, c_uint8]
dll.setTxMode.restype = c_int32

# DLLExport int32_t setTxTiming(void *channel, uint32_t id, int32_t time);
dll.setTxTiming.argtypes = [c_void_p, c_uint32, c_int32]
dll.setTxTiming.restype = c_int32

# DLLExport int32_t isBlinkSupported(void *channel, uint8_t *supported);
dll.isBlinkSupported.argtypes = [c_void_p, ctypes.POINTER(c_uint8)]
dll.isBlinkSupported.restype = c_int32

# DLLExport int32_t blinkChannel(void *channel, uint8_t blink);
dll.blinkChannel.argtypes = [c_void_p, c_uint8]
dll.blinkChannel.restype = c_int32

# DLLExport int32_t isChannelBlinking(void *channel, uint8_t *blinking);
dll.isChannelBlinking.argtypes = [c_void_p, ctypes.POINTER(c_uint8)]
dll.isChannelBlinking.restype = c_int32
