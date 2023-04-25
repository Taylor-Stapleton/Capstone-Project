from tkinter import*
import tkinter as tk
from geopy.geocoders import Nominatim
from tkinter import ttk,messagebox
from timezonefinder import TimezoneFinder
from datetime import *
import requests
import pytz
from PIL import Image, ImageTk
import json
from io import BytesIO
import urllib.request

# API endpoint and key
url = "https://api.openweathermap.org/data/2.5/weather"
api_key = "0e3ccabaab93b1986b25abd5207f6f3f"


# Function to get weather data from API
def get_weather_data(city_name, unit):
    geolocator= Nominatim(user_agent="geoapiExpress")
    location= geolocator.geocode(city_name)
    obj = TimezoneFinder()

    result = obj.timezone_at(lng=location.longitude,lat=location.latitude)
    timezone.config(text=result)
    long_lat.config(text=f"{round(location.latitude, 4)}°N, {round(location.longitude,4 )}°E")

    home=pytz.timezone(result)
    local_time=datetime.now(home)
    current_time=local_time.strftime("%I:%M %p")
    clock.config(text=current_time)
    params = {"q": city_name, "appid": api_key, "units": unit}
    response = requests.get(url, params=params)
    data = json.loads(response.text)
    return data

# Function to display weather data
def display_weather_data():
    city = city_entry.get()
    unit = "metric" if unit_var.get() == 1 else "imperial"
    data = get_weather_data(city, unit)
    if data["cod"] != "404":
        weather = data["weather"][0]["description"].title()
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        high_temp = data["main"]["temp_max"]
        low_temp = data["main"]["temp_min"]
        unit_symbol = "°C" if unit == "metric" else "°F"
        weather_label.config(text=f"Weather: {weather}")
        temp_label.config(text=f"Temperature: {temp}{unit_symbol}")
        feels_like_label.config(text=f"Feels like: {feels_like}{unit_symbol}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        wind_speed_label.config(text=f"Wind speed: {wind_speed} m/s")
        high_temp_label.config(text=f" {high_temp}{unit_symbol}")
        low_temp_label.config(text=f" {low_temp}{unit_symbol}")
        icon_id = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/w/{icon_id}.png"
        with urllib.request.urlopen(icon_url) as url:
            icon_data = url.read()
        icon_image = Image.open(BytesIO(icon_data))
        icon_photo = ImageTk.PhotoImage(icon_image)
        icon_label.config(image=icon_photo)
        icon_label.image = icon_photo
        
        
    else:
        weather_label.config(text="City not found")
        temp_label.config(text="")
        feels_like_label.config(text="")
        humidity_label.config(text="")
        wind_speed_label.config(text="")
        high_temp_label.config(text="")
        low_temp_label.config(text="")

       

        


        
        

# Create window
window = Tk()
window.title("Weather App")
window.geometry("890x470+300+200")
window.configure(bg="#57adff")
window.resizable(False,False)


  

# Icon label



#--------icon---------
image_icon=PhotoImage(file="Images\logo.png")
window.iconphoto(False, image_icon)

Round_box=PhotoImage(file="Images\Rounded Rectangle 1.png")
Label(window, image=Round_box,bg="#57adff").place(x=30, y=110)

# Icon label
icon_label = tk.Label(window, bg="#203243")
icon_label.place(x=100, y=250)


#------Label--------
label1=Label(window,text="Temperature:", font=('Helvetica, 11'), fg="white",bg="#203243")
label1.place(x=40,y=120)

label2=Label(window,text="Humidity:", font=('Helvetica, 11'), fg="white",bg="#203243")
label2.place(x=40,y=140)

label3=Label(window,text="Feels like:", font=('Helvetica, 11'), fg="white",bg="#203243")
label3.place(x=40,y=160)

label4=Label(window,text="Wind speed:", font=('Helvetica, 11'), fg="white",bg="#203243")
label4.place(x=40,y=180)

label5=Label(window,text="Weather:", font=('Helvetica, 11'), fg="white",bg="#203243")
label5.place(x=40,y=200)





# Create labels and entry

unit_label = tk.Label(window, text="Unit:",font=('Helvetica, 11'), bg="#203243", fg="white")
unit_var = tk.IntVar()
unit_c_button = tk.Radiobutton(window, text="C", variable=unit_var, value=1, font=('Helvetica, 9'), bg="#203243", fg="white")
unit_f_button = tk.Radiobutton(window, text="F", variable=unit_var, value=2, font=('Helvetica, 9'), bg="#203243", fg="white")
unit_f_button.select() # Default to Fahrenheit
weather_label = tk.Label(window, text="",font=('Helvetica, 11'), bg="#203243", fg="white")
temp_label = tk.Label(window, text="",font=('Helvetica, 11'), bg="#203243", fg="white")
feels_like_label = tk.Label(window, text="",font=('Helvetica, 11'), bg="#203243", fg="white")
humidity_label = tk.Label(window, text="",font=('Helvetica, 11'), bg="#203243", fg="white")
wind_speed_label = tk.Label(window, text="",font=('Helvetica, 11'), bg="#203243", fg="white")





# Position labels and entry
unit_label.place(x=50, y=222)
unit_c_button.place(x=85, y=220)
unit_f_button.place(x=115, y=220)


weather_label.place(x=38, y=200)
temp_label.place(x=38, y=120)
feels_like_label.place(x=38, y=160)
humidity_label.place(x=38, y=140)
wind_speed_label.place(x=38, y=180)





#-----------Search Box----------

Search_image=PhotoImage(file="Images\Rounded Rectangle 3.png")
myimage=Label(image=Search_image,bg="#57adff")
myimage.place(x=270,y=120)

weat_image=PhotoImage(file="Images\Layer 7.png")
weatherimage=Label(window,image=weat_image,bg="#203243")
weatherimage.place(x=290,y=127)

city_entry=tk.Entry(window,justify='center',width=15,font=('poppins',25,'bold'),bg="#203243",border=0,fg="white")
city_entry.place(x=370,y=130)
city_entry.focus()

def on_enter(event):
    display_weather_data()

city_entry.bind('<Return>', on_enter)

Search_icon=PhotoImage(file="Images\Layer 6.png")
display_button =Button(image=Search_icon,borderwidth=0,cursor="hand2",bg='#203243', command=display_weather_data)
display_button.place(x=645,y=125)

#--------Clock---------
clock=Label(window,font=("Helvetica",30,'bold'),fg="white",bg="#57adff")
clock.place(x=30,y=20)


#---------Timezone-----------
timezone=Label(window,font=("Helvetica",20),fg="white",bg="#57adff")
timezone.place(x=670,y=20)

long_lat=Label(window,font=("Helvetica",10),fg="white",bg="#57adff")
long_lat.place(x=670,y=55)





#--------------------------------







#-----Bottom Box------------
window=Frame(window, width=900, height=180, bg="#212120")
window.pack(side=BOTTOM)

#------Bottom Boxes----------
firstbox=PhotoImage(file="Images\Rounded Rectangle 2.png")
secondbox=PhotoImage(file="Images\Rounded Rectangle 2 copy.png")

Label(window, image=firstbox,bg="#212120").place(x=30,y=20)
Label(window, image=secondbox,bg="#212120").place(x=300,y=20)
Label(window, image=secondbox,bg="#212120").place(x=400,y=20)
Label(window, image=secondbox,bg="#212120").place(x=500,y=20)
Label(window, image=secondbox,bg="#212120").place(x=600,y=20)
Label(window, image=secondbox,bg="#212120").place(x=700,y=20)
Label(window, image=secondbox,bg="#212120").place(x=800,y=20)

#--------------First cell with image---------











firframe=Frame(window,width=230, height=132, bg="#282829")
firframe.place(x=35,y=100)

icon_label =Label(firframe,bg="#282829")
icon_label.place(x=5, y=50)

firimage=Label(firframe, bg="#282829")
firframe.place(x=35,y=25)

#---------------------High temp------
high_temp_label = Frame(window,width=150, height=25, bg="#282829")
high_temp_label.place(x=115, y=85)



high_temp_label=Label(high_temp_label,font="Helvetica 15 bold", bg="#282829", fg="#fff")
high_temp_label.place(x=5, y=3)


#--------------Low Temp----------------

low_temp_label =  Frame(window,width=150, height=25, bg="#282829")
low_temp_label.place(x=115, y=125)


low_temp_label=Label(low_temp_label,font="Helvetica 11 bold", bg="#282829", fg="#fff")
low_temp_label.place(x=5, y=3)

#----First cell---------
firstframe=Frame(window,width=230, height=35,bg="#282829")
firstframe.place(x=35,y=25)

day1=Label(firstframe, font="arial 20",bg="#282829",fg="#fff")
day1.place(x=55,y=5)

firstimage=Label(firstframe, bg="#282829")
firstimage.place(x=1, y=15)




#----Second cell---------
Secondframe=Frame(window,width=70, height=115, bg="#282829")
Secondframe.place(x=305.4,y=25)

day2=Label(Secondframe, bg="#282829", fg="#fff")
day2.place(x=5,y=5)

secondimage=Label(Secondframe, bg="#282829")
secondimage.place(x=7,y=20)



#----Third cell---------
Thirdframe=Frame(window,width=70, height=115, bg="#282829")
Thirdframe.place(x=405.4,y=25)


day3=Label(Thirdframe,  bg="#282829", fg="#fff")
day3.place(x=5,y=5)

thirdimage=Label(Thirdframe, bg="#282829")
thirdimage.place(x=7,y=20)

#----Fourth cell---------
Fourthframe=Frame(window,width=70, height=115, bg="#282829")
Fourthframe.place(x=505.4,y=25)

day4=Label(Fourthframe, bg="#282829", fg="#fff")
day4.place(x=10,y=5)

fourthimage=Label(Fourthframe, bg="#282829")
fourthimage.place(x=7,y=20)

#----Fifth cell---------
Fifthframe=Frame(window,width=70, height=115, bg="#282829")
Fifthframe.place(x=605.4,y=25)


day5=Label(Fifthframe,  bg="#282829", fg="#fff")
day5.place(x=10,y=5)

fifthimage=Label(Fifthframe, bg="#282829")
fifthimage.place(x=7,y=20)

#----Sixth cell---------
Sixthframe=Frame(window,width=70, height=115, bg="#282829")
Sixthframe.place(x=705.4,y=25)


day6=Label(Sixthframe,  bg="#282829", fg="#fff")
day6.place(x=10,y=5)


sixthimage=Label(Sixthframe, bg="#282829")
sixthimage.place(x=7,y=20)

#----Seventh cell---------
Seventhframe=Frame(window,width=70, height=115, bg="#282829")
Seventhframe.place(x=805.4,y=25)


day7=Label(Seventhframe, bg="#282829", fg="#fff")
day7.place(x=10,y=5)


seventhimage=Label(Seventhframe, bg="#282829")
seventhimage.place(x=7,y=20)


#---------cells-----------
#---------first----------















#-------------days----------




first = datetime.now()
day1.config(text=first.strftime("%A"))

second=first+timedelta(days=1)
day2.config(text=second.strftime("%A"))

third=first+timedelta(days=2)
day3.config(text=third.strftime("%A"))

fourth=first+timedelta(days=3)
day4.config(text=fourth.strftime("%A"))

fifth=first+timedelta(days=4)
day5.config(text=fifth.strftime("%A"))

sixth=first+timedelta(days=5)
day6.config(text=sixth.strftime("%A"))

seventh=first+timedelta(days=6)
day7.config(text=seventh.strftime("%A"))





# Start window
window.mainloop()