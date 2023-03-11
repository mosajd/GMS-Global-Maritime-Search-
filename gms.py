
####################################################################################################################################################################################################

##################################################################### THIS SOFTWARE IS CREATED BY SAYED MOHAMMAD SAJJADI, MOSAJD@GMAIL.COM #########################################################

##################################################################################### https://github.com/mosajd ####################################################################################

#################################################################################################################################################################################################
########################################################################################## Libraries ############################################################################################
#################################################################################################################################################################################################
import tkinter as tk
from tkinter import ttk
from tkinter.constants import ACTIVE, DISABLED, END
from tkinter import *
from tkinter.font import BOLD
from tkinter.tix import *
from tkhtmlview import HTMLLabel 
from tkhtmlview import HTMLScrolledText
from tkhtmlview import HTMLText
import Pmw
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure as FigureMat
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)
from PIL import ImageTk, Image 

# Folium Maps
#from datetime import datetime, timedelta
from matplotlib import pyplot as plt
import folium
from branca.element import Figure
from folium import plugins
from folium.plugins import TimestampedGeoJson
import webbrowser

#################################################################################################################################################################################################
########################################################################################## Tkinter Frame ########################################################################################
#################################################################################################################################################################################################
sns.set_style('whitegrid')

root = tk.Tk()

# tkinter title
root.title('GMS (Global Maritime Search) v.1.0')

# tkinter background color
root.configure(bg='#3232ff')
#root.attributes('-alpha', 0.95)

# windows only (remove the minimize/maximize button)
#root.attributes('-toolwindow', True)

# tkinter size
root.resizable(False, False) 
window_width = 800
window_height = 790

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point
center_x = int(screen_width/2 - window_width / 2)
center_y = int(screen_height/2 - window_height / 2)

# set the position of the window to the center of the screen
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

#Make the window jump above all
#root.attributes('-topmost',1)

# tkniter icon
#root.iconbitmap('uni.ico')

# create a notebook
notebook = ttk.Notebook(root)
notebook.place(x=0, y=0)

# Create Tabs
tab_introduction = ttk.Frame(notebook)
tab_help = ttk.Frame(notebook)
tab_routes = ttk.Frame(notebook)
tab_vessel = ttk.Frame(notebook)
tab_cargo = ttk.Frame(notebook)
tab_time = ttk.Frame(notebook)
tab_fuel = ttk.Frame(notebook)
tab_environment = ttk.Frame(notebook)
tab_cost = ttk.Frame(notebook)
tab_risk = ttk.Frame(notebook)
tab_references = ttk.Frame(notebook)
tab_developers = ttk.Frame(notebook)
#tab_test = ttk.Frame(notebook)

# Add Tabs
notebook.add(tab_introduction, text='Introduction')
notebook.add(tab_help, text='Help')
notebook.add(tab_routes, text ='Routes')
notebook.add(tab_vessel, text ='Vessel')
notebook.add(tab_cargo, text ='Cargo')
notebook.add(tab_time, text ='Time')
notebook.add(tab_fuel, text ='Fuel')
notebook.add(tab_environment, text='Environment')
notebook.add(tab_cost, text ='Cost')
notebook.add(tab_risk, text='Stochastic')
notebook.add(tab_references, text='References')
notebook.add(tab_developers, text='Team')
#notebook.add(tab_test, text='Test')

#################################################################################################################################################################################################
########################################################################################## Functions ############################################################################################
#################################################################################################################################################################################################

#################################################################################### callbackTime Function #######################################################################################
def callbackTime(*args):
    # required fuel for this voyage
    required_fuel_var = fuel_consumption.get() * shipping_time.get()   # gallon / day * day = gallon
    required_fuel.set(round(required_fuel_var,3))

    # required number of times for refuling inside bunkering ports
    refueling_times_var = required_fuel_var/(fuel_tank_capacity.get() * 1000000)
    refueling_times.set(int(refueling_times_var))

    # spending time in bunkering ports for refuling
    refueling_time_delay_var = int(refueling_times_var) * bunkering.get()  # hours
    refueling_time_delay.set(refueling_time_delay_var)

    # totla time for both shipping and unshipping
    value = ((refueling_time_delay_var + bureaucracy.get() + dwell.get()) / 24) + shipping_time.get()  # days
    total_voyage_time.set(round(value, 3))

def callbackCost(*args):
    # cargo insurance cost
    cargo_insurance_cost_var = round(cargo_insurance_coefficient.get() * 0.01 * cargo_value.get(), 3)
    cargo_insurance_cost.set(cargo_insurance_cost_var)   # Million USD
    
    # repair and services cost annual
    repair_service_cost_var = round(coefficient_repair_service.get() * 0.01 * capital_cost.get(), 3)
    repair_service_cost.set(repair_service_cost_var)    # million USD

    # repair and services cost voyage
    repair_service_vayage_var = (repair_service_cost.get() * total_voyage_time.get() / 365) * 1000000
    repair_service_vayage.set(int(repair_service_vayage_var))   # USD

    # annual capital and depreciation cost of vessel
    annual_capital_cost_var = round(coefficient_capital_cost.get() * 0.01 * capital_cost.get(),3)
    annual_capital_cost.set(annual_capital_cost_var)   # Million USD

    # voyage capital cost and depreciation of vessel
    voyage_capital_cost_var = (annual_capital_cost_var * total_voyage_time.get() / 365) * 1000000
    voyage_capital_cost.set(int(voyage_capital_cost_var))    # USD

    # annual insurance cost of vessel structure
    annual_insurance_cost_var = round(coefficient_insurance.get() * 0.01 * capital_cost.get(),3)
    annual_insurance_cost.set(annual_insurance_cost_var)   # Million USD

    # voyage insurance cost of vessel structure
    voyage_insurance_cost_var = (annual_insurance_cost_var * total_voyage_time.get() / 365) * 1000000
    voyage_insurance_cost.set(int(voyage_insurance_cost_var))   # USD

    # piracy insurance cost for this voyage
    piracy_insurance_cost_var = int(parameter_insurance.get() * piracy_coefficient.get() * total_voyage_time.get() / 365)
    piracy_insurance_cost.set(piracy_insurance_cost_var)     # USD

    # salary in this voyage
    salary_voyage_var = int((salary_month.get() / 30) * total_voyage_time.get())
    salary_voyage.set(salary_voyage_var)   # USD

    # Port dues
    port_dues_var = coefficient_port_dues.get() * gross.get() * 2
    port_dues.set(port_dues_var)  # USD

    # Environmental Cost
    total_environmental_cost_var = air_pollution_cost.get() + global_warming_cost.get()
    total_environmental_cost.set(int(total_environmental_cost_var))   # USD

    # Total Cost
    total_cost_var = ((cargo_insurance_cost_var * 1000000) + salary_voyage_var + piracy_insurance_cost_var + repair_service_vayage_var + voyage_capital_cost_var + voyage_insurance_cost_var 
    + port_dues_var + total_environmental_cost_var + total_fuel_consumption_cost.get()) / 1000000
    total_cost.set(round(total_cost_var, 6))

#################################################################################################################################################################################################
########################################################################################## Introduction Tab #####################################################################################
#################################################################################################################################################################################################
# Photo strategos
strategos = Image.open("strategos.png")
strategos_resized = strategos.resize((175, 175), Image.ANTIALIAS)
strategos_show = ImageTk.PhotoImage(strategos_resized)
strategos_label = ttk.Label(tab_introduction, image=strategos_show)
strategos_label.place(relx=0.4, rely=0.01)

# Photo shipping route
shipping_routes = Image.open("routes.png")
shipping_routes_resized = shipping_routes.resize((250, 250), Image.ANTIALIAS)
shipping_routes_show = ImageTk.PhotoImage(shipping_routes_resized)
shipping_routes_label = ttk.Label(tab_introduction, image=shipping_routes_show)
shipping_routes_label.place(relx=0.05, rely=0.2)

quote_text = "<p style='margin: 100px 50px 100px 145px;'><strong><i>«If a man does not know to what port he is<br> steering, no wind is favourable to him»<br></i></strong><br>\
(Lucius Annaeus Seneca, 5 BC - 65 AD)</p>"
quote_label = HTMLLabel(tab_introduction, html=quote_text)
quote_label.place(relx=0.46, rely=0.33)

description_text = "<div style='text-align: left'><h5>Economic Feasibility of Maritime Routes for the Future</h5>\
<p style=font-size:85%; text-align:justify;>According to phenomena of global warming, icebergs in the north pole are expected to melt in a few years. Regardless \
of likely environmental consequences, the maritime Arctic Ocean route would become available for vessel ships to sail across without utilizing specific equipment such as ice breakers.</p><br>\
<p style=font-size:85%;>Therefore, analyzing and comparing Northeast Passage with other routes can be considered an interesting opportunity for many businesses particularly for freight companies.</p>\
<p style=font-size:85%;><a href='https://github.com/mosajd/GMS-Global-Maritime-Search-' style='color:red;'>GMS (Global Maritime Search)</a> software which is the result of one of the teamwork projects for\
<a href='http://www.simulationteam.com/strategos/edu/complexsystems/'>Modelling and Design of Complex Systems</a>\
course from the master program of <a href='http://strategos.it/'>Engineering Technology for Strategy and Security - Strategos</a> at the <a href='https://unige.it/en'>University of Genoa</a> is \
designed as a tool to model this scenario.</p>\
<p style=font-size:85%;>\
Our model currently evaluating, analyzing, and comparing two routes: the <b>Suez Canal Route (SCR)</b> and <b>Northern Sea Route (NSR)</b>, considering that NSR is free of icebergs and is accessible at \
most times of the year.<br>\
</p></div>"
description_label = HTMLLabel(tab_introduction, html=description_text)
description_label.place(x=15,rely=0.55, relwidth=0.95)
#################################################################################################################################################################################################
########################################################################################## Help Tab #####################################################################################
#################################################################################################################################################################################################

description_help = "<h5>Methodology</h5>\
<p style='font-size:75%;'>This model calculates both <b>time</b> and <b>cost</b> for each desired voyage in both <strong>deterministic</strong> and <b>stochastic (probabilistic)</b> simulations.</p>\
<h6>Input parameters for deterministic model:</h6>\
<ul style='font-size:75%;'>\
    <li>Distance (between two ports)</li>\
    <li>Average shipping speed</li>\
    <li>Vessel type (TEU, load capacity, dimensions, tank capacity, year of construction, crew, engine power, fuel consumption, price, ...)</li>\
    <li>Vessel costs (services & maintenance, annual capital cost and depreciation, insurances, and crew salary)</li>\
    <li>Cargo (type, value, weight, and insurance cost)</li>\
    <li>Time (bureaucracy and administrative issues, the dwell time in ports, the average delay for bunkering)</li>\
    <li>Fuel (type and price for each route)</li>\
    <li>Environmental cost (cost of air pollution and cost of global warming)</li>\
</ul>\
<h6>Input parameters for stochastic model:</h6>\
<ul style=font-size:75%;>\
    <li>Fuel price (mean and standard deviation price for each route based on the normal distribution)</li>\
    <li>Weather conditions could affect shipping time and delay. For this parameter mean and standard deviation in terms of days are defined based on the normal distribution.</li>\
    <li>Wind and currents could affect shipping speed. For this parameter mean and standard deviation in terms of shipping speed are defined based on the normal distribution.</li>\
</ul>\
<p style=font-size:75%;>All stochastic parameters in this model are created according to the <b>Monte Carlo method</b> and then applied to outputs.<br>\
In this software, you select the input parameters step by step according to the guide numbering, and then the system suggests the next values based on the available references. \
You can also change the values in each section to be applied to the result.</p>\
<div><img src='cost.jpg' alt='Girl in a jacket' style='width:800px;height:600px;'></div>\
<div><img src='time.jpg' alt='Girl in a jacket' style='width:800px;height:600px;'></div>\
<h5>Notes</h5>\
<ul style=font-size:75%;>\
    <li>In some parts, where the asterisk sign * is observed, placing the mouse cursor over it displays the description for that part.</li>\
    <li>By default, when entering the Inputs mode you can see the corresponding values of the last prespecified data that you selected. This way you can modify some properties of the last scenario \
        (f.e. distance or average shipping speed) and perform a simple sensitivity analysis.</li>\
    <li>When entering data please DO NOT use the thousands separator ',' .</li>\
</ul>\
<h5>Disclaimer</h5>\
<p style=font-size:75%;>Naturally, this model has been created with a subjective knowledge and specific experiences and may be subject to corrections and implementations, but it still intends to offer an exhaustive\
 framework and a useful and concrete answer for the identified scenario.</p>"

description_help_label = HTMLScrolledText(tab_help, html=description_help)
description_help_label.place(x=10, y=10, relwidth=0.98, relheight=0.98)

#################################################################################################################################################################################################
########################################################################################## Routes Tab ###########################################################################################
#################################################################################################################################################################################################

########################################################################################## Year & Month #################################################################################################
# # # create label frame
# lf_year = ttk.LabelFrame(tab_routes, text="Year & Month", relief='sunken')
# lf_year.grid(column=1, row=0, padx=10, pady=10, sticky=tk.EW)

# # # Label Desription
# ttk.Label(lf_year, text="1- Define year and month of the shipping time.", foreground='red').grid(column=0,row=0, pady=8)

# # # label year
# year_label = ttk.Label(lf_year, text="Year:")
# year_label.grid(column=0, row=1, sticky=tk.NSEW)
# # # create a combobox year
# year = tk.StringVar()
# year_combo = ttk.Combobox(lf_year, textvariable=year)
# year_combo.grid(column=0, row=2, sticky=tk.W, padx=8, pady=8)
# year_combo['values'] = [i for i in range(2030, 2051)]

# # # label month
# month_label = ttk.Label(lf_year, text="Month:")
# month_label.grid(column=1, row=1, sticky=tk.NSEW)
# # # create a combobox month
# month = tk.StringVar()
# month_combo = ttk.Combobox(lf_year, textvariable=month)
# month_combo.grid(column=1, row=2, sticky=tk.W, padx=8, pady=8)
# month_combo['values'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
##########################################################################################  Ports ##########################################################################################
# create label frame
lf_ports = ttk.LabelFrame(tab_routes, text="Ports", relief='sunken')
lf_ports.grid(column=1,row=1, padx=10, pady=10)

# Label Desription
ttk.Label(lf_ports, text="1- Define both port of departure and arrival.", foreground='red').grid(column=0,row=0)
########################################################################################## Origin Ports ##########################################################################################
# create label frame
lf_origin_ports = ttk.LabelFrame(lf_ports, text="Port of Departure", relief='raised')
lf_origin_ports.grid(column=0,row=1, padx=10, pady=10, sticky=tk.W, ipadx=10)

selected_origin_ports = tk.StringVar()
origin_port_1 = ttk.Radiobutton(lf_origin_ports, text="Mumbai (INBOM)", value=0, variable=selected_origin_ports)
origin_port_2 = ttk.Radiobutton(lf_origin_ports, text="Singapore (SGSIN)", value=1, variable=selected_origin_ports)
origin_port_3 = ttk.Radiobutton(lf_origin_ports, text="Shanghai (CNSGH)", value=2, variable=selected_origin_ports)
origin_port_4 = ttk.Radiobutton(lf_origin_ports, text="Yokohama (JPYOK)", value=3, variable=selected_origin_ports)
origin_port_5 = ttk.Radiobutton(lf_origin_ports, text="Murmansk (RUMMK)", value=4, variable=selected_origin_ports)
origin_port_6 = ttk.Radiobutton(lf_origin_ports, text="Rotterdam (NLRTM)", value=5, variable=selected_origin_ports)
origin_port_7 = ttk.Radiobutton(lf_origin_ports, text="Genoa (ITGOA)", value=6, variable=selected_origin_ports)
origin_port_8 = ttk.Radiobutton(lf_origin_ports, text="Malta Freeport", value=7, variable=selected_origin_ports)

origin_port_1.grid(column=0, row=0, sticky=tk.W)
origin_port_2.grid(column=0, row=1, sticky=tk.W)
origin_port_3.grid(column=0, row=2, sticky=tk.W)
origin_port_4.grid(column=0, row=3, sticky=tk.W)
origin_port_5.grid(column=0, row=4, sticky=tk.W)
origin_port_6.grid(column=0, row=5, sticky=tk.W)
origin_port_7.grid(column=0, row=6, sticky=tk.W)
origin_port_8.grid(column=0, row=7, sticky=tk.W)

########################################################################################## Destination Ports ##########################################################################################
# create label frame
lf_destination_ports = ttk.LabelFrame(lf_ports, text="Port of Arrival", relief='raised')
lf_destination_ports.grid(column=1,row=1, padx=10, pady=10, sticky=tk.E, ipadx=10)

