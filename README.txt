Inspiration

When children get sick, parents will often call out of work to take care of them. However, for pet owners, it is often difficult to justify the significant financial cost of staying home from work or hiring assistance. Nevertheless, many consider their pets to be members of the family and worry about leaving them alone, for health emergencies can quickly become serious and life-threatening. To solve this problem we propose petMD: a convenient and cost-effective way to monitor and watch over pets who are sick or injured without disrupting the daily lives of their owners.

What it does

petMD has two components: an autonomous pet-seeking video rover and a vital-sign monitor, both of which are accessible remotely through a web application. Using the rover, pet owners can visually check in on their pets no matter where in the house they might be, offering an advantage over stationary cameras which offer limited perspectives. With the vital-sign monitor they can keep track of the pet's heartbeat, temperature, and humidity. The monitor will notify owners if vital signs enter dangerous territory, allowing them to catch emergencies before it's too late. Together, these two components provide pet owners with peace of mind and a better picture of the health of their pets.

How we built it

We thought of several configurations and arrangements, but ultimately settled upon a Raspberry Pi powered-rover with an ESP32 controlled vital-monitor. Both microcontrollers are capable of wireless communication which we would use to send data to the web application, and the Rasp Pi is capable of using a camera accessory, providing support for the live-stream, a key feature of our platform. On the software side, we set up a local server on a laptop with a web socket connection to the rover and the vital-monitor. Upon receiving data, the server would then send that data through another WebSocket connection to an Astro app that we built, which would then process the data and create the video stream as well as the vitals dashboard.

Challenges we ran into

One of the biggest challenges was configuring the Raspberry Pi, specifically doing so in headless mode and with the camera module. We didn't have the right cables/adapters to connect a display to the Rasp Pi, so we had to configure it without any visual indication. Additionally, legacy support for older camera libraries was recently revoked, which made a lot of online resources and tutorials obsolete.

Accomplishments that we're proud of

We are particularly proud of the video stream, which is a respectable 30 fps and which has a very reasonable resolution, given how small the camera is. Additionally, controlling the rover with a Raspberry Pi was something that nobody on the team had experience with, but we are proud not only of the rover's ability to navigate, but to do so autonomously, blending information from the video feed with machine learning image recognition models to generate motor instructions.

What we learned

One common sentiment expressed throughout the entire process was that "nothing comes easy. " Even aspects that we had planned out meticulously and thought would be straightforward ended up having hiccups or hurdles that took a lot of debugging and problem-solving. The Raspberry Pi is a great example: we anticipated difficulty in implementing web streaming or video quality, but one of our largest roadblocks was actually just connecting to it! As such we had to pare down our expectations and goals for the project, but the result was a better understanding of what our core features should be, a stronger identity as to what problems we could solve.

What's next for petMD

Although we do believe petMD can today be useful to pet owners, there are a handful of clear directions for improvement. Among the most significant are: support for a mobile app, the ability to train an image recognition model on the actual pet, or a GPS or UWB module that can help the rover locate pets when they are not in line of sight.


