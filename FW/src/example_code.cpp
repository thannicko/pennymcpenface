#include <TMCStepper.h>
#include <Wire.h>
#include <Adafruit_PWMServoDriver.h>
// #include "ADS1X15.h"
// #include <Adafruit_ADS1X15.h>
#include "Adafruit_ADS1X15.h"

constexpr pin_size_t pin_chipSelA = 21; // Mot0
constexpr pin_size_t pin_chipSelB = 18; // Enc0
constexpr pin_size_t pin_chipSelC = 25; // Mot1
constexpr pin_size_t pin_chipSelD = 24; // Enc1
constexpr pin_size_t pin_SPI0SCK = 22;
constexpr pin_size_t pin_SPI0MOSI = 19;
constexpr pin_size_t pin_SPI0MISO = 20;
constexpr pin_size_t in1Pin = 1;
constexpr pin_size_t in2Pin = 0;
// Stepper Motor OConfig
constexpr uint16_t MOTOR_CURRENT = 4000;
constexpr uint8_t DEFAULT_IRUN = 31;
constexpr uint8_t DEFAULT_IHOLD = 16;
constexpr uint8_t TMC_TOFFRUN = 4;