selected_destination_ports = tk.StringVar()
destination_port_1 = ttk.Radiobutton(lf_destination_ports, text="Mumbai (INBOM)", value=0, variable=selected_destination_ports)
destination_port_2 = ttk.Radiobutton(lf_destination_ports, text="Singapore (SGSIN)", value=1, variable=selected_destination_ports)
destination_port_3 = ttk.Radiobutton(lf_destination_ports, text="Shanghai (CNSGH)", value=2, variable=selected_destination_ports)
destination_port_4 = ttk.Radiobutton(lf_destination_ports, text="Yokohama (JPYOK)", value=3, variable=selected_destination_ports)
destination_port_5 = ttk.Radiobutton(lf_destination_ports, text="Murmansk (RUMMK)", value=4, variable=selected_destination_ports)
destination_port_6 = ttk.Radiobutton(lf_destination_ports, text="Rotterdam (NLRTM)", value=5, variable=selected_destination_ports)
destination_port_7 = ttk.Radiobutton(lf_destination_ports, text="Genoa (ITGOA)", value=6, variable=selected_destination_ports)
destination_port_8 = ttk.Radiobutton(lf_destination_ports, text="Malta Freeport", value=7, variable=selected_destination_ports)

destination_port_1.grid(column=0, row=0, sticky=tk.W, ipadx=10, ipady=1)
destination_port_2.grid(column=0, row=1, sticky=tk.W, ipadx=10, ipady=1)
destination_port_3.grid(column=0, row=2, sticky=tk.W)
destination_port_4.grid(column=0, row=3, sticky=tk.W)
destination_port_5.grid(column=0, row=4, sticky=tk.W)
destination_port_6.grid(column=0, row=5, sticky=tk.W)
destination_port_7.grid(column=0, row=6, sticky=tk.W)
destination_port_8.grid(column=0, row=7, sticky=tk.W)

########################################################################################## Routes ##########################################################################################
# create label frame
lf_routes = ttk.LabelFrame(tab_routes, text="Routes")
lf_routes.grid(column=2, row=1, padx=10, pady=10)

# Label Desription
ttk.Label(lf_routes, text="2- Define the route.", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=8)

selected_routes = tk.StringVar()
r1 = ttk.Radiobutton(lf_routes, text='NSR (Northern Sea Route)', value='NSR', variable=selected_routes, command=lambda: selectedRoute(selected_origin_ports.get(), selected_destination_ports.get(), route='NSR'))
r2 = ttk.Radiobutton(lf_routes, text='SCR (Suez Canal Route)', value='SCR', variable=selected_routes, command=lambda: selectedRoute(selected_origin_ports.get(), selected_destination_ports.get(), route='SCR'))

r1.grid(column=0,row=1, sticky=tk.NSEW, ipadx=10, ipady=10, padx=10, pady=10)
r2.grid(column=0,row=2, sticky=tk.NSEW, ipadx=10, ipady=10, padx=10, pady=10)

################################################################################################### Distance ##########################################################################################
# create label frame
lf_distance = ttk.LabelFrame(tab_routes, text="Distance")
lf_distance.grid(column=1,row=2, padx=5, pady=10, ipadx=5, ipady=5, columnspan=2)
lf_distance.columnconfigure(0,weight=1)
lf_distance.columnconfigure(1,weight=1)
lf_distance.columnconfigure(2,weight=1)
lf_distance.columnconfigure(3,weight=1)

# Label Desription
ttk.Label(lf_distance, text="3- The maritime distance between the ports is found through the 'aquaplot.com'. You can modify this distance.", foreground='red').grid(column=0,row=0, sticky=tk.W, columnspan=4, pady=8)

distances_array_nsr = np.array([
[0, 2453, 4683, 5337, 10786, 13095, 14528, 14671],
[2453, 0, 2238, 2893, 8341, 10324, 12111, 12254],
[4683, 2238, 0, 1073, 6316, 8299, 9721, 9864],
[5337, 2893, 1073, 0, 5553, 7537, 8959, 9101],
[10786, 8341, 6316, 5553, 0, 2310, 3733, 3875],
[13095, 10324, 8299, 7537, 2310, 0, 2248, 2391],
[14528, 12111, 9721, 8959, 3733, 2248, 0, 609],
[14671, 12254, 9864, 9101, 3875, 2391, 609, 0]])

distances_array_scr = np.array([
[0, 2453, 4640, 5337, 7835, 6319, 4484, 3978],
[2453, 0, 2195, 2893, 9833, 8318, 6482, 5985],
[4640, 2195, 0, 1069, 12020, 10505, 8670, 8173],
[5337, 2893, 1069, 0, 12717, 11202, 9367, 8870],
[7835, 9833, 12020, 12717, 0, 1602, 3730, 3873],
[6319, 8318, 10505, 11202, 1602, 0, 2215, 2358],
[4484, 6482, 8670, 9367, 3730, 2215, 0, 609],
[3987, 5985, 8173, 8870, 3873, 2358, 609, 0]   
])

# Distance nm
real_distance_nm = tk.IntVar()
real_distance_nm_label = ttk.Label(lf_distance, text="Distance (nm) * :")
real_distance_nm_label.grid(column=0, row=1, padx=5, sticky=tk.W)
real_distance_nm_entry = ttk.Entry(lf_distance, textvariable=real_distance_nm)
real_distance_nm_entry.grid(column=1, row=1,padx=5, sticky=tk.W)

# Balloon nm
balloon_nm = Pmw.Balloon(lf_distance)
balloon_nm.bind(real_distance_nm_label,'Nautical Miles are used to measure the distance traveled through the water. \nA nautical mile is slightly longer than a mile on land, equaling 1.1508 land-measured (or statute) miles.')

# Distance Km
real_distance_km = tk.IntVar()
real_distance_km_label = ttk.Label(lf_distance, text="Distance (Km):")
real_distance_km_label.grid(column=2, row=1, padx=5, sticky=tk.E)
real_distance_km_entry = ttk.Entry(lf_distance, textvariable=real_distance_km)
real_distance_km_entry.grid(column=3, row=1, padx=5, sticky=tk.E)

################################################################################################### Speed ##########################################################################################
# create label frame
lf_speed = ttk.LabelFrame(tab_routes, text="Speed")
lf_speed.grid(column=1,row=3, padx=5, pady=10, ipady=5, columnspan=2)
lf_speed.columnconfigure(0,weight=1)
lf_speed.columnconfigure(1,weight=1)
lf_speed.columnconfigure(2,weight=1)
lf_speed.columnconfigure(3,weight=1)

# Label Desription
ttk.Label(lf_speed, text="4- You can change the average shipping speed or use the recommended by the system.", foreground='red').grid(column=0,row=0, sticky=tk.W, columnspan=2, pady=10)

# Average Speed knots
average_speed_knots = tk.DoubleVar()
average_speed_knots_label = ttk.Label(lf_speed, text='Average Shipping Speed (knots) * :')
average_speed_knots_label.grid(column=0, row=1, padx=5,sticky=tk.W)
average_speed_knots_entry = ttk.Spinbox(lf_speed,from_=1,to=50 ,textvariable=average_speed_knots, command=lambda: shippingSpeed(average_speed_knots.get()))
average_speed_knots_entry.grid(column=1, row=1, padx=2,sticky=tk.W)

# Balloon knots
balloon_knots = Pmw.Balloon(lf_speed)
balloon_knots.bind(average_speed_knots_label,'The knot (/nɒt/) is a unit of speed equal to one nautical mile per hour, exactly 1.852 km/h (approximately 1.151 mph or 0.514 m/s).')

# Average Speed kph
average_speed_kph = tk.DoubleVar()
average_speed_kph_label = ttk.Label(lf_speed, text='Average Shipping Speed (km/h):')
average_speed_kph_label.grid(column=2, row=1, padx=2,sticky=tk.W)
average_speed_kph_entry = ttk.Entry(lf_speed, textvariable=average_speed_kph)
average_speed_kph_entry.grid(column=3, row=1, padx=5,sticky=tk.W)

################################################################################################### Shipping Time ##########################################################################################
# create label frame
lf_shipping_time = ttk.LabelFrame(tab_routes, text="Shipping Time")
lf_shipping_time.grid(column=1,row=4, padx=10, pady=10, ipadx=5, ipady=5, columnspan=2)

# Label Desription
ttk.Label(lf_shipping_time, text="Total shipping time is calculated:", foreground='blue').grid(column=0,row=0, sticky=tk.W, pady=8)

# Label Shipping Time
shipping_time_label = ttk.Label(lf_shipping_time, text='Shipping Time (days):')
shipping_time_label.grid(column=0, row=1, sticky=tk.W)
# Entry Shipping Time
shipping_time = tk.DoubleVar()
shipping_time_entry = ttk.Entry(lf_shipping_time, textvariable=shipping_time)
shipping_time_entry.grid(column=1, row=1, sticky=tk.W)

### trace
#shipping_time.trace('w', callbackTime)

def shippingSpeed(arg):
    # Convert knots to kph
    average_speed_kph_entry.config(state=ACTIVE)
    average_speed_kph_entry.delete(0, END)
    average_speed_kph_entry.insert(0, round(arg * 1.852, 3))
    average_speed_kph_entry.config(state=DISABLED)
    # calculate shipping time to days
    shipping_time_entry.config(state=ACTIVE)
    shipping_time_entry.delete(0, END)
    shipping_time_entry.insert(0, round(real_distance_nm.get() / arg / 24, 3))   # hours
    shipping_time_entry.config(state=DISABLED)

######################################################################################### Button Show on Map ##########################################################################################

folium_map_button = ttk.Button(tab_routes, text="Show On the Map", command=lambda: mapRoute('ports.xlsx', int(selected_origin_ports.get()), int(selected_destination_ports.get()), selected_routes.get(), real_distance_nm.get()))
folium_map_button.grid(column=1, row=5, pady=20, ipadx=7, ipady=7, columnspan=2)


#################################################################################################################################################################################################
########################################################################################## Folium Map ###########################################################################################
#################################################################################################################################################################################################


########################################################################################## Folium Functions ##########################################################################################


def mapRoute(xlsx_file, origin, destination, route, distance):
############################################ show map types using layer control ###################################################
    # map
    m=folium.Map(location=[53,86], zoom_start=3)

    # add tiles to map
    folium.raster_layers.TileLayer('CartoDB Dark_Matter').add_to(m)
    folium.raster_layers.TileLayer('Open Street Map').add_to(m)
    folium.raster_layers.TileLayer('Stamen Terrain').add_to(m)
    folium.raster_layers.TileLayer('Stamen Toner').add_to(m)
    folium.raster_layers.TileLayer('Stamen Watercolor').add_to(m)
    folium.raster_layers.TileLayer('CartoDB Positron').add_to(m)

    # add layer control to show different maps
    folium.LayerControl().add_to(m)

    #lat/lon popovers by click on the map
    m.add_child(folium.LatLngPopup())

############################################# Measure Control ###########################################
    measure_control = plugins.MeasureControl(position='topleft', active_color='red', completed_color='red', primary_length_unit='meters')

    # add measure control to map
    m.add_child(measure_control)
############################################ Routes Coordinates ##########################################
    nsr_routes = np.array([
    ['Mumbai', 'Mumbai_Singapore', 'Mumbai_Shanghai', 'Mumbai_Yokohama', 'Mumbai_Murmansk_nsr', 'Mumbai_Rotterdam_nsr', 'Mumbai_Genova_nsr', 'Mumbai_Malta_nsr'],
    ['Singapore_Mumbai', 'Singapore', 'Singapore_Shanghai', 'Singapore_Yokohama', 'Singapore_Murmansk_nsr', 'Singapore_Rotterdam_nsr', 'Singapore_Genova_nsr', 'Singapore_Malta_nsr'],
    ['Shanghai_Mumbai', 'Shanghai_Singapore', 'Shanghai', 'Shanghai_Yokohama', 'Shanghai_Murmansk_nsr', 'Shanghai_Rotterdam_nsr', 'Shanghai_Genova_nsr', 'Shanghai_Malta_nsr'],
    ['Yokohama_Mumbai', 'Yokohama_Singapore', 'Yokohama_Shanghai', 'Yokohama', 'Yokohama_Murmansk_nsr', 'Yokohama_Rotterdam_nsr', 'Yokohama_Genova_nsr', 'Yokohama_Malta_nsr'],
    ['Murmansk_Mumbai_nsr', 'Murmansk_Singapore_nsr', 'Murmansk_Shanghai_nsr', 'Murmansk_Yokohama', 'Murmansk', 'Murmansk_Rotterdam', 'Murmansk_Genova', 'Murmansk_Malta'],
    ['Rotterdam_Mumbai_nsr', 'Rotterdam_Singapore_nsr', 'Rotterdam_Shanghai_nsr', 'Rotterdam_Yokohama_nsr', 'Rotterdam_Murmansk', 'Rotterdam', 'Rotterdam_Genova', 'Rotterdam_Malta'],
    ['Genova_Mumbai_nsr', 'Genova_Singapore_nsr', 'Genova_Shanghai_nsr', 'Genova_Yokohama_nsr', 'Genova_Murmansk', 'Genova_Rotterdam', 'Genova', 'Genova_Malta'],
    ['Malta_Mumbai_nsr', 'Malta_Singapore_nsr', 'Malta_Shanghai_nsr', 'Malta_Yokohama_nsr', 'Malta_Murmansk', 'Malta_Rotterdam', 'Malta_Genova', 'Malta']   
    ])

    scr_routes = np.array([
    ['Mumbai', 'Mumbai_Singapore', 'Mumbai_Shanghai', 'Mumbai_Yokohama', 'Mumbai_Murmansk_scr', 'Mumbai_Rotterdam_scr', 'Mumbai_Genova_scr', 'Mumbai_Malta_scr'],
    ['Singapore_Mumbai', 'Singapore', 'Singapore_Shanghai', 'Singapore_Yokohama', 'Singapore_Murmansk_scr', 'Singapore_Rotterdam_scr', 'Singapore_Genova_scr', 'Singapore_Malta_scr'],
    ['Shanghai_Mumbai', 'Shanghai_Singapore', 'Shanghai', 'Shanghai_Yokohama', 'Shanghai_Murmansk_scr', 'Shanghai_Rotterdam_scr', 'Shanghai_Genova_scr', 'Shanghai_Malta_scr'],
    ['Yokohama_Mumbai', 'Yokohama_Singapore', 'Yokohama_Shanghai', 'Yokohama', 'Yokohama_Murmansk_scr', 'Yokohama_Rotterdam_scr', 'Yokohama_Genova_scr', 'Yokohama_Malta_scr'],
    ['Murmansk_Mumbai_scr', 'Murmansk_Singapore_scr', 'Murmansk_Shanghai_scr', 'Murmansk_Yokohama', 'Murmansk', 'Murmansk_Rotterdam', 'Murmansk_Genova', 'Murmansk_Malta'],
    ['Rotterdam_Mumbai_scr', 'Rotterdam_Singapore_scr', 'Rotterdam_Shanghai_scr', 'Rotterdam_Yokohama_scr', 'Rotterdam_Murmansk', 'Rotterdam', 'Rotterdam_Genova', 'Rotterdam_Malta'],
    ['Genova_Mumbai_scr', 'Genova_Singapore_scr', 'Genova_Shanghai_scr', 'Genova_Yokohama_scr', 'Genova_Murmansk', 'Genova_Rotterdam', 'Genova', 'Genova_Malta'],
    ['Malta_Mumbai_scr', 'Malta_Singapore_scr', 'Malta_Shanghai_scr', 'Malta_Yokohama_scr', 'Malta_Murmansk', 'Malta_Rotterdam', 'Malta_Genova', 'Malta']   
    ])

