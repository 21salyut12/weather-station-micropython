from machine import Pin, ADC

rain_pin = ADC(Pin(13))
rain_pin.atten(ADC.ATTN_11DB)

calibration_coefficients = {"a": 0.2, "b": 0.5}


def get_rainfall(analog_voltage):
    a = calibration_coefficients["a"]
    b = calibration_coefficients["b"]
    rainfall = a * analog_voltage + b
    return rainfall


def calibrate():
    reference_values = {0.1: 0.0, 0.3: 5.0, 0.5: 10.0, 0.7: 20.0}

    for voltage, rainfall in reference_values.items():
        analog_voltage = rain_pin.read() / 4095.0
        calibrated_rainfall = get_rainfall(analog_voltage)
        print(
            "Analog Voltage: {:.3f}, Reference Rainfall: {:.1f}, Calibrated Rainfall: {:.1f}".format(
                analog_voltage, rainfall, calibrated_rainfall
            )
        )


calibrate()
