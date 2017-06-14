# clAIre
Every car needs a name. The name Claire also contains AI. I thought it worked well.

I will refer to the car as Claire now.

The steps I will take are roughly:

- Connect Raspberry pi up to existing rc car or make diy rc car. This will involve connecting raspberry pi to motor shield then to the DC motors. Use little examplar script to test that it all works.

> Update: I will use both the Raspberry Pi and the Arduino together. I have more experience in using the Arudino with sensors, motors and other add-ons but my C++ skills are a bit rusty hopefully unlike my Python skills that have been in use lately. Also I don't have any network capabilities on more Arduino, and the Arduino doesn't have any USB port unlike the Raspberry Pi that has 6. The network functionality and processing: sending data, receiving and processing data will be done on the Raspberry Pi, whereas the Arduino will be used for data generation and implementation of sensors, motors. Also I want to use my Logitech USB webcam with this project so the USB ports will be handy.

- Add range sensor and the functionality to stop the car before colliding with an object.

>Update: I had a simpler version of this hooked up that turned on an LED when an object was less than 10 cms away from it.

- Add functionality so that it can turn.

- Attach camera to the car and figure out the plumbing needed to be able to use the footage.
> Need to investigate this. This would make it more a project in computer vision than one in AI/Deep Learning.
- TensorFlow and video footage.
- Get the car to follow a path.
- Learn it to stop for a traffic light.