############################################ Map Routes ###################################################

    if route == 'NSR':
        sheet_name = nsr_routes[origin,destination]
    elif route == 'SCR':
        sheet_name = scr_routes[origin][destination]
    print(sheet_name)
    print('origin: ', origin)
    print('destination: ', destination)
    df = pd.read_excel(xlsx_file, sheet_name, names=['ports','latitude', 'longitude'])

    origin_index = df[df['ports']==origin].index[0]
    print('origin_index: ', origin_index)
    destination_index = df[df['ports']==destination].index[0]
    
    coordinates = list()
    for i in range(origin_index,destination_index+1):
        coordinates.append([df.loc[i]['latitude'],df.loc[i]['longitude']])
    
    #ship_icon.add_to(m)
    plugins.AntPath(coordinates, color="#ff3399", pulse_color='white', dash_array=[1,15], use='circle',tooltip=str(distance)+' nr',popup=str(distance)+' nr',weight=3, opacity=0.8).add_to(m)
    
    ############################################ Vessel Ship ##############################################
    ship_loc = coordinates[0]
    ship_icon = folium.DivIcon(html=f"""<center><img src="https://img.icons8.com/external-konkapp-outline-color-konkapp/64/000000/external-ship-logistic-and-delivery-konkapp-outline-color-konkapp.png"/></center>""")
    folium.Marker(location=ship_loc, icon=ship_icon).add_to(m)

    ################################################# Piracy Area ##########################################
    piracy_location = [(-5.222,39.331),(-4.959,49.965),(0.131,54.931),(9.968,59.853),(14.008,59.941),(16.989,54.05),(14.902,42.846),(15.126,39.694)]
    folium.vector_layers.Polygon(locations=piracy_location, tooltip='Pirate Zone',fill_color='red',fill_opacity=0.4,weight=1,color='black',opacity=0.5,num_sides=3, radius=3).add_to(m)

    ################################################# Pirates Ship ##########################################
    lst = [(-4.565,40.649),(-3.864,44.472),(-2.328,48.251),(0.219,51.416),(3.688,53.657),(6.096,57.832),(10.098,59.941),
        (13.923,59.809),(16.045,57.128),(13.795,52.426),(12.726,48.911),(11.178,44.472)]
    def create_geojson_features(lst):
        features = []
        for i in range(len(lst)):
            feature = {
                'type': 'Feature',
                'geometry': {
                    'type':'Point', 
                    'coordinates':[lst[i][1],lst[i][0]]
                },
                'properties': {
                    'time': i* 100000,
                    'style': {'color' : ''},
                    'icon': 'marker',
                    'iconstyle':{
                        'iconUrl': "https://img.icons8.com/external-justicon-lineal-color-justicon/50/000000/external-ship-pirates-justicon-lineal-color-justicon.png",
                        'fillColor': 'orange',
                        'iconSize': [35, 35],
                        'fillOpacity': 0.8,
                        'stroke': 'True',
                        'radius': i,
                        'id': 'house'
                    }
                }
            }
            
            features.append(feature)
        return features
    start_geojson = create_geojson_features(lst)

    #add TimestampedGeoJson
    TimestampedGeoJson(start_geojson,period = 'PT1M',duration = 'PT1M',transition_time = 1000,auto_play = True).add_to(m)

    ############################################## Add ports ###########################################

    xlsx_ports = pd.read_excel(xlsx_file, 'ports', names=['ports','country', 'latitude', 'longitude'])
    df_ports = pd.DataFrame(xlsx_ports)
    ##################################################### Add ports #############################################################
    for i in range(0,len(df_ports)):
        ports_loc = [df_ports.iloc[i]['latitude'], df_ports.iloc[i]['longitude']]
        pop = df_ports.iloc[i]['ports']
        title = df_ports.iloc[i]['ports']
        #ports_icons = folium.DivIcon(html=f"""<center><img src="port.png" style="width:35px;height:35px; alt="Italian Trulli"></center>""", icon_anchor=(0,0))

        folium.Marker(location=ports_loc, popup=pop, title=title, draggable=False).add_to(m)

########################################### Add Names of the ports on the map #############################################################   

    for i in range(0,len(df_ports)):
       folium.Marker(location=[df_ports.iloc[i]['latitude'], df_ports.iloc[i]['longitude']],popup=df_ports.iloc[i]['ports'],icon=folium.DivIcon(html=f"""<div style="font-family: courier new; color: black">{df_ports.iloc[i]['ports']}</div>""")).add_to(m)

    ############################################ Show Map ##############################################
    m.save('ship.html')
    webbrowser.open('ship.html')
    
#################################################################################################################################################################################################
########################################################################################## Vessel Tab ###########################################################################################
#################################################################################################################################################################################################

########################################################################################## Vessel ##########################################################################################
tab_vessel.columnconfigure(0,weight=1)
tab_vessel.columnconfigure(2,weight=1)
# create label frame
lf_vessel = ttk.LabelFrame(tab_vessel, text="Vessel", relief=SUNKEN)
lf_vessel.grid(column=1,row=0, padx=10, pady=10, ipadx=10, ipady=10, sticky=tk.EW)

# Label Desription
ttk.Label(lf_vessel, text="5- Select one of the vessels or specify a new one.", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=3)

# veseel
selected_vessel = tk.StringVar()
vessel_1 = ttk.Radiobutton(lf_vessel, text="Al Dahna", value='Al Dahna', variable=selected_vessel, command=lambda: vesselSelection('Al Dahna'))
vessel_2 = ttk.Radiobutton(lf_vessel, text="Afif", value='Afif', variable=selected_vessel, command=lambda: vesselSelection('Afif'))
vessel_3 = ttk.Radiobutton(lf_vessel, text="Ain Snan", value='Ain Snan', variable=selected_vessel, command=lambda: vesselSelection('Ain Snan'))
vessel_4 = ttk.Radiobutton(lf_vessel, text="Cartagena Express", value='Cartagena Express', variable=selected_vessel, command=lambda: vesselSelection('Cartagena Express'))
vessel_5 = ttk.Radiobutton(lf_vessel, text="Chicago Express", value='Chicago Express', variable=selected_vessel, command=lambda: vesselSelection('Chicago Express'))
vessel_6 = ttk.Radiobutton(lf_vessel, text="Palena", value='Palena', variable=selected_vessel, command=lambda: vesselSelection('Palena'))
vessel_7 = ttk.Radiobutton(lf_vessel, text="Rotterdam Express", value='Rotterdam Express', variable=selected_vessel, command=lambda: vesselSelection('Rotterdam Express'))
vessel_8 = ttk.Radiobutton(lf_vessel, text="NEW", value='new', variable=selected_vessel, command=lambda: vesselSelection('new'))

vessel_1.grid(column=0, row=1, sticky=tk.W, padx=10)
vessel_2.grid(column=0, row=2, sticky=tk.W, padx=10)
vessel_3.grid(column=0, row=3, sticky=tk.W, padx=10)
vessel_4.grid(column=0, row=4, sticky=tk.W, padx=10)
vessel_5.grid(column=0, row=5, sticky=tk.W, padx=10)
vessel_6.grid(column=0, row=6, sticky=tk.W, padx=10)
vessel_7.grid(column=0, row=7, sticky=tk.W, padx=10)
vessel_8.grid(column=0, row=8, sticky=tk.W, padx=10)

# TEU
teu = tk.IntVar()
tue_label = ttk.Label(lf_vessel, text="TEU * : ")
tue_label.grid(column=2, row=1, sticky=tk.W, padx=26, pady=1)
teu_entry = ttk.Entry(lf_vessel, textvariable=teu)
teu_entry.grid(column=2, row=2, sticky=tk.W, padx=26, pady=1)

# Balloon TEU
balloon_teu = Pmw.Balloon(lf_vessel)
balloon_teu.bind(tue_label,'A TEU or Twenty-foot Equivalent Unit is an exact unit of measurement \nused to determine cargo capacity for container ships and terminals. \nThis measurement is derived from the dimensions of a 20ft standardized shipping container.')

# Gross Tonnage
gross = tk.IntVar()
gross_label = ttk.Label(lf_vessel, text="Gross Tonnage (ton) * : ")
gross_label.grid(column=2, row=3, sticky=tk.W, padx=26, pady=1)
gross_entry = ttk.Entry(lf_vessel, textvariable=gross)
gross_entry.grid(column=2, row=4, sticky=tk.W, padx=26, pady=1)

# Balloon Gross Tonnage
balloon_gross = Pmw.Balloon(lf_vessel)
balloon_gross.bind(gross_label,"Gross tonnage (GT) is a function of the volume of all of a ship's enclosed spaces \n(from keel to funnel) measured to the outside of the hull framing.")

### trace
gross.trace('w', callbackCost)

# DWT
dwt = tk.IntVar()
dwt_label = ttk.Label(lf_vessel, text="DWT (ton) * : ")
dwt_label.grid(column=2, row=5, sticky=tk.W, padx=26, pady=1)
dwt_entry = ttk.Entry(lf_vessel, textvariable=dwt)
dwt_entry.grid(column=2, row=6, sticky=tk.W, padx=26, pady=1)

# Balloon DWT
balloon_dwt = Pmw.Balloon(lf_vessel)
balloon_dwt.bind(dwt_label,"Deadweight tonnage or tons deadweight is a measure of how much weight a ship can carry. \nIt is the sum of the weights of cargo, fuel, fresh water, ballast water, provisions, passengers, and crew.")

# Length
length = tk.IntVar()
length_label = ttk.Label(lf_vessel, text="Length (m): ")
length_label.grid(column=2, row=7, sticky=tk.W, padx=26, pady=1)
length_entry = ttk.Entry(lf_vessel, textvariable=length)
length_entry.grid(column=2, row=8, sticky=tk.W, padx=26, pady=1)

# Beam
beam = tk.IntVar()
beam_label = ttk.Label(lf_vessel, text="Beam (m): ")
beam_label.grid(column=2, row=9, sticky=tk.W, padx=26, pady=1)
beam_entry = ttk.Entry(lf_vessel, textvariable=beam)
beam_entry.grid(column=2, row=10, sticky=tk.W, padx=26, pady=1)

# Fuel Tank Capacity
fuel_tank_capacity = tk.DoubleVar()
fuel_tank_capacity_label = ttk.Label(lf_vessel, text="Fuel Tank Capacity (Million Gallon): ")
fuel_tank_capacity_label.grid(column=2, row=11, sticky=tk.W, padx=26, pady=1)
fuel_tank_capacity_entry = ttk.Entry(lf_vessel, textvariable=fuel_tank_capacity)
fuel_tank_capacity_entry.grid(column=2, row=12, sticky=tk.W, padx=26, pady=1)

# Built Year
built_year = tk.StringVar()
built_year_label = ttk.Label(lf_vessel, text="Built Year: ")
built_year_label.grid(column=3, row=1, sticky=tk.W, padx=26, pady=1)
built_year_entry = ttk.Entry(lf_vessel, textvariable=built_year)
built_year_entry.grid(column=3, row=2, sticky=tk.W, padx=26, pady=1)

# Engine Power
engine_power = tk.IntVar()
engine_power_label = ttk.Label(lf_vessel, text="Engine Power (KW): ")
engine_power_label.grid(column=3, row=3, sticky=tk.W, padx=26, pady=1)
engine_power_entry = ttk.Entry(lf_vessel, textvariable=engine_power)
engine_power_entry.grid(column=3, row=4, sticky=tk.W, padx=26, pady=1)

# Nominal Speed
nominal_speed = tk.DoubleVar()
nominal_speed_label = ttk.Label(lf_vessel, text="Nominal Speed (knots): ")
nominal_speed_label.grid(column=3, row=5, sticky=tk.W, padx=26, pady=1)
nominal_speed_entry = ttk.Entry(lf_vessel, textvariable=nominal_speed)
nominal_speed_entry.grid(column=3, row=6, sticky=tk.W, padx=26, pady=1)

# Crew
crew = tk.IntVar()
crew_label = ttk.Label(lf_vessel, text="Crew: ")
crew_label.grid(column=3, row=7, sticky=tk.W, padx=26, pady=1)
crew_entry = ttk.Entry(lf_vessel, textvariable=crew)
crew_entry.grid(column=3, row=8, sticky=tk.W, padx=26, pady=1)

# Capital Cost of building the vessel
capital_cost = tk.DoubleVar()
capital_cost_label = ttk.Label(lf_vessel, text="Vessel Price (Millions USD): ")
capital_cost_label.grid(column=3, row=9, sticky=tk.W, padx=26, pady=1)
capital_cost_entry = ttk.Entry(lf_vessel, textvariable=capital_cost)
capital_cost_entry.grid(column=3, row=10, sticky=tk.W, padx=26, pady=1)

### trace
capital_cost.trace('w', callbackCost)

# Fuel Consumption 
fuel_consumption = tk.DoubleVar()
fuel_consumption_label = ttk.Label(lf_vessel, text="Fuel Consumption (Gallon/Day): ")
fuel_consumption_label.grid(column=3, row=11, sticky=tk.W, padx=26, pady=1)
fuel_consumption_entry = ttk.Entry(lf_vessel, textvariable=fuel_consumption)
fuel_consumption_entry.grid(column=3, row=12, sticky=tk.W, padx=26, pady=1)

### trace
fuel_consumption.trace('w', callbackTime)

########################################################################################## Repair and Services ##########################################################################################
# create label frame
lf_repair_service = ttk.LabelFrame(tab_vessel, text="Repair and Services Cost")
lf_repair_service.grid(column=1,row=1, padx=10, pady=7, ipady=5, ipadx=5, sticky=tk.EW)
lf_repair_service.columnconfigure(0, weight=1)
lf_repair_service.columnconfigure(1, weight=1)
lf_repair_service.columnconfigure(2, weight=1)
lf_repair_service.columnconfigure(3, weight=1)

# Label Desription
ttk.Label(lf_repair_service, text="6- Annual Repair and Maintanance cost including 'cost of ship', 'lubricant cost', 'dock cost' ,and 'spare parts cost':", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=5)

# Coefficient Repair and Services
coefficient_repair_service = tk.DoubleVar()
coefficient_repair_service_label = ttk.Label(lf_repair_service, text="Coefficient (%):")
coefficient_repair_service_label.grid(column=0, row=1, sticky=tk.W)
coefficient_repair_service_entry= ttk.Entry(lf_repair_service, textvariable = coefficient_repair_service)
coefficient_repair_service_entry.grid(column=1, row=1, sticky=tk.W)

### trace
coefficient_repair_service.trace('w', callbackCost)

# Repair and Services Cost
repair_service_cost = tk.DoubleVar()
repair_service_label = ttk.Label(lf_repair_service, text="Cost of Repair & Services (Million USD)")
repair_service_label.grid(column=2, row=1, sticky=tk.W)
repair_service_entry= ttk.Entry(lf_repair_service, textvariable = repair_service_cost)
repair_service_entry.config(state=DISABLED)
repair_service_entry.grid(column=3, row=1, padx=5, sticky=tk.E)

### trace
repair_service_cost.trace('w', callbackCost)

########################################################################################## Annual Capital Cost and Depreciation of Vessel ##########################################################################################
# create label frame
lf_capital_cost = ttk.LabelFrame(tab_vessel, text="Annual Capital Cost and Depreciation of Vessel")
lf_capital_cost.grid(column=1,row=2, padx=10, pady=7, ipady=5, ipadx=5, sticky=tk.EW)
lf_capital_cost.columnconfigure(0, weight=1)
lf_capital_cost.columnconfigure(1, weight=1)
lf_capital_cost.columnconfigure(2, weight=1)
lf_capital_cost.columnconfigure(3, weight=1)

# Label Desription
ttk.Label(lf_capital_cost, text="7- You can change this amount as a persentage of the capital cost of vessel: ", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=5)

# Label coefficient annual capital cost
coefficient_capital_cost_label = ttk.Label(lf_capital_cost, text="Coefficient (%): ")
coefficient_capital_cost_label.grid(column=0, row=1, sticky=tk.W)
# Entry coefficient annual capital cost
coefficient_capital_cost = tk.DoubleVar()
coefficient_capital_cost_entry = ttk.Entry(lf_capital_cost, textvariable = coefficient_capital_cost)
coefficient_capital_cost_entry.grid(column=1, row=1,padx=5, sticky=tk.E)

### trace
coefficient_capital_cost.trace('w', callbackCost)

# Label Annual Capital Cost
annual_capital_cost_label = ttk.Label(lf_capital_cost, text="Annual Capital Cost & Depreciation (Million USD): ")
annual_capital_cost_label.grid(column=2, row=1, sticky=tk.E)
# Entry Annual Capital Cost
annual_capital_cost = tk.DoubleVar()
annual_capital_cost_entry = ttk.Entry(lf_capital_cost, textvariable = annual_capital_cost)
annual_capital_cost_entry.config(state=DISABLED)
annual_capital_cost_entry.grid(column=3, row=1, padx=5, sticky=tk.E)

########################################################################################## Insurance Vessel Structure ##########################################################################################
# create label frame
lf_insurance = ttk.LabelFrame(tab_vessel, text="Insurance")
lf_insurance.grid(column=1,row=3, padx=10, pady=7, ipady=5, ipadx=5, sticky=tk.EW)
lf_insurance.columnconfigure(0, weight=1)
lf_insurance.columnconfigure(1, weight=1)
lf_insurance.columnconfigure(2, weight=1)
lf_insurance.columnconfigure(3, weight=1)

# Label Desription
ttk.Label(lf_insurance, text="8- Here the annual insurance cost of the vessel structure is calculated by the percentage of capital cost of vessel:", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=5)

