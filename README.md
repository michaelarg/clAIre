# clAIre
Every car needs a name. The name Claire also contains AI. I thought it worked well.

![170301163620-roborace-barcelonas-media-daniel-simon-02-large-super-169](https://user-images.githubusercontent.com/15652565/27119802-9e932a5e-5124-11e7-87b4-cb7915b15468.jpg)

Like this car pictured but much smaller and much prettier. Probably less intelligent too. Slightly slower as well I'm guessing.

I will refer to the car as Claire now.

The steps I will take are roughly:

- Connect Raspberry pi up to existing rc car or make diy rc car. (I ended up purchasing a $15 car from Kmart).
This will involve connecting raspberry pi to motor shield then to the DC motors. Use little examplar script to test that it all works.

> Update: I will use both the Raspberry Pi and the Arduino together. I have more experience in using the Arudino with sensors, motors and other add-ons but my C++ skills are a bit rusty hopefully unlike my Python skills that have been in use lately. Also I don't have any network capabilities on more Arduino, and the Arduino doesn't have any USB port unlike the Raspberry Pi that has 6. The network functionality and processing: sending data, receiving and processing data will be done on the Raspberry Pi, whereas the Arduino will be used for data generation and implementation of sensors, motors. Also I want to use my Logitech USB webcam with this project so the USB ports will be handy. Also I get to use C++ and Python in this project.

- Add range sensor and the functionality to stop the car before colliding with an object.

>Update: I had a simpler version of this hooked up that turned on an LED when an object was less than 10 cms away from it.



- Add functionality so that it can turn.

>There is a dc motor in the car that already gives it turning functionality. All that needs to be done here is to hook this up to the LN298 motor shield and code it correctly. It is actually really beautiful to see this work. There is a cog connected to the dc motor which is in a horizontal position, spinning clockwise and anti clockwise that is connected to a horizontal cog which is then further connected to the steering road.

- Attach camera to the car and figure out the plumbing needed to be able to use the footage.
> Need to investigate this. This would make it more a project in computer vision than one in AI/Deep Learning.
- TensorFlow and video footage.
- Get the car to follow a path.
- Learn it to stop for a traffic light.
- Adapt accelerometer to measure G Force of collision. Ultimately understand the accelerometer and G Force better.

### Update 8/8/17: ClAIre may need a bigger body!

### Update 6/9/17: Finding new flatmate, work, GOT and Rick and Morty have taken over my nights and I've been a bit slack with ClAIre. Did buy a bigger body so all the components should fit on now. Experimenting with webcams and raspberry pi. Found the video really slow and currently researching ways around this bottleneck before I can get stuck into some cool computer vision.
