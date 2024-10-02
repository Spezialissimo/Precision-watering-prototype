# Prototype of an automatic irrigation system
I've made this project for my bachelor's degree thesis. It is a small scale rendition of an automated irrigation system, with a frontend for monitoring the moisure values in real time and set the irrigation rules.

This fork contains a simple demo that is not actually connected to any real hardware system. The actual project, that does need hardware components to work, can be found (here)[https://github.com/ManuelePasini/small_watering]
You can visit the demo live (here)[https://precision-watering-prototype.onrender.com].

Precision irrigation is a branch of precision agriculture that focuses on optimizing water usage. In this demo, we simulate a physical system, featuring six sensors and two sprinklers. The six sensors are positioned in pairs, spaced 20 cm apart horizontally and 10 cm apart vertically. The first pair is located at a depth of 5 cm, with the two elements of the pair placed 10 cm from the edges of the testbed. As a result, the sensors are labeled as follows:
+ Sensor (10, 5)
+ Sensor (10, 15)
+ Sensor (10, 25)
+ Sensor (30, 5)
+ Sensor (30, 15)
+ Sensor (30, 25)

The two sprinklers are referred to as the "right sprinkler" and the "left sprinkler." In the original system, a valve controls the left sprinkler; in this context, it is replaced by a button labeled "Toggle left sprinklers."

You can decide the basis for future irrigation calculations:
+ Slider: The system will try to maintain an average moisture level based on the value set by the slider.
+ Matrix: The system will attempt to match the moisture matrix displayed in the Moisture matrix section as closely as possible.

By closing the left sprinklers, we can test how using the correct moisture matrix allows for proper irrigation. This can be visualized as simulating a scenario where the soil on the left absorbs less water than the right side. If the system attempts to maintain an excessively high average moisture level using the slider, it might never reach that level, leaving the pump running indefinitely. The same issue occurs if a completely saturated matrix is selected. 

