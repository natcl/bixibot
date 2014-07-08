// This #include statement was automatically added by the Spark IDE.
#include "elapsedMillis/elapsedMillis.h"

// This #include statement was automatically added by the Spark IDE.
#include "neopixel/neopixel.h"


#define OFF 48
#define GREEN 49
#define RED 50

// Pins
int redPin = A0;
int greenPin = A4;
int bluePin = A1;
int buttonPin = D5;
int neoPixelPin = D7;

int numLeds = 15;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(numLeds, neoPixelPin, WS2812B);

elapsedMillis timeElapsed;
int fadeTime = 2000;
String lastCommand = "000000000000000";


void setup() {
    Spark.function("update", updateLeds);
    strip.begin();
    strip.show();
    strip.setBrightness(64);
    
    pinMode(redPin, OUTPUT);
    pinMode(greenPin, OUTPUT);
    pinMode(bluePin, OUTPUT);
    
    pinMode(buttonPin, INPUT_PULLDOWN);
    
    analogWrite(redPin, 255);
    analogWrite(greenPin, 255);
    analogWrite(bluePin, 255);
    
    Serial.begin(115200);

}

int updateLeds(String command)
{
    timeElapsed = 0;
    while (timeElapsed < fadeTime)
    {
        for (int led = 0 ; led < numLeds ; led++)
        {
            int state = command.charAt(led);
            int lastState = lastCommand.charAt(led);

            byte redFrom;
            byte redTo;
            byte greenFrom;
            byte greenTo;
            
            if ( state != lastState )
            {
                // from green to red
                if ((lastState == GREEN) && (state == RED))
                {
                    redFrom = 0;
                    redTo = 255;
                    greenFrom = 255;
                    greenTo = 0;
                }
                
                // from red to green
                if ((lastState == RED) && (state == GREEN))
                {
                    redFrom = 255;
                    redTo = 0;
                    greenFrom = 0;
                    greenTo = 255;
                }
                
                // from off to red
                if ((lastState == OFF) && (state == RED))
                {
                    redFrom = 0;
                    redTo = 255;
                    greenFrom = 0;
                    greenTo = 0;
                }
                
                // from off to green
                if ((lastState == OFF) && (state == GREEN))
                {
                    redFrom = 0;
                    redTo = 0;
                    greenFrom = 0;
                    greenTo = 255;
                }
                
                // from green to off
                if ((lastState == GREEN) && (state == OFF))
                {
                    redFrom = 0;
                    redTo = 0;
                    greenFrom = 255;
                    greenTo = 0;
                }
                
                // from red to off
                if ((lastState == RED) && (state == OFF))
                {
                    redFrom = 255;
                    redTo = 0;
                    greenFrom = 0;
                    greenTo = 0;
                }
                
                // before encoder
                if (led < 7)
                    strip.setPixelColor(numLeds - 2 - led, map(timeElapsed, 0, fadeTime, redFrom, redTo), map(timeElapsed, 0, fadeTime, greenFrom, greenTo), 0);
                
                // If led is encoder
                if (led == 7)
                {
                    analogWrite(redPin, map(timeElapsed, 0, fadeTime, 255-redFrom, 255-redTo));
                    analogWrite(greenPin, map(timeElapsed, 0, fadeTime, 255-greenFrom, 255-greenTo));
                    analogWrite(bluePin, 255);
                }

                // after encoder
                if (led > 7)
                    strip.setPixelColor((numLeds - led) - 1, map(timeElapsed, 0, fadeTime, redFrom, redTo), map(timeElapsed, 0, fadeTime, greenFrom, greenTo), 0);
            }
        }
        strip.show();
    }
    lastCommand = command;
    return 1;
}

void set_all_leds(byte r, byte g, byte b)
{
    for (int i = 0 ; i < numLeds ; i++)
    {
        if (i == 14) {
            analogWrite(redPin, abs(r-255));
            analogWrite(greenPin, abs(g-255));
            analogWrite(bluePin, abs(b-255));
        }
        else {
            strip.setPixelColor(i, r, g, b);
        }
    }
    strip.show();
}

void loop() {
    
    if (digitalRead(buttonPin) == HIGH) {
        set_all_leds(0,0,0);
        lastCommand = "000000000000000";
    }
}