# Label coefficient annual insurance
coefficient_insurance_label = ttk.Label(lf_insurance, text="Coefficient (%): ")
coefficient_insurance_label.grid(column=0, row=1, sticky=tk.W)
# Entry coefficient annual insurance
coefficient_insurance = tk.DoubleVar()
coefficient_insurance_entry = ttk.Entry(lf_insurance, textvariable = coefficient_insurance)
coefficient_insurance_entry.grid(column=1, row=1, sticky=tk.W)

### trace
coefficient_insurance.trace('w', callbackCost)

# Label Annual Insurance Cost
annual_insurance_cost_label = ttk.Label(lf_insurance, text="Annual Insurance Cost (Million USD): ")
annual_insurance_cost_label.grid(column=2, row=1, sticky=tk.E)
# Entry Annual Insurance Cost
annual_insurance_cost = tk.DoubleVar()
annual_insurance_cost_entry = ttk.Entry(lf_insurance, textvariable = annual_insurance_cost)
annual_insurance_cost_entry.config(state=DISABLED)
annual_insurance_cost_entry.grid(column=3, row=1, padx=5, sticky=tk.E)

########################################################################################## Salary tab vessel ##########################################################################################
# create label frame
lf_salary_month = ttk.LabelFrame(tab_vessel, text="Salary")
lf_salary_month.grid(column=1,row=4, padx=10, pady=7, ipady=5, ipadx=5)

# Label Desription
ttk.Label(lf_salary_month, text="9- Average Salary per month for crew (USD): ", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5)

# Entry Salary
salary_month = tk.IntVar()
salary_month_entry = ttk.Entry(lf_salary_month, textvariable=salary_month)
salary_month_entry.grid(column=1, row=0, sticky=tk.W)

### trace
salary_month.trace("w",callbackCost)

########################################################################################## Lubricant ##########################################################################################

#################################################################################################################################################################################################
########################################################################################## Cargo Tab ###########################################################################################
#################################################################################################################################################################################################

########################################################################################## Cargo ##########################################################################################

# create label frame
lf_cargo = ttk.LabelFrame(tab_cargo, text="Cargo")
lf_cargo.grid(column=1, row=1, padx=10, pady=10, ipadx=10, ipady=10)
lf_cargo.columnconfigure(0,weight=1)
lf_cargo.columnconfigure(2,weight=1)
ttk.Label(lf_cargo, text="10- Select the type of the cargo and its value. (It affects on the 'cargo insurance' cost)", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=5)

# label cargo
cargo_label = ttk.Label(lf_cargo, text="Cargo Type: ")
cargo_label.grid(column=0, row=1, sticky=tk.W, padx=5)
# create a combobox cargo
cargo = tk.StringVar()
cargo_combo = ttk.Combobox(lf_cargo, textvariable=cargo, width=38)
cargo_combo.grid(column=1, row=1, sticky=tk.W, padx=5, pady=10)
cargo_combo['values'] = ['Machinery, Equipment, and Factory Parts','LNG, CNG, and Other Gas-Based Fuels','Livestock and Animals','Food Stuff','Dry Bulk Cargo','Liquid Bulk Cargo','Chemical, Hazardous, and Toxic Products']

# label cargo value
cargo_value_label = ttk.Label(lf_cargo, text="Cargo Value (Million Dollar): ")
cargo_value_label.grid(column=0, row=2, sticky=tk.W, pady=5, padx=5)
# Entry Fuel Price
cargo_value = tk.DoubleVar()
cargo_value_entry = ttk.Entry(lf_cargo, textvariable=cargo_value)
cargo_value_entry.grid(column=1, row=2, sticky=tk.W, pady=5, padx=5)

### trace
cargo_value.trace('w', callbackCost)

# label cargo weight
cargo_weight_label = ttk.Label(lf_cargo, text="Cargo Weight (ton): ")
cargo_weight_label.grid(column=0, row=3, sticky=tk.W, pady=5, padx=5)
# Entry Fuel Price
cargo_weight = tk.DoubleVar()
cargo_weight_entry = ttk.Entry(lf_cargo, textvariable=cargo_weight)
cargo_weight_entry.grid(column=1, row=3, sticky=tk.W, pady=5, padx=5)

########################################################################################## Cargo Insurance ######################################################################################
# create label frame
lf_cargo_insurance = ttk.LabelFrame(tab_cargo, text="Cargo Insurance")
lf_cargo_insurance.grid(column=1, row=2, padx=10, pady=10, ipadx=10, ipady=10)
tab_cargo.columnconfigure(0, weight=1)
tab_cargo.columnconfigure(2, weight=1)

# Label Description
ttk.Label(lf_cargo_insurance, text="11- Here you can define the cargo insurance price based on the percentage of the cargo value.", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=3)

# label cargo insurance
cargo_insurance_coefficient_label = ttk.Label(lf_cargo_insurance, text="Coefficient (%):")
cargo_insurance_coefficient_label.grid(column=0, row=1, sticky=tk.W, padx=5)
cargo_insurance_coefficient = tk.DoubleVar()
cargo_insurance_coefficient_entry = ttk.Entry(lf_cargo_insurance, textvariable=cargo_insurance_coefficient)
cargo_insurance_coefficient_entry.grid(column=1, row=1, sticky=tk.W, pady=5, padx=5)

### trace
cargo_insurance_coefficient.trace('w', callbackCost)

# label cargo insurance cost
cargo_insurance_cost_label = ttk.Label(lf_cargo_insurance, text="Cargo Insurance Cost (Million Dollar):")
cargo_insurance_cost_label.grid(column=2, row=1, sticky=tk.W, padx=5)
cargo_insurance_cost = tk.DoubleVar()
cargo_insurance_cost_entry = ttk.Entry(lf_cargo_insurance, textvariable=cargo_insurance_cost)
cargo_insurance_cost_entry.config(state=DISABLED)
cargo_insurance_cost_entry.grid(column=3, row=1, sticky=tk.W, pady=5, padx=5)

### trace
cargo_insurance_cost.trace('w', callbackCost)

#################################################################################################################################################################################################
########################################################################################## Time Tab ###########################################################################################
#################################################################################################################################################################################################
# create label frame
lf_time = ttk.LabelFrame(tab_time, text="Time")
lf_time.grid(column=0,row=3, padx=10, pady=10)

#################################################################################### Bureaucracy and administrative #######################################################################################
# create label frame Bureaucracy and administrative
lf_bureaucracy = ttk.LabelFrame(tab_time, text="Bureaucracy and administrative")
lf_bureaucracy.grid(column=0,row=0, sticky=tk.W, padx=10, pady=10, ipady=5)

# Label Desription
ttk.Label(lf_bureaucracy, text="12- Define estimated delay time for Bureaucracy and administrative (hour):", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5)

# Entry Bureaucracy and administrative
################# it gets from totla fuel
bureaucracy = tk.IntVar()
bureaucracy_entry = ttk.Entry(lf_bureaucracy, textvariable=bureaucracy)
bureaucracy_entry.grid(column=0, row=1)

### trace
bureaucracy.trace('w', callbackTime)

########################################################################################## Dwell Time #################################################################################################
# create label frame Dwell Time
lf_dwell = ttk.LabelFrame(tab_time, text="Dwell Time * ")
lf_dwell.grid(column=1,row=0, sticky=tk.W, padx=10, pady=10, ipady=5)

# Balloon Dwell Time
balloon_dwell_time = Pmw.Balloon(tab_time)
balloon_dwell_time.bind(lf_dwell,'Port dwell time is the amount of time which cargo or ships spend within a port.')

# Label Desription
ttk.Label(lf_dwell, text="13- Define estimated delay time for dwelling in each port (hour):", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5)

# Entry Bureaucracy and administrative
dwell = tk.IntVar()
dwell_entry = ttk.Entry(lf_dwell, textvariable=dwell)
dwell_entry.grid(column=0, row=1)

### trace
dwell.trace('w', callbackTime)
########################################################################################## Bunker Time #################################################################################################
# create label frame
lf_bunkering = ttk.LabelFrame(tab_time, text="Bunkering")
lf_bunkering.grid(column=0,row=1, padx=10, pady=10, ipady=5)

# Label Desription
ttk.Label(lf_bunkering, text="14- Define average time delay expected for bunkering in each port (hour):", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=2)

# label bunker
bunkering_label = ttk.Label(lf_bunkering, text="Average time delay for bunkering (hour):")
bunkering_label.grid(column=0, row=1, sticky=tk.W)

# Spinbox Bunkering
bunkering = tk.IntVar(value=12)
bunkering_spin_box = ttk.Spinbox(lf_bunkering,from_=0,to=100,textvariable=bunkering)
bunkering_spin_box.grid(column=1, row=1, sticky=tk.W, pady=5)

### trace
bunkering.trace('w',callbackTime)

# label required fuel
required_fuel_label = ttk.Label(lf_bunkering, text="Required Fuel (Gallon):")
required_fuel_label.grid(column=0, row=2, sticky=tk.W, pady=5)
# Entry required fuel
required_fuel = tk.DoubleVar()
required_fuel_entry = ttk.Entry(lf_bunkering, textvariable=required_fuel)
required_fuel_entry.config(state=DISABLED)
required_fuel_entry.grid(column=1, row=2, sticky=tk.W, pady=5)

# label vessel fuel capacity
vessel_fuel_capacity_label = ttk.Label(lf_bunkering, text="Vessel Fuel Capacity (Million Gallon):")
vessel_fuel_capacity_label.grid(column=0, row=3, sticky=tk.W, pady=5)
# Entry vessel fuel capacity
vessel_fuel_capacity_entry = ttk.Entry(lf_bunkering, textvariable=fuel_tank_capacity)
vessel_fuel_capacity_entry.config(state=DISABLED)
vessel_fuel_capacity_entry.grid(column=1, row=3, sticky=tk.W, pady=5)

# label number of refueling
refueling_times_label = ttk.Label(lf_bunkering, text="Number of Refueling:")
refueling_times_label.grid(column=0, row=4, sticky=tk.W, pady=5)
# Entry number of refueling
refueling_times = tk.IntVar()
refueling_times_entry = ttk.Entry(lf_bunkering, textvariable=refueling_times)
refueling_times_entry.grid(column=1, row=4, sticky=tk.W, pady=5)
refueling_times_entry.config(state=DISABLED)

# label estimated time delay for refueling
refueling_time_delay_label = ttk.Label(lf_bunkering, text="Estimated time delay for refueling (hour):")
refueling_time_delay_label.grid(column=0, row=5, sticky=tk.W, pady=5)
# Entry estimated time delay for refueling
################## it gets by calculating bunkering time and refueling times
refueling_time_delay = tk.DoubleVar()
refueling_time_delay_entry = ttk.Entry(lf_bunkering, textvariable=refueling_time_delay)
refueling_time_delay_entry.config(state=DISABLED)
refueling_time_delay_entry.grid(column=1, row=5, sticky=tk.W, pady=5)

########################################################################################## Total Shipping Time #################################################################################################
# create label Total Shipping Time
lf_total_time = ttk.LabelFrame(tab_time, text="Total Time")
lf_total_time.grid(column=1,row=1, padx=10, pady=10, columnspan=2, ipadx=10, ipady=5)

# Label Desription
ttk.Label(lf_total_time, text="Total voyage shipping time is estimated (Days):", foreground='blue').grid(column=0,row=0, pady=5)

# Entry Total Shipping Time
total_voyage_time = tk.DoubleVar()
total_voyage_time_entry = ttk.Entry(lf_total_time, textvariable=total_voyage_time)
total_voyage_time_entry.grid(column=0, row=1)
total_voyage_time_entry.config(state=DISABLED)
### trace
total_voyage_time.trace('w', callbackCost)

#################################################################################################################################################################################################
########################################################################################## Fuel Tab ###########################################################################################
#################################################################################################################################################################################################

########################################################################################## Fuel type ##########################################################################################
tab_fuel.columnconfigure(0,weight=1)
tab_fuel.columnconfigure(2,weight=1)
# create label frame
lf_fuel = ttk.LabelFrame(tab_fuel, text="Fuel")
lf_fuel.grid(column=1,row=1, padx=10, pady=10)

# Label Desription
ttk.Label(lf_fuel, text="15- Select the fuel (it affacts on the cost, time and environmental effects).", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=3)

# radio buttons fuel selection
fuel_selected = tk.StringVar()
fuel_1 = ttk.Radiobutton(lf_fuel, text='IFO380', value=0, variable=fuel_selected, command=lambda: fuelSelection(fuel_selected.get()))
fuel_2 = ttk.Radiobutton(lf_fuel, text='MGO', value=1, variable=fuel_selected, command=lambda: fuelSelection(fuel_selected.get()))
fuel_3 = ttk.Radiobutton(lf_fuel, text='VLSFO', value=2, variable=fuel_selected, command=lambda: fuelSelection(fuel_selected.get()))
fuel_4 = ttk.Radiobutton(lf_fuel, text='ULSFO', value=3, variable=fuel_selected, command=lambda: fuelSelection(fuel_selected.get()))
fuel_5 = ttk.Radiobutton(lf_fuel, text='IFO180', value=4, variable=fuel_selected, command=lambda: fuelSelection(fuel_selected.get()))
fuel_1.grid(column=0, row=1, sticky=tk.W, pady=5)
fuel_2.grid(column=0, row=2, sticky=tk.W, pady=5)
fuel_3.grid(column=0, row=3, sticky=tk.W, pady=5)
fuel_4.grid(column=0, row=4, sticky=tk.W, pady=5)
fuel_5.grid(column=0, row=5, sticky=tk.W, pady=5)

# label Fuel Price
fuel_price_label = ttk.Label(lf_fuel, text="Average Fuel Price (USD/mt)*:")
fuel_price_label.grid(column=1, row=2, sticky=tk.W, pady=5)
balloon = Pmw.Balloon(lf_fuel)
balloon.bind(fuel_price_label,'mt represents metric tons and each mt equals 521 gallons')

# Entry Fuel Price
fuel_price = tk.IntVar()
fuel_price_entry = ttk.Entry(lf_fuel, textvariable=fuel_price)
fuel_price_entry.grid(column=1, row=3, sticky=tk.W, pady=5)

# Function Fuel selection price
def fuelSelection(arg):
    fuel_price_entry.delete(0, END)
    fuel_price_entry.insert(0, fuel_selected.get())
    # Entry Total Fuel Consumption in this voyage (Gallon)
    total_fuel_consumption_entry.config(state=ACTIVE)
    total_fuel_consumption_entry.delete(0, END)
    total_fuel_consumption_entry.insert(0, round(fuel_consumption.get() * shipping_time.get(),3))
    total_fuel_consumption_entry.config(state=DISABLED)
    # Entry Total Fuel Consumption Cost for this voyage (USD)
    total_fuel_consumption_cost_entry.config(state=ACTIVE)
    total_fuel_consumption_cost_entry.delete(0, END)
    total_fuel_consumption_cost_entry.insert(0, int(total_fuel_consumption.get() * fuel_price.get() / 521))
    total_fuel_consumption_cost_entry.config(state=DISABLED)
    # set fuel price for fuel mean risk
    feul_mean_risk.set(fuel_price.get())

########################################################################################## Fuel Cost ##########################################################################################
# create label frame
lf_fuel_cost = ttk.LabelFrame(tab_fuel, text="Fuel Cost")
lf_fuel_cost.grid(column=1,row=2, padx=10, pady=10)

# Label Shipping Time
shipping_time_label = ttk.Label(lf_fuel_cost, text='Shipping Time (days): ')
shipping_time_label.grid(column=0, row=0, pady=5, padx=3, sticky=tk.W)
# Entry Shipping Time
shipping_time_entry_fuel = ttk.Entry(lf_fuel_cost, textvariable=shipping_time)
shipping_time_entry_fuel.config(state=DISABLED)
shipping_time_entry_fuel.grid(column=1, row=0, padx=3, pady=5, sticky=tk.W)

# Label Fuel Consumption
fuel_consumption_label = ttk.Label(lf_fuel_cost, text="Vessel Fuel Consumption (Gallon/day): ")
fuel_consumption_label.grid(column=0, row=1, padx=3, pady=5, sticky=tk.W)
# Entry Fuel Consumption
fuel_consumption_entry = ttk.Entry(lf_fuel_cost, textvariable=fuel_consumption)
fuel_consumption_entry.config(state=DISABLED)
fuel_consumption_entry.grid(column=1, row=1, padx=3, pady=5, sticky=tk.W)

# Label Total Vessel Fuel Consumption
total_fuel_consumption_label = ttk.Label(lf_fuel_cost, text="Total Vessel Fuel Consumption in this voyage (Gallon): ")
total_fuel_consumption_label.grid(column=0, row=2, padx=3, pady=5, sticky=tk.W)
# Entry Fuel Consumption
total_fuel_consumption = tk.DoubleVar()
total_fuel_consumption_entry = ttk.Entry(lf_fuel_cost, textvariable=total_fuel_consumption)
total_fuel_consumption_entry.grid(column=1, row=2, padx=3, pady=5, sticky=tk.W)

