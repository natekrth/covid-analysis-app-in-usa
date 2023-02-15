# USA Covid-19 Analysis App
![Covid Project UML](USA%20Covid-19%20Analysis%20App%20Preview.png)

## Description
What the application does.  Consider including a screen-shot and a link to your demonstration video.

This application is a tool for analysing data and comparing data about Covid-19 in USA by plot data<br>
that you interested in each chart. 

This application allows you to sort the data by 

- **Timeframe** in Day, Month, Year
- **State** in USA
- **Topic** about Covid-19 in USA


You can select which graph you want to plot to compare data.

- **Selected 1** will plot left graph
- **Selected 2** will plot right graph

You can select 3 different plot type in this program.

- **Barh** plot
- **Line** plot
- **Histrogram** plot

## Instruction
### How to plot?
1. Select Graph, Timeframe, State, Topic, Plot type
2. Press Plot Button

### How to sort data by state and show?
1. Select state you interested
2. Press Sort by state button

### How to clear after plot?
1. Select Graph you want to clear
2. Press Clear button.

## Running the Application
Any dependencies (packages) needed to run your program. How to run it.

In this application you need 
1. ```tkinter```
2. ```pandas```
3. ```matplotlib```
4. ```pip install tkintermapview```
5. ```pip install customtkinter```
6. ```pip install pyperclip```
7. ```pillow```

TkinterMapView Source:  https://github.com/TomSchimansky/TkinterMapView
### Running the Application by run ```application.py```


## Design
Describe the overall design, including a UML class diagram.

#### User Interface design
In this project, I use many different widget from tkinter.

1. ```Treeview and Scrollbar```<br> for displaying items from data.
2.```TkinterMapView``` <br> which is a tile based interactive map renderer widget for the python Tkinter library.
   TkiterMapView will display USA state that we are interested.
3. ```Label``` <br> for labeling.
4. ```Button``` <br> for clicking and let run tasks or take action.
5. ```Frame and Label Frame``` <br> create a frame for widgets.
6. ```Radiobutton``` <br> for selecting which graph user wants to plot.
7. ```Combobox``` <br> select for sorting data.
8. ```Progressbar``` <br> add to be responsive and show progress of the program.
9. ```Customtkinter Frame``` <br> create a frame for TkinterMapView.

#### Class Design
![Covid Project UML](Covid%20Project%20UML.jpg)


## Design Patterns Used
Describe any design patterns you used, and how they are used in your application.

### 1. Model-View-Controller (MVC) Pattern<br/>
- **Model** in this program will do a scientific computing and sorting data using pandas then sent result back to controller. 
- **View** is the user interface that representing the data in the model by communicate via controller and controller to model. Mainly, I use for plotting the graph.
- **Controller** is a medium between View and Model which after user action to plot view will can sent data to controller and also receive result data from controller.

### 2.State Pattern
I use State Pattern which split into 2 state 
1. ```ProcessingState``` is a state use to notify the user that program is still processing (start the progressbar)
2. ```StandbyState``` is a state use to notify the user that program is standby and ready to process the task.
   (stop the progressbar, set status, set active button)

 
## Other Information
Anything else you would like to include.  Anything you think is important or interesting that you learned.  For example, any interesting libraries or packages you use in your application.

This project is such a good practice of scientific computing using (pandas, matplotlib) combining with
User interface (tkinter) and other. These two combination create powerful/useful program.

In this project, I have learned a lot about tkinter basic and about how to handle with the event loop.
I think the hardest part is about way to use design pattern and also the progressbar which I have learned about Thread.

The most impressive library is the tkintermapview because I can use the data from my dataset to search the state on the map.
