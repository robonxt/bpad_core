#ifndef Pins_Arduino_h
#define Pins_Arduino_h

#include <stdint.h>
#include "soc/soc_caps.h"

#define USB_VID 0x303a
#define USB_PID 0x1001

// Default Serial Pins
static const uint8_t TX = 43;
static const uint8_t RX = 44;

// System I2C Bus (Fast Mode 400kHz)
static const uint8_t SDA = 18;
static const uint8_t SCL = 17;

// Display SPI / QSPI Bus (ST77916 360x360 Round)
static const uint8_t SS   = 14;
static const uint8_t MOSI = 5;  // LCD_D0
static const uint8_t MISO = 4;  // LCD_D1
static const uint8_t SCK  = 6;  // LCD_SCK

#define TFT_CS      14
#define TFT_RST     42
#define TFT_DC      40  // Hardware Mode Strap (Pulled LOW for QSPI)
#define TFT_BL      39  // Backlight LEDC PWM (LEDC Timer 0, Ch 0)
#define TFT_SCK     6
#define TFT_D0      5
#define TFT_D1      4
#define TFT_D2      2
#define TFT_D3      1
#define TFT_WIDTH   360
#define TFT_HEIGHT  360

// Touch Controller (CST816S at 0x15)
#define TOUCH_IRQ   38
#define TOUCH_RST   42  // Shared with TFT_RST
#define TOUCH_SDA   18
#define TOUCH_SCL   17
#define TOUCH_ADDR  0x15

// Audio & Haptics
#define PIN_AMP_PWR     13
#define AUDIO_DAC_ADDR  0x61  // MCP4725
#define HAPTIC_DAC_ADDR 0x60  // MCP4728 (4-Channel)

// IMU (ICM-42607-P at 0x69, -90 deg PCB rotation offset)
#define IMU_ADDR    0x69

// Storage (XinYY SD32G 4GB SD-NAND, 4-bit SDMMC)
#define SD_MMC_CLK  9
#define SD_MMC_CMD  12
#define SD_MMC_D0   11
#define SD_MMC_D1   10
#define SD_MMC_D2   7
#define SD_MMC_D3   8

// Analog Inputs
static const uint8_t A0  = 1;
static const uint8_t A1  = 2;
static const uint8_t A2  = 3;
static const uint8_t A3  = 4;
static const uint8_t A4  = 5;
static const uint8_t A5  = 6;
static const uint8_t A6  = 7;
static const uint8_t A7  = 8;
static const uint8_t A8  = 9;
static const uint8_t A9  = 10;
static const uint8_t A10 = 11;
static const uint8_t A11 = 12;
static const uint8_t A12 = 13;
static const uint8_t A13 = 14;
static const uint8_t A14 = 15;
static const uint8_t A15 = 16;
static const uint8_t A16 = 17;
static const uint8_t A17 = 18;
static const uint8_t A18 = 19;
static const uint8_t A19 = 20;

// Touch Pad Channels
static const uint8_t T1  = 1;
static const uint8_t T2  = 2;
static const uint8_t T3  = 3;
static const uint8_t T4  = 4;
static const uint8_t T5  = 5;
static const uint8_t T6  = 6;
static const uint8_t T7  = 7;
static const uint8_t T8  = 8;
static const uint8_t T9  = 9;
static const uint8_t T10 = 10;
static const uint8_t T11 = 11;
static const uint8_t T12 = 12;
static const uint8_t T13 = 13;
static const uint8_t T14 = 14;

#endif /* Pins_Arduino_h */