# Label Total Fuel Consumption price
total_fuel_consumption_cost_label = ttk.Label(lf_fuel_cost, text="Total Fuel Price in this Voyage (USD): ")
total_fuel_consumption_cost_label.grid(column=0, row=3, padx=3, pady=5, sticky=tk.W)
# Entry Total Fuel Consumption Price
total_fuel_consumption_cost = tk.IntVar()
total_fuel_consumption_cost_entry = ttk.Entry(lf_fuel_cost, textvariable=total_fuel_consumption_cost)
total_fuel_consumption_cost_entry.grid(column=1, row=3, padx=3, pady=5, sticky=tk.W)

#################################################################################################################################################################################################
########################################################################################## Environment Tab ######################################################################################
#################################################################################################################################################################################################

########################################################################################## Cost of Air Pollution ################################################################################
# center
tab_environment.columnconfigure(0,weight=1)
tab_environment.columnconfigure(2,weight=1)

# create label frame
lf_cap = ttk.LabelFrame(tab_environment, text="Cost of Air Pollution (CAP)")
lf_cap.grid(column=1, row=0, padx=10, pady=10)

# label pollutant
label_pollutant = ttk.Label(lf_cap,text='Pollutant',font=("Helvetica", 10,"bold"))
label_pollutant.grid(column=0, row=0, padx=10, pady=10)

# label Emmision Factor
label_emission_factor = ttk.Label(lf_cap,text='Emission Factor (Kg/t) *',font=("Helvetica", 10, 'bold'))
label_emission_factor.grid(column=1, row=0, padx=10, pady=10)
Pmw.Balloon(lf_cap).bind(label_emission_factor,'(Kg emmited / tone of fuel)')

# label Pollution Cost
label_pollution_cost = ttk.Label(lf_cap,text='Pollution Cost (USD/t)',font=("Helvetica", 10, 'bold'))
label_pollution_cost.grid(column=2, row=0, padx=10, pady=10)

cap_dict = {
    'CO2':{'name':'CO2','balloon':'Carbon Dioxide','emission':3130.0,'nsr_emission':5078.33,'scr_emission':18455.19,'nsr_cost':0,'scr_cost':0,'gwp20_arctic':1.0,'gwp20_other':1.0,'co2_nsr':5078.32,'co2_scr':18455.19},
    'CO':{'name':'CO','balloon':'Carbon Monoxide','emission':7.4,'nsr_emission':12.01,'scr_emission':43.63,'nsr_cost':0,'scr_cost':0,'gwp20_arctic':1.8,'gwp20_other':1.8,'co2_nsr':21.61,'co2_scr':78.54},
    'SOx':{'name':'SOx','balloon':'Sulphur Oxides','emission':54.0,'nsr_emission':87.61,'scr_emission':318.4,'nsr_cost':8005.05,'scr_cost':10153.15,'gwp20_arctic':0,'gwp20_other':0,'co2_nsr':0,'co2_scr':0},
    'NOx':{'name':'NOx','balloon':'Nitrogen Oxides','emission':78.0,'nsr_emission':126.55,'scr_emission':459.91,'nsr_cost':3359.12,'scr_cost':2958.18,'gwp20_arctic':0,'gwp20_other':0,'co2_nsr':0,'co2_scr':0},
    'N2O':{'name':'N2O','balloon':'Nitrous Oxide','emission':0.08,'nsr_emission':0.13,'scr_emission':0.47,'nsr_cost':0, 'scr_cost':0, 'gwp20_arctic':265.0, 'gwp20_other':265.0, 'co2_nsr':34.39, 'co2_scr':125.0},
    'CH4':{'name':'CH4','balloon':'Methane', 'emission':0.3,'nsr_emission':0.49, 'scr_emission':1.77,'nsr_cost':0, 'scr_cost':0, 'gwp20_arctic':30.0, 'gwp20_other':30.0, 'co2_nsr':14.6, 'co2_scr':53.07},
    'NMVOC':{'name':'NMVOC','balloon':'Non-Methane Volatile Organic Compound','emission':2.4,'nsr_emission':3.89,'scr_emission':14.15,'nsr_cost':1214.23,'scr_cost':1186.72,'gwp20_arctic':0,'gwp20_other':0,'co2_nsr':0,'co2_scr':0},
    'BC':{'name':'BC','balloon':'Black Carbon','emission':0.35,'nsr_emission':0.57,'scr_emission':2.06,'nsr_cost':0, 'scr_cost':0, 'gwp20_arctic':1700.0,'gwp20_other':345.0, 'co2_nsr':3353.13, 'co2_scr':4882.08},
    'OC':{'name':'OC','balloon':'Organic Carbon','emission':1.07,'nsr_emission':1.74,'scr_emission':6.31,'nsr_cost':0, 'scr_cost':0, 'gwp20_arctic':0,'gwp20_other':0, 'co2_nsr':0, 'co2_scr':0},
    'PM25':{'name':'PM25','balloon':'Particulate Matter','emission':11.79,'nsr_emission':19.13,'scr_emission':69.52,'nsr_cost':21084.14, 'scr_cost':28228.21,'gwp20_arctic':0,'gwp20_other':0,'co2_nsr':0,'co2_scr':0},
    }

# SOx Emission
sox_label = tk.Label(lf_cap, text='SOx *', font=("Helvetica", 8, 'bold'))
sox_label.grid(column=0,row=1)
Pmw.Balloon(lf_cap).bind(sox_label,cap_dict['SOx']['balloon'])
sox_emission = tk.DoubleVar()
sox_emission_entry = ttk.Entry(lf_cap, textvariable=sox_emission)
sox_emission_entry.grid(column=1, row=1, sticky=tk.W, padx=10, pady=5)

# NOx Emission
nox_label = tk.Label(lf_cap, text='NOx *', font=("Helvetica", 8, 'bold'))
nox_label.grid(column=0,row=2)
Pmw.Balloon(lf_cap).bind(nox_label,cap_dict['NOx']['balloon'])
nox_emission = tk.DoubleVar()
nox_emission_entry = ttk.Entry(lf_cap, textvariable=nox_emission)
nox_emission_entry.grid(column=1, row=2, sticky=tk.W, padx=10, pady=5)

# NMVOC Emission
nmvoc_label = tk.Label(lf_cap, text='NMVOC *', font=("Helvetica", 8, 'bold'))
nmvoc_label.grid(column=0,row=3)
Pmw.Balloon(lf_cap).bind(nmvoc_label,cap_dict['NMVOC']['balloon'])
nmvoc_emission = tk.DoubleVar()
nmvoc_emission_entry = ttk.Entry(lf_cap, textvariable=nmvoc_emission)
nmvoc_emission_entry.grid(column=1, row=3, sticky=tk.W, padx=10, pady=5)

# PM25 Emission
pm25_label = tk.Label(lf_cap, text='PM 2.5 *', font=("Helvetica", 8, 'bold'))
pm25_label.grid(column=0,row=4)
Pmw.Balloon(lf_cap).bind(pm25_label,cap_dict['PM25']['balloon'])
pm25_emission = tk.DoubleVar()
pm25_emission_entry = ttk.Entry(lf_cap, textvariable=pm25_emission)
pm25_emission_entry.grid(column=1, row=4, sticky=tk.W, padx=10, pady=5)

# SOx Pollution Cost
sox_pollution_cost = tk.DoubleVar()
sox_pollution_cost_entry = ttk.Entry(lf_cap, textvariable=sox_pollution_cost)
sox_pollution_cost_entry.grid(column=2, row=1, sticky=tk.W, padx=10, pady=5)

# NOx Pollution Cost
nox_pollution_cost = tk.DoubleVar()
nox_pollution_cost_entry = ttk.Entry(lf_cap, textvariable=nox_pollution_cost)
nox_pollution_cost_entry.grid(column=2, row=2, sticky=tk.W, padx=10, pady=5)

# NMVOC Pollution Cost
nmvoc_pollution_cost = tk.DoubleVar()
nmvoc_pollution_cost_entry = ttk.Entry(lf_cap, textvariable=nmvoc_pollution_cost)
nmvoc_pollution_cost_entry.grid(column=2, row=3, sticky=tk.W, padx=10, pady=5)

# PM25 Pollution Cost
pm25_pollution_cost = tk.DoubleVar()
pm25_pollution_cost_entry = ttk.Entry(lf_cap, textvariable=pm25_pollution_cost)
pm25_pollution_cost_entry.grid(column=2, row=4, sticky=tk.W, padx=10, pady=5)

# Total Air Pollution Cost
air_pollution_cost_label = tk.Label(lf_cap, text='Total Air Pollution Cost in this voyage (USD):', font=("Helvetica", 10))
air_pollution_cost_label.grid(column=3,row=3, columnspan=2)
air_pollution_cost = tk.DoubleVar()
air_pollution_cost_entry = ttk.Entry(lf_cap, textvariable=air_pollution_cost)
air_pollution_cost_entry.grid(column=4, row=4, sticky=tk.W, padx=5)

### trace
air_pollution_cost.trace('w', callbackCost)

########################################################################################## Cost of Global Warming ################################################################################
# create label frame
lf_cgw = ttk.LabelFrame(tab_environment, text="Cost of Global Warming (CGW)")
lf_cgw.grid(column=1, row=1, padx=10, pady=10)

# label pollutant
label_pollutant = ttk.Label(lf_cgw,text='Pollutant',font=("Helvetica", 10, 'bold'))
label_pollutant.grid(column=0, row=0, padx=10, pady=10)

# label Emmision Factor
label_emission_factor = ttk.Label(lf_cgw,text='Emission Factor (Kg/t) *',font=("Helvetica", 10, 'bold'))
label_emission_factor.grid(column=1, row=0, padx=10, pady=10)
Pmw.Balloon(lf_cgw).bind(label_emission_factor,'(Kg emmited / tone of fuel)')

# label Pollution Cost
label_pollution_cost = ttk.Label(lf_cgw,text='Pollution Cost (USD/t)',font=("Helvetica", 10, 'bold'))
label_pollution_cost.grid(column=2, row=0, padx=10, pady=10)

# CO2 Emission
co2_label = tk.Label(lf_cgw, text='CO2 *', font=("Helvetica", 8, 'bold'))
co2_label.grid(column=0,row=1, padx=10, pady=5)
Pmw.Balloon(lf_cgw).bind(co2_label,cap_dict['CO2']['balloon'])
co2_emission = tk.DoubleVar()
co2_emission_entry = ttk.Entry(lf_cgw, textvariable=co2_emission)
co2_emission_entry.grid(column=1, row=1, sticky=tk.W, padx=10, pady=5)

# CO Emission
co_label = tk.Label(lf_cgw, text='CO *', font=("Helvetica", 8, 'bold'))
co_label.grid(column=0,row=2, padx=10, pady=5)
Pmw.Balloon(lf_cgw).bind(co_label,cap_dict['CO']['balloon'])
co_emission = tk.DoubleVar()
co_emission_entry = ttk.Entry(lf_cgw, textvariable=co_emission)
co_emission_entry.grid(column=1, row=2, sticky=tk.W, padx=10, pady=5)

# N2O Emission
n2o_label = tk.Label(lf_cgw, text='N2O *', font=("Helvetica", 8, 'bold'))
n2o_label.grid(column=0,row=3, padx=10, pady=5)
Pmw.Balloon(lf_cgw).bind(n2o_label,cap_dict['N2O']['balloon'])
n2o_emission = tk.DoubleVar()
n2o_emission_entry = ttk.Entry(lf_cgw, textvariable=n2o_emission)
n2o_emission_entry.grid(column=1, row=3, sticky=tk.W, padx=10, pady=5)

# CH4 Emission
ch4_label = tk.Label(lf_cgw, text='CH4 *', font=("Helvetica", 8, 'bold'))
ch4_label.grid(column=0,row=4, padx=10, pady=5)
Pmw.Balloon(lf_cgw).bind(ch4_label,cap_dict['CH4']['balloon'])
ch4_emission = tk.DoubleVar()
ch4_emission_entry = ttk.Entry(lf_cgw, textvariable=ch4_emission)
ch4_emission_entry.grid(column=1, row=4, sticky=tk.W, padx=10, pady=5)

# BC Emission
bc_label = tk.Label(lf_cgw, text='BC *', font=("Helvetica", 8, 'bold'))
bc_label.grid(column=0,row=5, padx=10, pady=5)
Pmw.Balloon(lf_cgw).bind(bc_label,cap_dict['BC']['balloon'])
bc_emission = tk.DoubleVar()
bc_emission_entry = ttk.Entry(lf_cgw, textvariable=bc_emission)
bc_emission_entry.grid(column=1, row=5, sticky=tk.W, padx=10, pady=5)

# CO2 Global Warming Cost
co2_pollution_cost = tk.DoubleVar()
co2_pollution_cost_entry = ttk.Entry(lf_cgw, textvariable=co2_pollution_cost)
co2_pollution_cost_entry.grid(column=2, row=1, sticky=tk.W, padx=10, pady=5)

# CO Global Warming Cost
co_pollution_cost = tk.DoubleVar()
co_pollution_cost_entry = ttk.Entry(lf_cgw, textvariable=co_pollution_cost)
co_pollution_cost_entry.grid(column=2, row=2, sticky=tk.W, padx=10, pady=5)

# N2O Global Warming Cost
n2o_pollution_cost = tk.DoubleVar()
n2o_pollution_cost_entry = ttk.Entry(lf_cgw, textvariable=n2o_pollution_cost)
n2o_pollution_cost_entry.grid(column=2, row=3, sticky=tk.W, padx=10, pady=5)

# CH4 Global Warming Cost
ch4_pollution_cost = tk.DoubleVar()
ch4_pollution_cost_entry = ttk.Entry(lf_cgw, textvariable=ch4_pollution_cost)
ch4_pollution_cost_entry.grid(column=2, row=4, sticky=tk.W, padx=10, pady=5)

# BC Global Warming Cost
bc_pollution_cost = tk.DoubleVar()
bc_pollution_cost_entry = ttk.Entry(lf_cgw, textvariable=bc_pollution_cost)
bc_pollution_cost_entry.grid(column=2, row=5, sticky=tk.W, padx=10, pady=5)

# Total Global Warming Cost
global_warming_cost_label = tk.Label(lf_cgw, text='Total Global Warming Cost in this voyage (USD):', font=("Helvetica", 9))
global_warming_cost_label.grid(column=3,row=4, columnspan=2)
global_warming_cost = tk.DoubleVar()
global_warming_cost_entry = ttk.Entry(lf_cgw, textvariable=global_warming_cost)
global_warming_cost_entry.grid(column=4, row=5, sticky=tk.W, padx=5)

### trace
global_warming_cost.trace('w', callbackCost)

def environmentalCost():

    # Air Pollution Cost
    sox_cost_var = sox_emission.get() * sox_pollution_cost.get() * total_fuel_consumption.get() * 0.000001
    nox_emission_var = nox_emission.get() * nox_pollution_cost.get() * total_fuel_consumption.get() * 0.000001
    nmvoc_emission_var = nmvoc_emission.get() *  nmvoc_pollution_cost.get() * total_fuel_consumption.get() * 0.000001
    pm25_emission_var = pm25_emission.get() * pm25_pollution_cost.get() * total_fuel_consumption.get() * 0.000001

    total_air_pollution_cost_var = (sox_cost_var + nox_emission_var + nmvoc_emission_var + pm25_emission_var) / teu.get()
    air_pollution_cost.set(int(total_air_pollution_cost_var))

    # Global Warming Cost
    co2_cost_var = co2_emission.get() * co2_pollution_cost.get() * total_fuel_consumption.get() * 100 * 0.001
    co_cost_var = co_emission.get() * co_pollution_cost.get() * total_fuel_consumption.get() * 100 * 0.001
    n2o_cost_var = n2o_emission.get() * n2o_pollution_cost.get() * total_fuel_consumption.get() * 100 * 0.001
    ch4_cost_var = ch4_emission.get() * ch4_pollution_cost.get() * total_fuel_consumption.get() * 100 * 0.001
    bc_cost_var = bc_emission.get() * bc_pollution_cost.get() * total_fuel_consumption.get() * 100 * 0.001

    total_global_warming_cost_var = (co2_cost_var + co_cost_var + n2o_cost_var + ch4_cost_var + bc_cost_var) / teu.get()
    global_warming_cost.set(int(total_global_warming_cost_var))

########################################################################################## Button ##########################################################################################

environmental_cost_button = ttk.Button(tab_environment, text="Calculate Environmental Cost", command=lambda: environmentalCost())
environmental_cost_button.grid(column=1,row=2, pady=20, ipadx=5, ipady=5)

