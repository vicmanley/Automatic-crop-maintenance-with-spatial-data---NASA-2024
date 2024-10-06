# Automatic-crop-maintenance-with-spatial-data---NASA-2024
Development of an automated system that uses NASA satellite data to monitor precipitation, humidity, and vegetation in agricultural areas. With a mobile app, drone control, and a central panel, it enables the management of irrigation, drainage, and seed dispersal, optimizing crops efficiently and accessibly

## THE CHALLENGE
Farmers around the world grapple with a myriad of challenges that threaten their livelihoods and food security. These challenges include unpredictable weather patterns that disrupt planting and harvesting schedules, pest infestations that damage crops, outbreaks of diseases that affect livestock, and even political tensions that impact trade and access to essential resources. These factors collectively contribute to the vulnerability of agricultural communities by impacting crop health, profitability, and overall sustainability.

## Structure
-scr/earthdata
  
  Scripts for fetching, processing, and analyzing satellite data precipitation (for the moment) from EarthData and GES_DISC.

-scr/appmobil
  
  Visualization of the application running locally with the option of a 3D viewer of your location using cardboard.

-scr/appAR

  Visualization of the application with Oculus Quest 3 using augmented reality.

-scr/PanelControl

  Demonstration video of the control panel and irrigation system simulation.

## Prerequisites

Before using this code, make sure you have the following installed:

- Python (recommended version 3.8+)
- Requests
- Geopy
- Matplotlib
- Install a program Miktex for visualer pdf (https://miktex.org/howto/install-miktex)    //Windows
  And with this opcion in install:
  ![Captura de pantalla 2024-10-06 134634](https://github.com/user-attachments/assets/ce3a6ee7-f41a-4134-bdf4-0dd580effbe9)
  
```bash
pip install requests
pip install h5py
pip install numpy
pip install geopy
pip install matplotlib

```

## Getting to start

# Follow these steps to obtain predictions for the desired area:

1.- Import the necessary libraries: At the beginning of the Python script, import the required libraries. This includes Geopy, Matplotlib, and the mentioned modules.

2.- Download the EarthData folder: Inside the folder, you will find the "RyC" file, which can be executed using the command prompt or IDLE. It will ask for your data, such as latitude and longitude (which can be obtained from Google Maps in the specified format).

3.- Wait for your daily results.

Remember to install MikTeX on your computer for everything to function properly.

[![](https://markdown-videos.deta.dev/youtube/NarBox1LkYc)](https://youtu.be/NarBox1LkYc)




