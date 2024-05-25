/**
 * @file canwrapper.h
 * @author Julles
 * @brief Define API for can card.
 * @version 1.0
 * @date 2023-09-18
 *
 * @copyright ITIMotor Copyright (c) 2023
 *
 * @History
 * @author Julles
 * @date 2023-11-25
 * @version 1.1
 * @Update Add isTxModeSupported isEchoMessageSupported function;
 *         Rename getEchoMessage to isEchoMessageEnabled.
 *
 * @author Julles
 * @date 2024-03-21
 * @version 1.2
 * @Update Add MAX_LEN defined;Add blink function
 */

#ifndef CAN_WRAPPER_H
#define CAN_WRAPPER_H

#define WRAPPER_MAX_CHANNELS_LEN 2000
#define WRAPPER_MAX_ERROR_LEN 100
#define WRAPPER_MAX_NAME_LEN 100
#define WRAPPER_MAX_BITRATE_LEN 128

#ifndef DLLExport
#ifdef __linux__
#define DLLExport __attribute__((visibility("default")))
#else
#define DLLExport __declspec(dllexport)
#endif
#endif

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdint.h>

/**
 * @brief find all channels
 *
 * @param str all channels, separated by tab, up to 2000 bytes in size
 * @param chnCount channels count
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t findAllChannels(char *str, int32_t *chnCount);

/**
 * @brief Get the Last Error
 *
 * @param error error description
 * @param eventNum  error code
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getLastError(char *error, int32_t *eventNum);

/**
 * @brief get the channel handle
 *
 * @param channel channel handle, nullptr if failed
 * @param device device name or channel name or serial number, used to identify device or channel.
 * @param chnIndex channel index in device
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getChannel(void **channel, char *device, int32_t chnIndex);

/**
 * @brief open the channel handle
 *
 * @param channel channel handle
 * @param type 0:can    1:canfd         2:canfd-brs     3:canfd-non iso
 * @param mode 0:normal 1:listen only   2:loopBack
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t openChannel(void *channel, int32_t type, int32_t mode);

/**
 * @brief close the channel handle
 *
 * @param channel channel handle
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t closeChannel(void *channel);

/**
 * @brief Get the Channel Name
 *
 * @param channel channel handle
 * @param name the name or description of channel
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getChannelName(void *channel, char *name);

/**
 * @brief Set the Baud Rate
 *
 * @param channel channel handle
 * @param baudRate new baudRate
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setBaudRate(void *channel, uint64_t baudRate);

/**
 * @brief Get the Baud Rate
 *
 * @param channel channel handle
 * @param baudRate new baudRate
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getBaudRate(void *channel, uint64_t *baudRate);

/**
 * @brief Set the Fd Baud Rate
 *
 * @param channel channel handle
 * @param baudRate new canfd baudRate
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setFdBaudRate(void *channel, uint64_t baudRate);

/**
 * @brief Get the Fd Baud Rate
 *
 * @param channel channel handle
 * @param baudRate canfd baudRate
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getFdBaudRate(void *channel, uint64_t *baudRate);

/**
 * @brief Set the channel's Custom Baud Rate
 *
 * @note Sometimes the device's custom baud rate is identified by a string, so you need to call this function instead of setBaudrate
 * @param channel channel handle
 * @param baudRate custom baudRate
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setCustomBaudRate(void *channel, char *baudRate);

/**
 * @brief Get the Custom BaudRate
 *
 * @note Sometimes the device's custom baud rate is identified by a string, so you need to call this function instead of getBaudrate
 * @param channel channel handle
 * @param baudRate custom baudRate
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getCustomBaudRate(void *channel, char *baudRate);

/**
 * @brief Set the Message
 *
 * @note set or transmit message,if the sending mode is automatic, it is to set the message otherwise it will send frame immediately.
 * @param channel channel handle
 * @param id can frame id
 * @param type can frame type
 * @param extended can frame id is extended
 * @param data can frame data
 * @param dataLength can frame dataLength (dlc)
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setMessage(void *channel, uint32_t id, uint8_t type, uint8_t extended, uint8_t *data, uint8_t dataLength, int32_t timeout);

/**
 * @brief Set the Messages
 *
 * @param channel [in] channel handle
 * @param id [in] can frame id array
 * @param type [in] can frame type array
 * @param extended [in] can frame id is extended array
 * @param data [in] can frame row data array, it it one-dimensional array that identifying the length of each message in @p dataLength
 * @param dataLength [in] can frame data length every can frame(dlc array)
 * @param items [in][out] can frame length
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setMessages(void *channel, uint32_t *id, uint8_t *type, uint8_t *extended, uint8_t *data, uint8_t *dataLength, uint32_t *items, int32_t timeout);

/**
 * @brief Get the receive Message Count
 *
 * @param channel channel handle
 * @param count message count
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getMessageCount(void *channel, int32_t *count);

/**
 * @brief Get one receive message
 *
 * @param channel [in] channel handle
 * @param id [out] can frame id
 * @param type [out] can frame type
 * @param extended [out] can frame id is extended
 * @param transmitted [out] can frame is transmitted
 * @param timestamp [out] can frame timestamp
 * @param data [out] can frame data array
 * @param dataLength [out] can frame data length (dlc)
 * @param timeout [in] receive timeout ms
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getMessage(void *channel, uint32_t *id, uint8_t *type, uint8_t *extended, uint8_t *transmitted, uint64_t *timestamp, uint8_t *data, uint8_t *dataLength, int32_t timeout);

/**
 * @brief Get the receive data
 *
 * @param channel [in] channel handle
 * @param id [out] can frame id array
 * @param type [out] can frame type array
 * @param extended [out] can frame id is extended array
 * @param transmitted [out] can frame is transmitted array
 * @param timestamp [out] can frame timestamp array
 * @param data [out] can frame row data array, it it one-dimensional array that identifying the length of each message in @p dataLength
 * @param dataLength [out] data length every can frame (dlc array)
 * @param items [in][out] the number of frame you want to receive\n
 * - if items is positive (or 0), the size of value arrays is no greater than this number.\n
 * - if items is negative (typically -1), the maximum number of values is returned.
 * @param timeout [in] receive timeout ms\n
 * - If timeout is zero, the function does not wait and immediately returns
 *      all available frame values up to @p items specifies.\n
 * - If timeout is negative, the function waits indefinitely for @p items values.\n
 * - If timeout is positive, the function waits for @p items values,then returns that number.
 *      If the values do not arrive prior to the timeout, an error is returned.
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t getMessages(void *channel, uint32_t *id, uint8_t *type, uint8_t *extended, uint8_t *transmitted, uint64_t *timestamp, uint8_t *data, uint8_t *dataLength, uint32_t *items, int32_t timeout);

/**
 * @brief Whether termination is supported
 *
 * @param channel channel handle
 * @param supported 1 is supported
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t isTerminationSupported(void *channel, uint8_t *supported);

/**
 * @brief Set the Termination Enabled
 *
 * @param channel channel handle
 * @param enabled enabled
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setTermination(void *channel, uint8_t enabled);

/**
 * @brief Whether termination is enabled
 *
 * @param channel channel handle
 * @param enabled 1 is enabled
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t isTerminationEnabled(void *channel, uint8_t *enabled);


/**
 * @brief Whether echo message (receive already been sent message) is supported
 *
 * @param channel channel handle
 * @param supported 1 is supported
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t isEchoMessageSupported(void *channel, uint8_t *supported);

/**
 * @brief Set whether to read messages that have already been sent (called echo message)
 *
 * @param channel channel handle
 * @param echo enable echo message(receive already been sent message)
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setEchoMessage(void *channel, uint8_t echo);

/**
 * @brief Get whether to read messages that have already been sent (called echo message)
 *
 * @param channel channel handle
 * @param echo 1 if is echo message (receive already been sent message)
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t isEchoMessageEnabled(void *channel, uint8_t *echo);

/**
 * @brief This function turns error frame reporting on or off.
 *
 * @param channel channel handle
 * @param enabled Default value is \c 1, error frame reporting is turned on.
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setBusErrorReport(void *channel, uint8_t enabled);

/**
 * @brief Apply the settings
 *
 * @param channel channel handle
 * @param temporary write to rom or just temporary
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t applySettings(void *channel, uint8_t temporary);

/**
 * @brief Check whether the channel supports the specified sending mode
 *
 * @param channel channel handle
 * @param mode 0:normal,1:auto send,2:queue mode
 * @param supported whether the specified sending mode is supported
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t isTxModeSupported(void *channel, uint8_t mode, uint8_t *supported);

/**
 * @brief Set the Tx Mode
 *
 * @param channel channel handle
 * @param mode 0:normal,1:auto send,2:queue mode
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setTxMode(void *channel, uint8_t mode);

/**
 * @brief Set the Tx Timing in auto send or queue mode
 *
 * @param channel channel handle
 * @param id uint32_t message id
 * @param time int32_t auto send time in ms
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t setTxTiming(void *channel, uint32_t id, int32_t time);

/**
 * @brief Check whether the channel supports blinking
 *
 * @param channel channel handle
 * @param supported whether the blinking is supported
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t isBlinkSupported(void *channel, uint8_t *supported);

/**
 * @brief Blink to identify channel
 *
 * @param channel channel handle
 * @param blink Blinking On or off
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t blinkChannel(void *channel, uint8_t blink);

/**
 * @brief Indicates whether the channel is blinking
 *
 * @param channel channel handle
 * @param blinking Blinking On or off
 * @return int32_t Returns zero on success, otherwise returns a negative number, and a positive number represents a warning.
 */
DLLExport int32_t isChannelBlinking(void *channel, uint8_t *blinking);

#ifdef __cplusplus
}
#endif // __cplusplus

#endif // CAN_WRAPPER_H