#################################################################################################################################################################################################
########################################################################################## Cost Tab #############################################################################################

#################################################################################################################################################################################################
########################################################################################## Port Dues ##########################################################################################
# center columns
tab_cost.columnconfigure(0,weight=1)
tab_cost.columnconfigure(4,weight=1)

# create label frame
lf_port_dues = ttk.LabelFrame(tab_cost, text="Port Dues")
lf_port_dues.grid(column=1,row=0, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW, columnspan=3)

# Label Desription
ttk.Label(lf_port_dues, text="16- Here you can define port fees based on the gross tonnage (GT):", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=6, ipady=5)

# Label coefficient Port Dues
coefficient_port_dues_label = ttk.Label(lf_port_dues, text="Coefficient: ")
coefficient_port_dues_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
# Entry coefficient Port Dues
coefficient_port_dues = tk.DoubleVar()
coefficient_port_dues_entry = ttk.Entry(lf_port_dues, textvariable = coefficient_port_dues)
coefficient_port_dues_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

### trace
coefficient_port_dues.trace('w', callbackCost)

# Gross Tonnage for port dues cost
gross_label_port = ttk.Label(lf_port_dues, text="Gross Tonnage (ton): ")
gross_label_port.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)
gross_entry_port = ttk.Entry(lf_port_dues, textvariable=gross)
gross_entry_port.grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)

# Label Port Dues
port_dues_label = ttk.Label(lf_port_dues, text="Port Dues Cost (USD): ")
port_dues_label.grid(column=4, row=1, sticky=tk.W, padx=5, pady=5)
# Entry Port Dues
port_dues = tk.IntVar()
port_dues_entry = ttk.Entry(lf_port_dues, textvariable = port_dues)
port_dues_entry.config(state=DISABLED)
port_dues_entry.grid(column=5, row=1, sticky=tk.W, padx=5, pady=5)
########################################################################################## Insurance Piracy ##########################################################################################
# create label frame
lf_piracy_insurance = ttk.LabelFrame(tab_cost, text="Piracy Insurance")
lf_piracy_insurance.grid(column=1,row=1, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW, columnspan=3)

# Label Desription
ttk.Label(lf_piracy_insurance, text="17- Here you can define the Annual Piracy Insurance cost based on the given paramterers:", foreground='red').grid(column=0,row=0, sticky=tk.W, pady=5, columnspan=6)

# Label piracy insurance Coefficient
piracy_parameter_label = ttk.Label(lf_piracy_insurance, text="")
piracy_parameter_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
# Label piracy insurance Coefficient
piracy_coefficient = tk.DoubleVar()
piracy_coefficient_entry = ttk.Entry(lf_piracy_insurance, textvariable = piracy_coefficient)
piracy_coefficient_entry.grid(column=1, row=1, sticky=tk.W, padx=5, pady=5)

### trace
piracy_coefficient.trace('w', callbackCost)

# Piracy Parameter Insurance
gross_label_insurance = ttk.Label(lf_piracy_insurance, text="")
gross_label_insurance.grid(column=2, row=1, sticky=tk.W, padx=5, pady=5)
parameter_insurance = tk.IntVar()
parameter_insurance_entry = ttk.Entry(lf_piracy_insurance, textvariable=parameter_insurance)
#gross_entry.config(state=DISABLED)
parameter_insurance_entry.grid(column=3, row=1, sticky=tk.W, padx=5, pady=5)

# Label Piracy Insurance Cost
piracy_insurance_cost_label = ttk.Label(lf_piracy_insurance, text="Piracy Insurance Cost \nfor this voyage (USD): ")
piracy_insurance_cost_label.grid(column=4, row=1, sticky=tk.W, padx=5, pady=5)
# Entry Piracy Insurance Cost
piracy_insurance_cost = tk.DoubleVar()
piracy_insurance_cost_entry = ttk.Entry(lf_piracy_insurance, textvariable = piracy_insurance_cost)
piracy_insurance_cost_entry.grid(column=5, row=1, sticky=tk.W, padx=5, pady=5)
piracy_insurance_cost_entry.config(state=DISABLED)
piracy_insurance_cost.trace('w', callbackCost)

########################################################################################## Cargo Insurance in this voyage ######################################################################################
# create label frame
lf_cargo_insurance = ttk.LabelFrame(tab_cost, text="Cargo Insurance")
lf_cargo_insurance.grid(column=1,row=2, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW)
lf_cargo_insurance.columnconfigure(0,weight=1)
lf_cargo_insurance.columnconfigure(1,weight=1)

# label cargo insurance cost
cargo_insurance_cost_label = ttk.Label(lf_cargo_insurance, text="Corgo Insurance Cost in this voyage (Million Dollar): ")
cargo_insurance_cost_label.grid(column=0, row=0, sticky=tk.NSEW,padx=5, pady=5)
cargo_insurance_cost_voyage_entry = ttk.Entry(lf_cargo_insurance, textvariable=cargo_insurance_cost)
cargo_insurance_cost_voyage_entry.grid(column=1, row=0, sticky=tk.E,padx=5, pady=5)
cargo_insurance_cost_voyage_entry.config(state=DISABLED)

########################################################################################## Salary tab cost ##########################################################################################
# create label frame
lf_salary = ttk.LabelFrame(tab_cost, text="Salary")
lf_salary.grid(column=1,row=3, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW)
lf_salary.columnconfigure(0,weight=1)
lf_salary.columnconfigure(1,weight=1)

# Label Salary voyage
gross_label_salary = ttk.Label(lf_salary, text="Salary for this voyage (USD):")
gross_label_salary.grid(column=0, row=0, sticky=tk.W,padx=5, pady=5)

# Entry Salary
salary_voyage = tk.IntVar()
salary_voyage_entry = ttk.Entry(lf_salary, textvariable=salary_voyage)
salary_voyage_entry.grid(column=1, row=0, sticky=tk.E,padx=5, pady=5)
salary_voyage_entry.config(state=DISABLED)

########################################################################################## Environmental Cost ##########################################################################################
# create label frame
lf_environmental_cost = ttk.LabelFrame(tab_cost, text="Environmental Cost")
lf_environmental_cost.grid(column=1,row=4, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW)
lf_environmental_cost.columnconfigure(0,weight=1)
lf_environmental_cost.columnconfigure(1,weight=1)

# Label Environmental Cost
environmental_cost_label = ttk.Label(lf_environmental_cost, text="Environmental Cost (USD): ")
environmental_cost_label.grid(column=0, row=0, sticky=tk.W,padx=5, pady=5)
# Entry Environmental Cost
total_environmental_cost = tk.IntVar()
environmental_cost_entry = ttk.Entry(lf_environmental_cost, textvariable=total_environmental_cost)
environmental_cost_entry.grid(column=1, row=0, sticky=tk.E,padx=5, pady=5)
environmental_cost_entry.config(state=DISABLED)

########################################################################################## Fuel Cost ##########################################################################################
# create label frame
lf_fuel_cost = ttk.LabelFrame(tab_cost, text="Fuel Cost")
lf_fuel_cost.grid(column=1,row=5, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW)
lf_fuel_cost.columnconfigure(0,weight=1)
lf_fuel_cost.columnconfigure(1,weight=1)

# Label Total Fuel Consumption price
total_fuel_consumption_cost_label = ttk.Label(lf_fuel_cost, text="Total Fuel Price in this Voyage (USD): ")
total_fuel_consumption_cost_label.grid(column=0, row=0, sticky=tk.W,padx=5, pady=5)
# Entry Total Fuel Consumption Price
total_fuel_consumption_cost_entry = ttk.Entry(lf_fuel_cost, textvariable=total_fuel_consumption_cost)
total_fuel_consumption_cost_entry.grid(column=1, row=0, sticky=tk.E,padx=5, pady=5)
total_fuel_consumption_cost_entry.config(state=DISABLED)

############################################################################ Annual Capital Cost and Depreciation of Vessel for this voyage ##########################################################################################
# create label frame
lf_capital_cost = ttk.LabelFrame(tab_cost, text="Annual Capital Cost and Depreciation of Vessel")
lf_capital_cost.grid(column=1,row=6, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW)
lf_capital_cost.columnconfigure(0,weight=1)
lf_capital_cost.columnconfigure(1,weight=1)

# Label Annual Capital Cost
annual_capital_cost_label = ttk.Label(lf_capital_cost, text="Annual Capital Cost & Depreciation (USD): ")
annual_capital_cost_label.grid(column=0, row=0, sticky=tk.W,padx=5, pady=5)
# Entry Annual Capital Cost
voyage_capital_cost = tk.DoubleVar()
voyage_capital_cost_entry = ttk.Entry(lf_capital_cost, textvariable = voyage_capital_cost)
voyage_capital_cost_entry.grid(column=1, row=0, sticky=tk.E,padx=5, pady=5)
voyage_capital_cost_entry.config(state=DISABLED)

########################################################################################## Repair and Services cost in this voyage ##########################################################################################
# create label frame
lf_repair_service = ttk.LabelFrame(tab_cost, text="Repair and Services Cost")
lf_repair_service.grid(column=1,row=7, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW)
lf_repair_service.columnconfigure(0,weight=1)
lf_repair_service.columnconfigure(1,weight=1)

# Repair and Services Cost in this voyage
repair_service_vayage = tk.DoubleVar()
repair_service_vayage_label = ttk.Label(lf_repair_service, text="Cost of Repair & Services in this voyage (USD): ")
repair_service_vayage_label.grid(column=0, row=0, sticky=tk.W,padx=5, pady=5)
repair_service_vayage_entry= ttk.Entry(lf_repair_service, textvariable = repair_service_vayage)
repair_service_vayage_entry.grid(column=1, row=0, sticky=tk.E,padx=5, pady=5)
repair_service_vayage_entry.config(state=DISABLED)

########################################################################################## Insurance Vessel Structure voyage ##########################################################################################
# create label frame
lf_insurance = ttk.LabelFrame(tab_cost, text="Vessel Instructure Insurance")
lf_insurance.grid(column=1,row=8, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.EW)
lf_insurance.columnconfigure(0,weight=1)
lf_insurance.columnconfigure(1,weight=1)

# Label Annual Insurance Cost
annual_insurance_cost_label = ttk.Label(lf_insurance, text="Vessel instructure Insurance Cost in this voyage (USD): ")
annual_insurance_cost_label.grid(column=0, row=0, sticky=tk.W,padx=5, pady=5)
# Entry Annual Insurance Cost
voyage_insurance_cost = tk.DoubleVar()
voyage_insurance_cost_entry = ttk.Entry(lf_insurance, textvariable = voyage_insurance_cost)
voyage_insurance_cost_entry.grid(column=1, row=0, sticky=tk.E,padx=5, pady=5)
voyage_insurance_cost_entry.config(state=DISABLED)

########################################################################################## Total Cost ##########################################################################################
# create label frame
lf_total_cost = ttk.LabelFrame(tab_cost, text="Total Cost")
lf_total_cost.grid(column=1,row=9, padx=5, pady=2, ipady=10, ipadx=8, columnspan=3)

# Label Total Cost
total_cost_label = ttk.Label(lf_total_cost, text="Total Cost for this voyage (Million USD): ", foreground='blue')
total_cost_label.grid(column=0, row=0, sticky=tk.W,padx=5, pady=15)
# Entry Total Cost
total_cost = tk.DoubleVar()
total_cost_entry = ttk.Entry(lf_total_cost, textvariable=total_cost)
total_cost_entry.grid(column=1, row=0, sticky=tk.W,padx=5, pady=15)
total_cost_entry.config(state=DISABLED)

########################################################################################## Button for Pie Chart ##########################################################################################
pie_chart = ttk.Button(tab_cost, text="Show on the Pie Chart", command=lambda: pieChart())
pie_chart.grid(column=1,row=10, pady=15, ipadx=5, ipady=5, columnspan=3)
########################################################################################## Pie Chart for the cost ##########################################################################################
# create label frame
lf_pie_chart_cost = ttk.LabelFrame(tab_cost, text="Total Cost")
lf_pie_chart_cost.grid(column=1,row=6, padx=5, pady=2, ipady=2, ipadx=2, sticky=tk.W, rowspan=5)

def pieChart():
    newWindow = Toplevel(root)
 
    # sets the title of the
    # Toplevel widget
    newWindow.title("Total Cost On Pie Chart")
 
    # sets the geometry of toplevel
    newWindow.geometry("800x800")
 
    fig = matplotlib.figure.Figure(figsize=(8,8), dpi=100) 
    ax = fig.add_subplot(111)
    explode = (0.2, 0.1, 0.3, 0.1, 0.25, 0.3, 0.25, 0.35, 0.25)
    labels = ['Environmental', 'Fuel','Cargo Insurance', 'Piracy Insurance', 'Repair & Services','Capital Cost', 'Vessel Insurance', 'Salary', 'Port Fees']
    pieSizes = [total_environmental_cost.get(), total_fuel_consumption_cost.get(), (cargo_insurance_cost.get() * 1000000), piracy_insurance_cost.get(), repair_service_vayage.get(), voyage_capital_cost.get(),
    voyage_insurance_cost.get(), salary_voyage.get(), port_dues.get()]

    colors = ['lightblue','lightsteelblue','silver',"orange", "cyan", "brown","grey", "indigo", "beige"]
    patches = ax.pie(pieSizes, colors=colors, explode=explode, labels=labels, autopct='%1.1f%%')
    ax.axis('equal')
    
    #ax.legend(patches, labels,loc ="best")

    canvas = FigureCanvasTkAgg(fig, newWindow)
    canvas.get_tk_widget().pack()
    canvas.draw()



#################################################################################################################################################################################################
########################################################################################## Functions #############################################################################################
#################################################################################################################################################################################################

##################################################################################### Selected Route Function ###################################################################################

def selectedRoute(*args,**kwargs):
 
    for key,value in kwargs.items():
        if key == 'route' and value == 'NSR':
            # Emission Pollution Factor
            sox_emission_entry.delete(0, END)
            sox_emission_entry.insert(0,cap_dict['SOx']['emission'])
            nox_emission_entry.delete(0, END)
            nox_emission_entry.insert(0,cap_dict['NOx']['emission'])
            nmvoc_emission_entry.delete(0, END)
            nmvoc_emission_entry.insert(0,cap_dict['NMVOC']['emission'])
            pm25_emission_entry.delete(0, END)
            pm25_emission_entry.insert(0,cap_dict['PM25']['emission'])
            # Pollution Cost
            sox_pollution_cost_entry.delete(0, END)
            sox_pollution_cost_entry.insert(0,cap_dict['SOx']['nsr_cost'])
            nox_pollution_cost_entry.delete(0, END)
            nox_pollution_cost_entry.insert(0,cap_dict['NOx']['nsr_cost'])
            nmvoc_pollution_cost_entry.delete(0, END)
            nmvoc_pollution_cost_entry.insert(0,cap_dict['NMVOC']['nsr_cost'])
            pm25_pollution_cost_entry.delete(0, END)
            pm25_pollution_cost_entry.insert(0,cap_dict['PM25']['nsr_cost'])
            # Global Warming Pollution Factor
            co2_emission_entry.delete(0, END)
            co2_emission_entry.insert(0,cap_dict['CO2']['emission'])
            co_emission_entry.delete(0, END)
            co_emission_entry.insert(0,cap_dict['CO']['emission'])
            n2o_emission_entry.delete(0, END)
            n2o_emission_entry.insert(0,cap_dict['N2O']['emission'])
            ch4_emission_entry.delete(0, END)
            ch4_emission_entry.insert(0,cap_dict['CH4']['emission'])
            bc_emission_entry.delete(0, END)
            bc_emission_entry.insert(0,cap_dict['BC']['emission'])
            # Global Warming Cost
            co2_pollution_cost_entry.delete(0, END)
            co2_pollution_cost_entry.insert(0,cap_dict['CO2']['gwp20_arctic'])
            co_pollution_cost_entry.delete(0, END)
            co_pollution_cost_entry.insert(0,cap_dict['CO']['gwp20_arctic'])
            n2o_pollution_cost_entry.delete(0, END)
            n2o_pollution_cost_entry.insert(0,cap_dict['N2O']['gwp20_arctic'])
            ch4_pollution_cost_entry.delete(0, END)
            ch4_pollution_cost_entry.insert(0,cap_dict['CH4']['gwp20_arctic'])
            bc_pollution_cost_entry.delete(0, END)
            bc_pollution_cost_entry.insert(0,cap_dict['BC']['gwp20_arctic'])

            # Insurance Label
            piracy_parameter_label.config(text='USD/GT/Year: ')
            gross_label_insurance.config(text='Gross Tonnage (ton): ')

            # Insurance Piracy
            piracy_coefficient_entry.delete(0, END)
            piracy_coefficient_entry.insert(0,10)

            # Port distance nm NSR
            #real_distance_nm_entry.config(state=ACTIVE)
            real_distance_nm_entry.delete(0, END)
            dis_nm_nsr = distances_array_nsr[int(args[0]), int(args[1])]
            real_distance_nm_entry.insert(0,dis_nm_nsr)
            #real_distance_nm_entry.config(state=DISABLED)

            # Port distance Km NSR
            real_distance_km_entry.config(state=ACTIVE)
            real_distance_km_entry.delete(0, END)
            real_distance_km_entry.insert(0,round(dis_nm_nsr * 1.852, 3))
            real_distance_km_entry.config(state=DISABLED)

            # Average Shipping Speed Knots
            average_speed_knots_entry.delete(0, END)
            average_speed_knots_entry.insert(0,20)

            # Average Shipping Speed Km per hour
            average_speed_kph_entry.config(state=ACTIVE)
            average_speed_kph_entry.delete(0, END)
            average_speed_kph_entry.insert(0, round(20 * 1.852, 3))
            average_speed_kph_entry.config(state=DISABLED)

            # Wind Probability for risk
            wind_mean_risk_entry.delete(0, END)
            wind_mean_risk_entry.insert(0, 17.5)
            wind_std_risk_entry.delete(0, END)
            wind_std_risk_entry.insert(0, 0.2)

            # Weather Probability for Risk tab
            weather_mean_risk_entry.delete(0, END)
            weather_mean_risk_entry.insert(0,0.03)
            weather_std_risk_entry.delete(0, END)
            weather_std_risk_entry.insert(0,0.001)

            # Fuel Price
            fuel_1.config(value=460)
            fuel_2.config(value=680)
            fuel_3.config(value=595)
            fuel_4.config(value=598)
            fuel_5.config(value=0)

        
        elif key == 'route' and value == 'SCR':
            sox_emission_entry.delete(0, END)
            sox_emission_entry.insert(0,cap_dict['SOx']['emission'])
            nox_emission_entry.delete(0, END)
            nox_emission_entry.insert(0,cap_dict['NOx']['emission'])
            nmvoc_emission_entry.delete(0, END)
            nmvoc_emission_entry.insert(0,cap_dict['NMVOC']['emission'])
            pm25_emission_entry.delete(0, END)
            pm25_emission_entry.insert(0,cap_dict['PM25']['emission'])
            # Pollution Cost
            sox_pollution_cost_entry.delete(0, END)
            sox_pollution_cost_entry.insert(0,cap_dict['SOx']['scr_cost'])
            nox_pollution_cost_entry.delete(0, END)
            nox_pollution_cost_entry.insert(0,cap_dict['NOx']['scr_cost'])
            nmvoc_pollution_cost_entry.delete(0, END)
            nmvoc_pollution_cost_entry.insert(0,cap_dict['NMVOC']['scr_cost'])
            pm25_pollution_cost_entry.delete(0, END)
            pm25_pollution_cost_entry.insert(0,cap_dict['PM25']['scr_cost'])
            # Global Warming Pollution Factor
            co2_emission_entry.delete(0, END)
            co2_emission_entry.insert(0,cap_dict['CO2']['emission'])
            co_emission_entry.delete(0, END)
            co_emission_entry.insert(0,cap_dict['CO']['emission'])
            n2o_emission_entry.delete(0, END)
            n2o_emission_entry.insert(0,cap_dict['N2O']['emission'])
            ch4_emission_entry.delete(0, END)
            ch4_emission_entry.insert(0,cap_dict['CH4']['emission'])
            bc_emission_entry.delete(0, END)
            bc_emission_entry.insert(0,cap_dict['BC']['emission'])
            # Global Warming Cost
            co2_pollution_cost_entry.delete(0, END)
            co2_pollution_cost_entry.insert(0,cap_dict['CO2']['gwp20_other'])
            co_pollution_cost_entry.delete(0, END)
            co_pollution_cost_entry.insert(0,cap_dict['CO']['gwp20_other'])
            n2o_pollution_cost_entry.delete(0, END)
            n2o_pollution_cost_entry.insert(0,cap_dict['N2O']['gwp20_other'])
            ch4_pollution_cost_entry.delete(0, END)
            ch4_pollution_cost_entry.insert(0,cap_dict['CH4']['gwp20_other'])
            bc_pollution_cost_entry.delete(0, END)
            bc_pollution_cost_entry.insert(0,cap_dict['BC']['gwp20_other'])

            # Insurance Label
            piracy_parameter_label.config(text='USD/TEU/Year: ')
            gross_label_insurance.config(text='TEU: ')

            # Insurance Piracy
            piracy_coefficient_entry.delete(0, END)
            piracy_coefficient_entry.insert(0,40)

            # Port distance nm SCR
            real_distance_nm_entry.delete(0, END)
            dis_nm_scr = distances_array_scr[int(args[0]), int(args[1])]
            real_distance_nm_entry.insert(0,dis_nm_scr)

            # Port distance Km SCR
            real_distance_km_entry.config(state=ACTIVE)
            real_distance_km_entry.delete(0, END)
            real_distance_km_entry.insert(0, round(dis_nm_scr*1.852, 3))
            real_distance_km_entry.config(state=DISABLED)

            # Average Shipping Speed knots
            average_speed_knots_entry.delete(0, END)
            average_speed_knots_entry.insert(0,20)

            # Average Shipping Speed Km per hour
            average_speed_kph_entry.config(state=ACTIVE)
            average_speed_kph_entry.delete(0, END)
            average_speed_kph_entry.insert(0, round(15 * 1.852, 3))
            average_speed_kph_entry.config(state=DISABLED)

            # Wind Probability for risk
            wind_mean_risk_entry.delete(0, END)
            wind_mean_risk_entry.insert(0, 18.0)
            wind_std_risk_entry.delete(0, END)
            wind_std_risk_entry.insert(0, 0.25)

            # Weather Probability for Risk tab
            weather_mean_risk_entry.delete(0, END)
            weather_mean_risk_entry.insert(0,0.02)
            weather_std_risk_entry.delete(0, END)
            weather_std_risk_entry.insert(0,0.001)

            # Fuel Price
            fuel_1.config(value=460)
            fuel_2.config(value=690)
            fuel_3.config(value=595)
            fuel_4.config(value=598)
            fuel_5.config(value=578)

    # calculate shipping time to days
    shipping_time_entry.config(state=ACTIVE)
    shipping_time_entry.delete(0, END)
    shipping_time_entry.insert(0, round(real_distance_nm.get() / average_speed_knots.get() / 24, 3))
    shipping_time_entry.config(state=DISABLED)

    # port dues coefficient
    coefficient_port_dues_entry.delete(0, END)
    coefficient_port_dues_entry.insert(0, 0.428)

    # Simulation Parameters for risk
    random_number_entry.delete(0, END)
    random_number_entry.insert(0, 10000)

##################################################################################### Selected Route Function ###################################################################################

vessels_dict={
    'Al Dahna':{'teu_entry':19870,'length_entry':400,'beam_entry':58,'dwt_entry':199744,'gross_entry':195636,'nominal_speed_entry':20.9,'engine_power_entry':41800,'built_year_entry':2016,'capital_cost_entry':185,
    'fuel_tank_capacity_entry':1.25,'fuel_consumption_entry':49516.92308,'crew_entry':22,'fuel_hfo':45888.9505,'fuel_vlsfo':49516.92308,'fuel_hfo':53892.83721,'fuel_ulsfo':58668.1519},
    'Afif':{'teu_entry':14993,'length_entry':368,'beam_entry':51,'dwt_entry':149360,'gross_entry':153148,'nominal_speed_entry':21.2,'engine_power_entry':37620,'built_year_entry':2017,'capital_cost_entry':159.4,
    'fuel_tank_capacity_entry':1.2,'fuel_consumption_entry':44565.23,'crew_entry':22,'fuel_hfo':41300.05,'fuel_vlsfo':44565.23,'fuel_hfo':48503.55,'fuel_ulsfo':52801.33},
    'Ain Snan':{'teu_entry':13500,'length_entry':366,'beam_entry':51,'dwt_entry':145528,'gross_entry':141077,'nominal_speed_entry':25.23,'engine_power_entry':71770,'built_year_entry':2011,'capital_cost_entry':135,
    'fuel_tank_capacity_entry':1,'fuel_consumption_entry':85019.85,'crew_entry':22,'fuel_hfo':78790.66,'fuel_vlsfo':85019.85,'fuel_hfo':92533.23,'fuel_ulsfo':100732.37},
    'Cartagena Express':{'teu_entry':11519,'length_entry':333,'beam_entry':48,'dwt_entry':123587,'gross_entry':118945,'nominal_speed_entry':21,'engine_power_entry':34224,'built_year_entry':2017,
    'capital_cost_entry':122.5,'fuel_tank_capacity_entry':0.9,'fuel_consumption_entry':40542.28,'crew_entry':22,'fuel_hfo':37571.85,'fuel_vlsfo':40542.28,'fuel_hfo':44125.08,'fuel_ulsfo':48034.9},
    'Chicago Express':{'teu_entry':8600,'length_entry':335,'beam_entry':42,'dwt_entry':103994,'gross_entry':93750,'nominal_speed_entry':23.5,'engine_power_entry':51480,'built_year_entry':2010,
    'capital_cost_entry':87.9,'fuel_tank_capacity_entry':0.8,'fuel_consumption_entry':60984.0,'crew_entry':22,'fuel_hfo':56515.86,'fuel_vlsfo':60984,'fuel_hfo':66373.28,'fuel_ulsfo':72254.46},
    'Palena':{'teu_entry':6541,'length_entry':304,'beam_entry':40,'dwt_entry':81112,'gross_entry':73934,'nominal_speed_entry':24.7,'engine_power_entry':60200,'built_year_entry':2006,'capital_cost_entry':68.3,
    'fuel_tank_capacity_entry':0.65,'fuel_consumption_entry':5388.92,'crew_entry':22,'fuel_hfo':69865.38,'fuel_vlsfo':5388.92,'fuel_hfo':82051.2,'fuel_ulsfo':89321.56},
    'Rotterdam Express':{'teu_entry':4890,'length_entry':294,'beam_entry':32,'dwt_entry':66975,'gross_entry':54465,'nominal_speed_entry':21.5,'engine_power_entry':28600,'built_year_entry':2000,
    'capital_cost_entry':4.7,'fuel_tank_capacity_entry':0.45,'fuel_consumption_entry':35816.0,'crew_entry':22,'fuel_hfo':33191.86,'fuel_vlsfo':35816,'fuel_hfo':38981.13,'fuel_ulsfo':42435.16},
    'new':{'teu_entry':0,'length_entry':0,'beam_entry':0,'dwt_entry':0,'gross_entry':0,'nominal_speed_entry':0,'engine_power_entry':0,'built_year_entry':0,'capital_cost_entry':0,'fuel_tank_capacity_entry':0,
    'fuel_consumption_entry':0,'crew_entry':0}
}           

# Vessel Function
def vesselSelection(vessel): 
    vessel_properties = [teu_entry, length_entry, beam_entry, dwt_entry, gross_entry, nominal_speed_entry, engine_power_entry, built_year_entry, capital_cost_entry, fuel_tank_capacity_entry, fuel_consumption_entry, crew_entry]
    vessel_properties_str = ['teu_entry', 'length_entry', 'beam_entry', 'dwt_entry', 'gross_entry', 'nominal_speed_entry', 'engine_power_entry', 'built_year_entry', 'capital_cost_entry', 'fuel_tank_capacity_entry', 'fuel_consumption_entry', 'crew_entry']
    for i in range(len(vessel_properties)):
        if vessel == 'new':
            vessel_properties[i].config(state=ACTIVE)
            vessel_properties[i].delete(0, END)            
        else:
            vessel_properties[i].config(state=ACTIVE)
            vessel_properties[i].delete(0, END)
            vessel_properties[i].insert(0,vessels_dict[vessel][vessel_properties_str[i]])
            vessel_properties[i].config(state=DISABLED)

    if piracy_parameter_label['text'] == 'USD/GT/Year: ':
        parameter_insurance_entry.delete(0, END)
        parameter_insurance_entry.insert(0,vessels_dict[vessel]['gross_entry'])

    elif piracy_parameter_label['text'] == 'USD/TEU/Year: ':
        parameter_insurance_entry.delete(0, END)
        parameter_insurance_entry.insert(0,vessels_dict[vessel]['teu_entry'])

    if vessel != 'new':
        # salary
        salary_month_entry.delete(0, END)
        salary_month_entry.insert(0,115000)

        # vessel insurance coefficient
        coefficient_insurance_entry.delete(0, END)
        coefficient_insurance_entry.insert(0, 0.343)

        # coefficient for repair and services
        coefficient_repair_service_entry.delete(0, END)
        coefficient_repair_service_entry.insert(0, 1.095)

        # coefficient for capital cost of vessel
        coefficient_capital_cost_entry.delete(0, END)
        coefficient_capital_cost_entry.insert(0, 10.9794625)


    if vessels_dict[vessel]['teu_entry'] < 6000:
        dwell_entry.delete(0, END)
        dwell_entry.insert(0,18)

    elif vessels_dict[vessel]['teu_entry'] >= 6000 and vessels_dict[vessel]['teu_entry'] < 10000:
        dwell_entry.delete(0, END)
        dwell_entry.insert(0,24)  

    elif vessels_dict[vessel]['teu_entry'] >= 10000 and vessels_dict[vessel]['teu_entry'] <= 11000:
        dwell_entry.delete(0, END)
        dwell_entry.insert(0,30)

    elif vessels_dict[vessel]['teu_entry'] > 11000 and vessels_dict[vessel]['teu_entry'] <= 15000:
        dwell_entry.delete(0, END)
        dwell_entry.insert(0,36)

    elif vessels_dict[vessel]['teu_entry'] > 15000 and vessels_dict[vessel]['teu_entry'] <= 20000:
        dwell_entry.delete(0, END)
        dwell_entry.insert(0,42)

#################################################################################################################################################################################################
########################################################################################## Stochastic #################################################################################################
#################################################################################################################################################################################################

########################################################################################## FUEL Probability #####################################################################################
# create label frame
lf_risk_fuel = ttk.LabelFrame(tab_risk, text="Fuel Price")
lf_risk_fuel.grid(column=0,row=0, padx=10, pady=5, ipady=5, ipadx=5, sticky=tk.EW)
lf_risk_fuel.columnconfigure(0, weight=1)
lf_risk_fuel.columnconfigure(1, weight=1)

# label stochastic fuel price mean
feul_mean_label = ttk.Label(lf_risk_fuel, text="Fuel Price Mean (USD): ")
feul_mean_label.grid(column=0, row=0, pady=5, sticky=tk.W, padx=5)
# Entry stochastic fuel price mean
feul_mean_risk = tk.DoubleVar()
feul_mean_risk_entry = ttk.Entry(lf_risk_fuel, textvariable=feul_mean_risk)
feul_mean_risk_entry.grid(column=1, row=0, pady=5, sticky=tk.E, padx=5)

# label stochastic fuel price STD
feul_std_label = ttk.Label(lf_risk_fuel, text="Fuel Price STD (USD): ")
feul_std_label.grid(column=0, row=1, sticky=tk.W, padx=5)
# Entry stochastic fuel price STD
feul_std_risk = tk.DoubleVar()
feul_std_risk_entry = ttk.Entry(lf_risk_fuel, textvariable=feul_std_risk)
feul_std_risk_entry.grid(column=1, row=1, sticky=tk.E, padx=5)

########################################################################################## Weather Probability #####################################################################################
# create label frame
lf_risk_weather = ttk.LabelFrame(tab_risk, text="Weather")
lf_risk_weather.grid(column=0,row=1, padx=10, pady=5, ipady=5, ipadx=5, sticky=tk.EW)
lf_risk_weather.columnconfigure(0, weight=1)
lf_risk_weather.columnconfigure(1, weight=1)

# label stochastic weather mean
weather_mean_label = ttk.Label(lf_risk_weather, text="Margin Mean \n(Percentage on distance): ")
weather_mean_label.grid(column=0, row=0, pady=5, sticky=tk.W, padx=5)
# Entry stochastic weather mean
weather_mean_risk = tk.DoubleVar()
weather_mean_risk_entry = ttk.Entry(lf_risk_weather, textvariable=weather_mean_risk)
weather_mean_risk_entry.grid(column=1, row=0, pady=5, sticky=tk.E, padx=5)

# label stochastic weather STD
weather_std_label = ttk.Label(lf_risk_weather, text="Margin STD \n(Percentage on distance): ")
weather_std_label.grid(column=0, row=1, sticky=tk.W, padx=5)
# Entry stochastic weather STD
weather_std_risk = tk.DoubleVar()
weather_std_risk_entry = ttk.Entry(lf_risk_weather, textvariable=weather_std_risk)
weather_std_risk_entry.grid(column=1, row=1, sticky=tk.E, padx=5)

########################################################################################## Wind Probability #####################################################################################
# create label frame
lf_risk_wind = ttk.LabelFrame(tab_risk, text="Wind and Currents")
lf_risk_wind.grid(column=0,row=2, padx=10, pady=5, ipady=5, ipadx=5, sticky=tk.EW)
lf_risk_wind.columnconfigure(0, weight=1)
lf_risk_wind.columnconfigure(1, weight=1)

# label stochastic weather mean
wind_mean_label = ttk.Label(lf_risk_wind, text="Shipping Speed Mean (Knots): ")
wind_mean_label.grid(column=0, row=0, pady=5, sticky=tk.W, padx=5)
# Entry stochastic weather mean
wind_mean_risk = tk.DoubleVar()
wind_mean_risk_entry = ttk.Entry(lf_risk_wind, textvariable=wind_mean_risk)
wind_mean_risk_entry.grid(column=1, row=0, pady=5, sticky=tk.E, padx=5)

# label stochastic weather STD
wind_std_label = ttk.Label(lf_risk_wind, text="Shipping Speed STD (Knots): ")
wind_std_label.grid(column=0, row=1, sticky=tk.W, padx=5)
# Entry stochastic weather STD
wind_std_risk = tk.DoubleVar()
wind_std_risk_entry = ttk.Entry(lf_risk_wind, textvariable=wind_std_risk)
wind_std_risk_entry.grid(column=1, row=1, sticky=tk.E, padx=5)

########################################################################################## Telecommiuniacations Probability #####################################################################################
# create label frame
lf_telecommiunications = ttk.LabelFrame(tab_risk, text="Telecommiunications")
lf_telecommiunications.grid(column=0,row=3, padx=10, pady=5, ipady=5, ipadx=5, sticky=tk.EW)
lf_telecommiunications.columnconfigure(0, weight=1)
lf_telecommiunications.columnconfigure(1, weight=1)

# label Telecommiuniacations Probability
telecommiunications_probability_label = ttk.Label(lf_telecommiunications, text="Telecommiunications Probability (%): ")
telecommiunications_probability_label.grid(column=0, row=0, pady=5, sticky=tk.W, padx=5)
# Entry Telecommiuniacations Probability
telecommiunications_probability = tk.DoubleVar()
telecommiunications_probability_entry = ttk.Entry(lf_telecommiunications, textvariable=telecommiunications_probability)
telecommiunications_probability_entry.grid(column=1, row=0, pady=5, sticky=tk.E, padx=5)

# label Telecommiuniacations time delay
telecommiunications_delay_label = ttk.Label(lf_telecommiunications, text="Telecommiunications Delay Time (days): ")
telecommiunications_delay_label.grid(column=0, row=1, sticky=tk.W, padx=5)
# Entry Telecommiuniacations time delay
telecommiunications_delay = tk.DoubleVar()
telecommiunications_delay_entry = ttk.Entry(lf_telecommiunications, textvariable=telecommiunications_delay)
telecommiunications_delay_entry.grid(column=1, row=1, sticky=tk.E, padx=5)

########################################################################################## Simulation Parameters #####################################################################################
# create label frame
lf_simulation = ttk.LabelFrame(tab_risk, text="Simulation")
lf_simulation.grid(column=0,row=4, padx=10, pady=5, ipady=5, ipadx=5, sticky=tk.EW)
lf_simulation.columnconfigure(0, weight=1)
lf_simulation.columnconfigure(1, weight=1)
# label Sample Random Number
random_number_label = ttk.Label(lf_simulation, text="Sample Random Number: ")
random_number_label.grid(column=0, row=0, padx=5, sticky=tk.W)

# Entry stochastic fuel price mean
random_number = tk.IntVar()
random_number_entry = ttk.Entry(lf_simulation, textvariable=random_number)
random_number_entry.grid(column=1, row=0, sticky=tk.E, padx=5)

########################################################################################## Button Simulation #####################################################################################
# Button Simulation
simulation_button = ttk.Button(tab_risk, text="Simulate by Monte Carlo", command=lambda: graphTimeCost(stochasticTimeCost()))
simulation_button.grid(column=0, row=5, pady=15, ipadx=5, ipady=5)

################################################################################### Stochastic Time Function ##########################################################################
def stochasticTimeCost():
    # Cost
    deterministic_cost = ((cargo_insurance_cost.get() * 1000000) + salary_voyage.get() + piracy_insurance_cost.get() + repair_service_vayage.get() + voyage_capital_cost.get() + voyage_insurance_cost.get() +
    port_dues.get() + total_environmental_cost.get()) / 1000000
    fuel_random = np.random.normal(feul_mean_risk.get(), feul_std_risk.get(), random_number.get())
    # Time
    deterministic = (bureaucracy.get() + dwell.get())/24   # days
    weather = np.random.normal(weather_mean_risk.get(), weather_std_risk.get(), random_number.get())
    speed = np.random.normal(wind_mean_risk.get(), wind_std_risk.get(), random_number.get())
    telecommunication_random_number = np.random.random() * 100
    #political = np.random.choices([], weights = [10, 1, 1], k = random_number)
    df = pd.DataFrame(index=range(random_number.get()), data={'deterministic':deterministic,'weather': weather, 'speed': speed, 'deterministic_cost':deterministic_cost, 'fuel_random':fuel_random,
    'telecommunication':0})
    if telecommunication_random_number <= float(telecommiunications_probability.get()):
        df['telecommunication'] == float(telecommiunications_delay.get())

    df['distance'] = (1 + df['weather']) * real_distance_nm.get()   # nm
    df['shipping_time'] = df['distance'] / df['speed'] / 24     # days
    df['bunkering'] = (fuel_consumption.get() * df['shipping_time'] / (fuel_tank_capacity.get() * 1000000)).astype(int) * bunkering.get()   # hours
    df['total_time'] = (df['bunkering']/24) + df['deterministic'] + df['shipping_time'] + df['telecommunication']   # days
    df['fuel_consumption_cost'] = ((df['shipping_time'] * fuel_consumption.get() * df['fuel_random']) / (521 * 1000000))
    df['total_cost'] = df['deterministic_cost'] + df['fuel_consumption_cost']


    return df

def graphTimeCost(df):
    # Use TkAgg
    matplotlib.use("TkAgg")

    # Create a figure of specific size
    figure = FigureMat(figsize=(4, 7), dpi=100)
    figure.subplots_adjust(left=0.1,bottom=0.1, right=0.9, top=0.9, wspace=0.4, hspace=0.4)

    # Define Mean and STD Total Time
    mean_total_time = round(df["total_time"].mean(),2)
    std_total_time = round(df["total_time"].std(),2)

    # Define Mean and STD Total Cost
    mean_total_cost = round(df["total_cost"].mean(),3)
    std_total_cost = round(df["total_cost"].std(),3)

    # Define the points for plotting the figure
    plot_cost = figure.add_subplot(2, 1, 1)
    plot_cost.hist(df["total_cost"], label='Total Cost' ,bins=60, color='teal')
    plot_cost.axvline(df["total_cost"].mean(), color='k', linestyle='dashed', linewidth=2)
    plot_cost.text(23, 45, r'$\mu=15, b=3$')
    plot_cost.legend()
    plot_cost.set_xlabel('Total Cost (Million USD)')
    plot_cost.set_ylabel('Frequency')
    plot_cost.set_title('Total Cost Calculation based on stochastic and deterministic variables\n Mean = {} , STD = {}'.format(mean_total_cost, std_total_cost),fontsize=8)

    plot_time = figure.add_subplot(2, 1, 2)
    plot_time.hist(df["total_time"], label='Total Time' ,bins=60, color='cornflowerblue')
    plot_time.axvline(df["total_time"].mean(), color='k', linestyle='dashed', linewidth=2)
    plot_time.legend()
    plot_time.set_xlabel('Total Time (Days)')
    plot_time.set_ylabel('Frequency')
    plot_time.set_title('Total Time Calculation based on stochastic and deterministic variables\n Mean = {} , STD = {}'.format(mean_total_time, std_total_time),fontsize=8)
    
    # Add a canvas widget to associate the figure with canvas
    canvas = FigureCanvasTkAgg(figure, tab_risk)
    canvas.get_tk_widget().grid(column=1,row=0, rowspan=7, columnspan=2)

#################################################################################################################################################################################################
########################################################################################## References #################################################################################################
#################################################################################################################################################################################################
# # Center Buttom
tab_references.columnconfigure(0,weight=1)
tab_references.columnconfigure(2,weight=1)

#  Button Simulation
reference_button = ttk.Button(tab_references, text="Open the references file", command=lambda: openReferenceFile())
reference_button.grid(column=1, row=0, pady=15, ipadx=5, ipady=5)

def openReferenceFile():
    DummyFile = 'references.docx'
    os.startfile(DummyFile)


#################################################################################################################################################################################################
########################################################################################## Developers #################################################################################################
#################################################################################################################################################################################################

################################################################################################ Sajjadi ##########################################################################################
# Frame
frame_sajjadi = ttk.Frame(tab_developers)
frame_sajjadi.grid(column=1,row=1, pady=10, padx=10, sticky=tk.W)

# Photo
image_sajjadi = Image.open("sajjadi.png")
image_sajjadi_resized = image_sajjadi.resize((100, 100), Image.ANTIALIAS)
image_sajjadi_show = ImageTk.PhotoImage(image_sajjadi_resized)
image_sajjadi_label = ttk.Label(frame_sajjadi, image=image_sajjadi_show)
image_sajjadi_label.grid(column=1,row=1, rowspan=3, padx=20, pady=20)

# general labels
name_label = ttk.Label(frame_sajjadi, foreground='blue', font=("", 8), text="Full Name: ")
#expertise_label = ttk.Label(frame_sajjadi, foreground='blue', font=("", 8), text="Expertise: ")
title_label = ttk.Label(frame_sajjadi, foreground='blue', font=("", 8), text="Duty in this project: ")
email_label = ttk.Label(frame_sajjadi, foreground='blue', font=("", 8), text="Email Address: ")

name_label.grid(column=2, row=1, padx=10, sticky=tk.W)
#expertise_label.grid(column=2, row=2, padx=10, sticky=tk.W)
title_label.grid(column=2, row=2, padx=10, sticky=tk.W)
email_label.grid(column=2, row=3, padx=10, sticky=tk.W)

# personal labels
sajjadi_name_label = ttk.Label(frame_sajjadi, foreground='red', font=("",10), text="Sayed Mohammad Sajjadi")
#sajjadi_expertise_label = ttk.Label(frame_sajjadi, foreground='red', font=("", 10), text="Mechanical Engineering - Manufacturing & Design")
sajjadi_title_label = ttk.Label(frame_sajjadi, foreground='red', font=("", 10), text="Team Leader, Software Developer, Model Creator")
sajjadi_email_label = ttk.Label(frame_sajjadi, foreground='red', font=("", 10), text="mosajd@gmail.com ,  sayed.mohammad.sajjadi@simulationteam.com")

sajjadi_name_label.grid(column=3, row=1, columnspan=2, padx=20, sticky=tk.W)
#sajjadi_expertise_label.grid(column=3, row=2, columnspan=2, padx=20, sticky=tk.W)
sajjadi_title_label.grid(column=3, row=2, columnspan=2, padx=20, sticky=tk.W)
sajjadi_email_label.grid(column=3, row=3, columnspan=2, padx=20, sticky=tk.W)

################################################################################################ Siddhi ##########################################################################################
# Frame
frame_siddhi = ttk.Frame(tab_developers)
frame_siddhi.grid(column=1,row=2, pady=10, padx=10, sticky=tk.W)

frame_siddhi.columnconfigure(1,weight=1)
frame_siddhi.columnconfigure(2,weight=2)
frame_siddhi.columnconfigure(3,weight=1)
frame_siddhi.columnconfigure(4,weight=1)

# Photo
image_siddhi = Image.open("siddhi.png")
image_siddhi_resized = image_siddhi.resize((100, 100), Image.ANTIALIAS)
image_siddhi_show = ImageTk.PhotoImage(image_siddhi_resized)
image_siddhi_label = ttk.Label(frame_siddhi, image=image_siddhi_show)
image_siddhi_label.grid(column=1,row=1, rowspan=3, padx=20, pady=20, sticky=tk.W)

# general labels
name_label = ttk.Label(frame_siddhi, foreground='blue', font=("", 8),text="Full Name: ")
#expertise_label = ttk.Label(frame_siddhi, foreground='blue', font=("", 8),text="Expertise: ")
title_label = ttk.Label(frame_siddhi, foreground='blue', font=("", 8),text="Duty in this project: ")
email_label = ttk.Label(frame_siddhi, foreground='blue', font=("", 8),text="Email Address: ")

name_label.grid(column=2, row=1, padx=10, sticky=tk.W)
#expertise_label.grid(column=2, row=2, padx=10, sticky=tk.W)
title_label.grid(column=2, row=2, padx=10, sticky=tk.W)
email_label.grid(column=2, row=3, padx=10, sticky=tk.W)

# personal labels
siddhi_name_label = ttk.Label(frame_siddhi, foreground='red', font=("",10), text="Siddhi Rajendra Gangar")
#siddhi_expertise_label = ttk.Label(frame_siddhi, foreground='red', font=("",10), text="Electronics and Telecommunications  Engineer and Strategic Management")
siddhi_title_label = ttk.Label(frame_siddhi, foreground='red', font=("",10), text="Data research and analysis, Model Creator")
siddhi_email_label = ttk.Label(frame_siddhi, foreground='red', font=("",10), text="rhsiddhi@yahoo.com")

siddhi_name_label.grid(column=4, row=1, columnspan=2, padx=20, sticky=tk.W)
#siddhi_expertise_label.grid(column=4, row=2, columnspan=2, padx=20, sticky=tk.W)
siddhi_title_label.grid(column=4, row=2, columnspan=2, padx=20, sticky=tk.W)
siddhi_email_label.grid(column=4, row=3, columnspan=2, padx=20, sticky=tk.W)

################################################################################################ Giovanni ##########################################################################################
# Frame
frame_giovanni = ttk.Frame(tab_developers)
frame_giovanni.grid(column=1,row=3, pady=10, padx=10, sticky=tk.W)

# Photo
image_giovanni = Image.open("giovanni.png")
image_giovanni_resized = image_giovanni.resize((100, 100), Image.ANTIALIAS)
image_giovanni_show = ImageTk.PhotoImage(image_giovanni_resized)
image_giovanni_label = ttk.Label(frame_giovanni, image=image_giovanni_show)
image_giovanni_label.grid(column=1,row=1, rowspan=3, padx=20, pady=20)

# general labels
name_label = ttk.Label(frame_giovanni, foreground='blue', font=("", 8),text="Full Name: ")
#expertise_label = ttk.Label(frame_giovanni, foreground='blue', font=("", 8),text="Expertise: ")
title_label = ttk.Label(frame_giovanni, foreground='blue', font=("", 8),text="Duty in this project: ")
email_label = ttk.Label(frame_giovanni, foreground='blue', font=("", 8),text="Email Address: ")

name_label.grid(column=2, row=1, padx=10, sticky=tk.W)
#expertise_label.grid(column=2, row=2, padx=10, sticky=tk.W)
title_label.grid(column=2, row=2, padx=10, sticky=tk.W)
email_label.grid(column=2, row=3, padx=10, sticky=tk.W)

# personal labels
giovanni_name_label = ttk.Label(frame_giovanni, foreground='red', font=("",10), text="Giovanni Maria Ferraris")
#giovanni_expertise_label = ttk.Label(frame_giovanni, foreground='red', font=("",10), text="Chemical Engineering")
giovanni_title_label = ttk.Label(frame_giovanni, foreground='red', font=("",10), text="Data research and analysis, Model Creator")
giovanni_email_label = ttk.Label(frame_giovanni, foreground='red', font=("",10), text="giovannimariaferraris@gmail.com")

giovanni_name_label.grid(column=3, row=1, columnspan=2, padx=20, sticky=tk.W)
#giovanni_expertise_label.grid(column=3, row=2, columnspan=2, padx=20, sticky=tk.W)
giovanni_title_label.grid(column=3, row=2, columnspan=2, padx=20, sticky=tk.W)
giovanni_email_label.grid(column=3, row=3, columnspan=2, padx=20, sticky=tk.W)




root.mainloop()

####################################################################################################################################################################################################

##################################################################### THIS SOFTWARE IS CREATED BY SAYED MOHAMMAD SAJJADI, MOSAJD@GMAIL.COM #########################################################

##################################################################################### https://github.com/mosajd ####################################################################################

####################################################################################################################################################################################################