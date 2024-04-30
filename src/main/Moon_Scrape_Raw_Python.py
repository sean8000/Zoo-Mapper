from bs4 import BeautifulSoup 
from selenium import webdriver
import docx
import time
import pandas as pd
from datetime import datetime, timedelta

def days_between(d1, d2):
    """
    This function takes in two strings as dates and returns the number of days that take place
    between the two
    INPUTS: 
        d1: string representing date with format YYYY-MM-DD
        d2: string representing date with format YYYY-MM-DD
    OUTPUT:
        The number of days between the two inputted dates
    """
    
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    
    return abs((d2 - d1).days)

def subtract_days(date, days_to_subtract):
    """
    This function takes in one string as date and one number representing the days we want to
    go back. We return the date that comes days_to_subtract before the inputted date
    INPUTS:
        date: string representing date with format YYYY-MM-DD. 
        days_to_subtract: integer representing the number of days we want to modify our inputted
        date with
    OUTPUT:
        a string representing the date that is days_to_subtract before the inputted date
    """
    return str(datetime.strptime(date, "%Y-%m-%d") - timedelta(days=days_to_subtract))

Numbers = '1234567890'
Moon_Info_Options = []

def doc_to_excel_Moon_Data(File_Name:str, latitiude:str, longitude:str, new_excel_name:str):
    """
    In this function, we intake a docx file that contains dates and descriptions we want to grab moon data for. In the
    first section, we seperate the dates and descriptions, format them, and input them in a dataframe. Then we activate
    the chrome driver and begin constructing URLs so that we can grab the proper data from the website. We grab each
    url, parse the html to grab the data we need, and insert it into our dataframe. We finish by exiting the chrome driver,
    inserting all of the scraped data into our dataframes, and input it into a new excel sheet. 
    INPUTS:
        File_Name: Name of the .docx file we want to grab moon data for
        latitude: string representing the latitude of the aquarium where the data was recorded
        longitude: string representing the longitude of the aquarium where the data was recorded
    OUTPUT:
        We want to create a spread sheet containing the moon data for all of the dates recorded
        in the docx file. 
    """
    doc = docx.Document(File_Name)

    Dates = []                                      # Will store the dates we want to scrape from site
    Descriptions = []                               # Will Store the descriptions of the data we collected


    for i in doc.paragraphs:                        # going through our document and grabbing each line
        line = i.text
        if (line=="" or line[0] not in Numbers):    # filtering out lines with no date in front
            pass;
        else:                                       # these are the lines that begin with dates
            split_line = line.replace("–", "-").split("-") # seperating the dates from the descriptions
            if (len(split_line) == 0): 
                return;                             # Document not propery formatted
        
            if(split_line[0][1] == "/"):            # checking to see if the month is only 1 number, adding zero if needed (this standardizes of length of string)
                split_line[0] = "0" + split_line[0]
            
            if(split_line[0][4] == "/"):            # checking to see if the day is only 1 number, adding zero if needed (this standardizes of length of string)
                split_line[0] =  split_line[0][:3] + "0" + split_line[0][3:]
            
            split_line[0] = split_line[0][6:10] + "/" + split_line[0][:3] + split_line[0][3:5]  # formatting date to standardize it

            # adding the data to our lists
            Dates.append(split_line[0].replace("/", "-"))
            Descriptions.append(split_line[1])

    df = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates}) # Create a dataframe with the seperated dates and descriptions

    print("Setting Up Web Driver")

    driver = webdriver.Chrome()                     # creating our web driver
    driver.minimize_window()                        # minimizing the window so that it is not blocking the screen

    print("Web Driver Set-Up Complete")

    # These are all of the lists that will hold the data that we scrape
    URL = []                                        # this will hold the URL used to scrape the data
    Moon_Rise = []                                  # this will hold the time that the moon rose that day
    Moon_Culmination = []                           # this will hold the the time the moon passes over the meridian (culmination)
    Moon_Set = []                                   # this will hold the time when the moon touches the horizon
    Moon_Distance = []                              # this will hold the distance the moon is from the earth
    Moon_Altitude = []                              # this will hold the Altitude: The angle between the center of moon and the horizon including refraction.
    Moon_Azimuth = []                               # this will hold the Azimuth: The angle between the meridional plane of the earth and the vertical plane of the moon.
    Moon_Phase = []                                 # this will hold the moon phase
    Disk_Illumination = []                          # this will hold the percentage of the disk that is illuminated
    # Calculations
    Next_New_Moon_Date = []                         # this will hold the date of the next new moon
    Days_Till_Next_New_Moon = []                    # this will hold the number of days until the next new moon
    Next_Full_Moon_Date = []                        # this will hold the date of the next full moon
    Days_Till_Next_Full_Moon = []                   # this will hold the number of days until the next full moon             
    Prev_New_Moon_Date = []                         # this will hold the date of the previous new moon
    Days_Since_Prev_New_Moon = []                   # this will hold the number of days since the last new moon
    Prev_Full_Moon_Date = []                        # this will hold the date of the previous full moon
    Days_Since_Prev_Full_Moon = []                  # this will hold the number of days since the last new moon
    
    print("Begin Web Scraping")

    for ind in df.index:
        year = df['Dates'][ind][:4]                 # Grabbing the year 
        month = df['Dates'][ind][5:7]               # grabbing our month
        day = df['Dates'][ind][8:10]                # Grabbing our day

        # creating the URL we will scrape our data from
        url = "https://www.mooncalc.org/#/" + latitiude + "," + longitude + ",3/" + year + "." + month + "." + day + "/00:00/1/3"
        URL.append(url)                             # Adding constructed URL to list 
        
        driver.get(url)                             # searching using our constructed URL
        time.sleep(.25)                             # need a little bit to wait to make sure we have finished grabbing the values
        
        # insert html into soup so that we can search for the data we want
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Grabbing The Moon Rise Time
        Moon_Rs = soup.find('span', id='clickSunrise').contents[0]  # Grabbing data from the html file (using known id)
        Moon_Rise.append(Moon_Rs)                                   # append data to ther proper list

        # Grabbing the Moon Culmination
        Moon_Cul = soup.find('span', id='clickSunrise').contents[0] # Grabbing data from the html file (using known id)
        Moon_Culmination.append(Moon_Cul)                           # append data to the proper list

        # Grabbing the moon set 
        Moon_St = soup.find('span', id='clickSunset').contents[0]   # Grabbing data from the html file (using known id)
        Moon_Set.append(Moon_St)                                    # append data to the proper list

        # Grabbing the moon distance
        Moon_Dist = soup.find('span', {"class":"time-span twilight dawn-time"}).contents[0] # Grabbing data from the html file (based on class)
        Moon_Dist = Moon_Dist.replace("km", "")                                             # Getting rid of the km from the data 
        Moon_Distance.append(Moon_Dist)                                                     # append data to the proper lsit

        # Grabbing the moon altitude
        Moon_Alt = soup.find('span', id="sunhoehe").contents[0]     # Grabbing data from the html file (using known id)
        Moon_Alt = Moon_Alt.replace("°","")                         # getting rid of °
        Moon_Altitude.append(Moon_Alt)                              # append data to proper list

        # Grabbing the moon azimuth
        Moon_Azi = soup.find('span', id='azimuth').contents[0]      # Grabbing data from the html file (using known id)
        Moon_Azi = Moon_Azi.replace("°","")                         # Getting rid of °
        Moon_Azimuth.append(Moon_Azi)                               # append data to proper list
        
        # Grabbing both the moon Phase and Moon Illumination
        Phase_and_Illumination = soup.find('span', {"class":"moontext dusk-time"}).contents[0].split('/')   # Grabbing data from the html file (based on the class)
        Moon_Phase.append(Phase_and_Illumination[0])                                                        # inputting Phase into proper list
        Phase_and_Illumination[1] = Phase_and_Illumination[1].replace("%","")                               # Getting rid of % in result
        Disk_Illumination.append(Phase_and_Illumination[1])                                                 # inputting Illumination into proper list                                           # inputting Illumination into proper list
        
        # Calculations

        Current_Date = df['Dates'][ind][:10]                        # grabbing the date we are working on
        
        # Calculation for Next New Moon (Date + Days Till)
        New_Moon = soup.find('span', {"class":"moontext neumond"}).contents[0]  # Grabbing data from the html file (based on the class)
        New_Moon = New_Moon.split(" ")                                          # Splitting data based on format: Next_NM_Date Time_Until
        Next_NM_DT= New_Moon[0].split(".")                                      # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_NM_DT = Next_NM_DT[2] + "-" + Next_NM_DT[1] + "-" + Next_NM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_New_Moon_Date.append(Next_NM_DT)                                   # Appending Next New Moon Date to Proper List
        Next_NM_Days = days_between(Current_Date, Next_NM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_New_Moon.append(Next_NM_Days)                            # Appending Days between next New Moon + Inputted date to proper list
        
        # Calculation for Next Full Moon (Date + Days Till)
        Full_Moon = soup.find('span', {"class":"moontext vollmond"}).contents[0]# Grabbing data from the html file (based on the class)
        Full_Moon = Full_Moon.split(" ")                                        # Splitting data based on format: Next_FM_Date Time_Until
        Next_FM_DT = Full_Moon[0].split('.')                                    # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_FM_DT = Next_FM_DT[2] + "-" + Next_FM_DT[1] + "-" + Next_FM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_Full_Moon_Date.append(Next_FM_DT)                                  # appending Next Full Moon Date to proper list
        Next_FM_Days = days_between(Current_Date, Next_FM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_Full_Moon.append(Next_FM_Days)                           # Appending Days between next Full Moon + Inputted date to proper list
        
        # Calculation for Prev New Moon
        Lunar_Phase = 29         

        Prev_NM_DT = subtract_days(Next_NM_DT, Lunar_Phase)[:10]                # calculating date of previous new moon via inputting: next one - lunar phase
        
        Prev_New_Moon_Date.append(Prev_NM_DT)                                   # appending Previous New Moon Date into proper list
        Prev_NM_Days = days_between(Current_Date, Prev_NM_DT)                   # calculating the number of days between the inputted date and the date of previous new moon
        Days_Since_Prev_New_Moon.append(Prev_NM_Days)                           # Appending Days between previous New Moon + Inputted date to proper list
        
        # Calculation for Prev Full Moon
        Prev_FM_DT = subtract_days(Next_FM_DT, Lunar_Phase)[:10]                # calculating date of previous full moon via inputting: next one - lunar phase             
        
        Prev_Full_Moon_Date.append(Prev_FM_DT)                                  # appending Previous Full Moon Date into proper list
        Prev_FM_Days = days_between(Current_Date, Prev_FM_DT)                   # calculating the number of days between the inputted date and the date of previous full moon
        Days_Since_Prev_Full_Moon.append(Prev_FM_Days)                          # Appending Days between previous Full Moon + Inputted date to proper list
        
        
        driver.delete_all_cookies()
        # Loop Complete, onto the next row + URL

    print("Complete Web Scraping")

    driver.quit()                       # close out driver

    print("Driver Closed")
    

    # Creatin our final Dataframe with the data we have scraped/calcualted

    df_final = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates, "Moon Rise":Moon_Rise, "Moon Culmination":Moon_Culmination,
                             "Moon Set":Moon_Set, "Moon Distance (km)":Moon_Distance,"Moon Altitude (°)":Moon_Altitude,
                             "Moon Azimuth (°)":Moon_Azimuth, "Moon Phase":Moon_Phase,"Disk Illumination (%)":Disk_Illumination,
                             "Next New Moon Date":Next_New_Moon_Date, "Days Till Next New Moon":Days_Till_Next_New_Moon,
                             "Next Full Moon Date":Next_Full_Moon_Date, "Days Till Full New Moon":Days_Till_Next_Full_Moon,
                             "Prev New Moon Date":Prev_New_Moon_Date, "Days Since New Moon":Days_Since_Prev_New_Moon,
                             "Prev Full Moon Date":Prev_Full_Moon_Date, "Days Since Full New Moon":Days_Since_Prev_Full_Moon,
                             "URL":URL})
    
    # created the moon scrape dataframe, now creating new Excel Sheet
    filename = File_Name.rsplit("/", 1)
    print(filename[0] + new_excel_name + ".xlsx")
    df_final.to_excel(filename[0]  + "/" + new_excel_name + ".xlsx")

    print("Scraping of Moon Data Complete!!!")

    return

def excel_to_new_excel_Moon_Data(File_Name:str, Sheet_Name:str, Date_Column:str, Comment_Column:str, latitiude:str, longitude:str, new_excel_name:str):
    """
    In this function, we intake an excel file that may contain several sheets with lots if information. We are looking to 
    we want to grab dates and comments from the sheet name we are inputting, and then adding them into a new dataframe.
    Once that is done, we activate the chrome driver and begin constructing URLs so that we can grab the data we want from 
    the website. We grab each url, parse the html to grab the data we need, and insert it into our dataframe. We finish by 
    exiting the chrome driver, inserting all of the scraped data into our dataframes, and input it into a new excel sheet. 
    INPUTS:
        File_Name: Name of the .excl file we want to grab moon data for
        Sheet_Name: The sheet in the file where we will grab our initial data
        Date_Column: The column that contains the date we want to scrape data for 
        Comment_Column: The column that contains comments associated with dates
        latitude: string representing the latitude of the aquarium where the data was recorded
        longitude: string representing the longitude of the aquarium where the data was recorded
    OUTPUT:
        We want to create a new spread sheet containing the moon data for all of the dates recorded
        in the docx file. 
    """
    df = pd.read_excel(io=File_Name, sheet_name=Sheet_Name)

    Dates = []                                      # Will store the dates we want to scrape from site
    Descriptions = []                               # Will store the descriptions we want to scrape from site

    for ind in df.index:                            # going through our document and grabbing each line
        date = str(df[Date_Column][ind])            # grabbing the dates, placing in variable
        desc = df[Comment_Column][ind]

        if (date=="" and desc==""):    # we got all the dates, the rest of the cols don't matter
            break
        if (date== "NaT"):
            pass
        else:
            Dates.append(date)
            Descriptions.append(desc)

    # creating a dataframe 
    df = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates})

    print("Setting Up Web Driver")

    driver = webdriver.Chrome()                     # creating a chrome webdriver 
    driver.minimize_window()                        # minimizing the window so that it is not blocking the screen

    print("Web Driver Set Up Complete")

    # These are all of the lists that will hold the data that we scrape
    URL = []                                        # this will hold the URL used to scrape the data
    Moon_Rise = []                                  # this will hold the time that the moon rose that day
    Moon_Culmination = []                           # this will hold the the time the moon passes over the meridian (culmination)
    Moon_Set = []                                   # this will hold the time when the moon touches the horizon
    Moon_Distance = []                              # this will hold the distance the moon is from the earth
    Moon_Altitude = []                              # this will hold the Altitude: The angle between the center of moon and the horizon including refraction.
    Moon_Azimuth = []                               # this will hold the Azimuth: The angle between the meridional plane of the earth and the vertical plane of the moon.
    Moon_Phase = []                                 # this will hold the moon phase
    Disk_Illumination = []                          # this will hold the percentage of the disk that is illuminated
    # Calculations
    Next_New_Moon_Date = []                         # this will hold the date of the next new moon
    Days_Till_Next_New_Moon = []                    # this will hold the number of days until the next new moon
    Next_Full_Moon_Date = []                        # this will hold the date of the next full moon
    Days_Till_Next_Full_Moon = []                   # this will hold the number of days until the next full moon             
    Prev_New_Moon_Date = []                         # this will hold the date of the previous new moon
    Days_Since_Prev_New_Moon = []                   # this will hold the number of days since the last new moon
    Prev_Full_Moon_Date = []                        # this will hold the date of the previous full moon
    Days_Since_Prev_Full_Moon = []                  # this will hold the number of days since the last new moon
    
    print("Begin Web Scraping")

    # going though each row of the inputted excel sheet
    for ind in df.index:
        print("Current Date", df['Dates'][ind] )
        year = df['Dates'][ind][:4]                 # storing year
        month = df['Dates'][ind][5:7]               # storing month
        day = df['Dates'][ind][8:10]                # storing day
        data_time = df['Dates'][ind][11:16]         # storing time hh:mm

        url = "https://www.mooncalc.org/#/" + latitiude + "," + longitude + ",3/" + year + "." + month + "." + day + "/" + data_time +"/1/3"
        print("URL: ", url)
        URL.append(url)                             # Adding constructed URL to list 
        
        driver.get(url)                             # searching using our constructed URL
        time.sleep(.25)                             # need a little bit to wait to make sure we have finished grabbing the values
        
        # insert html into soup so that we can search for the data we want
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Grabbing The Moon Rise Time
        Moon_Rs = soup.find('span', id='clickSunrise').contents[0]  # Grabbing data from the html file (using known id)
        Moon_Rise.append(Moon_Rs)                                   # append data to ther proper list

        # Grabbing the Moon Culmination
        Moon_Cul = soup.find('span', id='clickSunrise').contents[0] # Grabbing data from the html file (using known id)
        Moon_Culmination.append(Moon_Cul)                           # append data to the proper list

        # Grabbing the moon set 
        Moon_St = soup.find('span', id='clickSunset').contents[0]   # Grabbing data from the html file (using known id)
        Moon_Set.append(Moon_St)                                    # append data to the proper list

        # Grabbing the moon distance
        Moon_Dist = soup.find('span', {"class":"time-span twilight dawn-time"}).contents[0] # Grabbing data from the html file (based on class)
        Moon_Dist = Moon_Dist.replace("km", "")                                             # Getting rid of the km from the data 
        Moon_Distance.append(Moon_Dist)                                                     # append data to the proper lsit

        # Grabbing the moon altitude
        Moon_Alt = soup.find('span', id="sunhoehe").contents[0]     # Grabbing data from the html file (using known id)
        Moon_Alt = Moon_Alt.replace("°","")                         # getting rid of °
        Moon_Altitude.append(Moon_Alt)                              # append data to proper list

        # Grabbing the moon azimuth
        Moon_Azi = soup.find('span', id='azimuth').contents[0]      # Grabbing data from the html file (using known id)
        Moon_Azi = Moon_Azi.replace("°","")                         # Getting rid of °
        Moon_Azimuth.append(Moon_Azi)                               # append data to proper list
        
        # Grabbing both the moon Phase and Moon Illumination
        Phase_and_Illumination = soup.find('span', {"class":"moontext dusk-time"}).contents[0].split('/')   # Grabbing data from the html file (based on the class)
        Moon_Phase.append(Phase_and_Illumination[0])                                                        # inputting Phase into proper list
        Phase_and_Illumination[1] = Phase_and_Illumination[1].replace("%","")                               # Getting rid of % in result
        Disk_Illumination.append(Phase_and_Illumination[1])                                                 # inputting Illumination into proper list
        
        # Calculations

        Current_Date = df['Dates'][ind][:10]                        # grabbing the date we are working on
        
        # Calculation for Next New Moon (Date + Days Till)
        New_Moon = soup.find('span', {"class":"moontext neumond"}).contents[0]  # Grabbing data from the html file (based on the class)
        New_Moon = New_Moon.split(" ")                                          # Splitting data based on format: Next_NM_Date Time_Until
        Next_NM_DT= New_Moon[0].split(".")                                      # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_NM_DT = Next_NM_DT[2] + "-" + Next_NM_DT[1] + "-" + Next_NM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_New_Moon_Date.append(Next_NM_DT)                                   # Appending Next New Moon Date to Proper List
        Next_NM_Days = days_between(Current_Date, Next_NM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_New_Moon.append(Next_NM_Days)                            # Appending Days between next New Moon + Inputted date to proper list
        
        # Calculation for Next Full Moon (Date + Days Till)
        Full_Moon = soup.find('span', {"class":"moontext vollmond"}).contents[0]# Grabbing data from the html file (based on the class)
        Full_Moon = Full_Moon.split(" ")                                        # Splitting data based on format: Next_FM_Date Time_Until
        Next_FM_DT = Full_Moon[0].split('.')                                    # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_FM_DT = Next_FM_DT[2] + "-" + Next_FM_DT[1] + "-" + Next_FM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_Full_Moon_Date.append(Next_FM_DT)                                  # appending Next Full Moon Date to proper list
        Next_FM_Days = days_between(Current_Date, Next_FM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_Full_Moon.append(Next_FM_Days)                           # Appending Days between next Full Moon + Inputted date to proper list
        
        # Calculation for Prev New Moon
        Lunar_Phase = 29         

        Prev_NM_DT = subtract_days(Next_NM_DT, Lunar_Phase)[:10]                # calculating date of previous new moon via inputting: next one - lunar phase
        
        Prev_New_Moon_Date.append(Prev_NM_DT)                                   # appending Previous New Moon Date into proper list
        Prev_NM_Days = days_between(Current_Date, Prev_NM_DT)                   # calculating the number of days between the inputted date and the date of previous new moon
        Days_Since_Prev_New_Moon.append(Prev_NM_Days)                           # Appending Days between previous New Moon + Inputted date to proper list
        
        # Calculation for Prev Full Moon
        Prev_FM_DT = subtract_days(Next_FM_DT, Lunar_Phase)[:10]                # calculating date of previous full moon via inputting: next one - lunar phase             
        
        Prev_Full_Moon_Date.append(Prev_FM_DT)                                  # appending Previous Full Moon Date into proper list
        Prev_FM_Days = days_between(Current_Date, Prev_FM_DT)                   # calculating the number of days between the inputted date and the date of previous full moon
        Days_Since_Prev_Full_Moon.append(Prev_FM_Days)                          # Appending Days between previous Full Moon + Inputted date to proper list
        
        
        driver.delete_all_cookies()
        # Loop Complete, onto the next row + URL

    print("Complete Web Scraping")

    driver.quit()                       # close out driver
    
    print("Driver Closed")
    
    # creating our final daraframe 
    df_final = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates, "Moon Rise":Moon_Rise, "Moon Culmination":Moon_Culmination,
                             "Moon Set":Moon_Set, "Moon Distance (km)":Moon_Distance,"Moon Altitude (°)":Moon_Altitude,
                             "Moon Azimuth (°)":Moon_Azimuth, "Moon Phase":Moon_Phase,"Disk Illumination (%)":Disk_Illumination,
                             "Next New Moon Date":Next_New_Moon_Date, "Days Till Next New Moon":Days_Till_Next_New_Moon,
                             "Next Full Moon Date":Next_Full_Moon_Date, "Days Till Full New Moon":Days_Till_Next_Full_Moon,
                             "Prev New Moon Date":Prev_New_Moon_Date, "Days Since New Moon":Days_Since_Prev_New_Moon,
                             "Prev Full Moon Date":Prev_Full_Moon_Date, "Days Since Full New Moon":Days_Since_Prev_Full_Moon,
                             "URL":URL})
    
    # created the moon scrape dataframe, now adding it to excel sheet
    filename = File_Name.rsplit("/", 1)
    print(filename[0] + new_excel_name + ".xlsx")
    df_final.to_excel(filename[0]  + "/" + new_excel_name + ".xlsx")


    print("Scraping of Moon Data Complete!!!")

    return

def L_excel_to_new_excel_Moon_Data(File_Name:str, Sheet_Name:str, Date_Column:str, Comment_Column:str, Latitude_Col_Name:str, Longitude_Col_Name:str, new_excel_name:str):
    """
    In this function, we intake an excel file that may contain several sheets with lots if information. We are looking to 
    we want to grab dates and comments from the sheet name we are inputting, and then adding them into a new dataframe.
    Once that is done, we activate the chrome driver and begin constructing URLs so that we can grab the data we want from 
    the website. We grab each url, parse the html to grab the data we need, and insert it into our dataframe. We finish by 
    exiting the chrome driver, inserting all of the scraped data into our dataframes, and input it into a new excel sheet. 
    INPUTS:
        File_Name: Name of the .excl file we want to grab moon data for
        Sheet_Name: The sheet in the file where we will grab our initial data
        Date_Column: The column that contains the date we want to scrape data for 
        Comment_Column: The column that contains comments associated with dates
        Latitude_Col_Name: string representing the latitude of the aquarium where the data was recorded
        Longitude_Col_Name: string representing the longitude of the aquarium where the data was recorded
        new_excel_name: string representing the name of the sheet we will be newly generating
    OUTPUT:
        We want to create a new spread sheet containing the moon data for all of the dates recorded
        in the docx file. 
    """
    df = pd.read_excel(io=File_Name, sheet_name=Sheet_Name)

    Dates = []                                      # Will store the dates we want to scrape from site
    Descriptions = []                               # Will store the descriptions we want to scrape from site
    Longitude = []
    Latitude = []

    for ind in df.index:                            # going through our document and grabbing each line
        date = str(df[Date_Column][ind])            # grabbing the dates, placing in variable
        desc = df[Comment_Column][ind]
        lat = str(df[Latitude_Col_Name][ind])
        long = str(df[Longitude_Col_Name][ind])

        if (date=="" and desc==""):    # we got all the dates, the rest of the cols don't matter
            break
        if (date== "NaT"):
            pass
        else:
            Dates.append(date)
            Descriptions.append(desc)
            Latitude.append(lat)
            Longitude.append(long)


    # creating a dataframe 
    df = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates, "Latitude":Latitude, "Longitude":Longitude})

    print("Setting Up Web Driver")

    driver = webdriver.Chrome()                     # creating a chrome webdriver 
    driver.minimize_window()                        # minimizing the window so that it is not blocking the screen

    print("Web Driver Set Up Complete")

    # These are all of the lists that will hold the data that we scrape
    URL = []                                        # this will hold the URL used to scrape the data
    Moon_Rise = []                                  # this will hold the time that the moon rose that day
    Moon_Culmination = []                           # this will hold the the time the moon passes over the meridian (culmination)
    Moon_Set = []                                   # this will hold the time when the moon touches the horizon
    Moon_Distance = []                              # this will hold the distance the moon is from the earth
    Moon_Altitude = []                              # this will hold the Altitude: The angle between the center of moon and the horizon including refraction.
    Moon_Azimuth = []                               # this will hold the Azimuth: The angle between the meridional plane of the earth and the vertical plane of the moon.
    Moon_Phase = []                                 # this will hold the moon phase
    Disk_Illumination = []                          # this will hold the percentage of the disk that is illuminated
    # Calculations
    Next_New_Moon_Date = []                         # this will hold the date of the next new moon
    Days_Till_Next_New_Moon = []                    # this will hold the number of days until the next new moon
    Next_Full_Moon_Date = []                        # this will hold the date of the next full moon
    Days_Till_Next_Full_Moon = []                   # this will hold the number of days until the next full moon             
    Prev_New_Moon_Date = []                         # this will hold the date of the previous new moon
    Days_Since_Prev_New_Moon = []                   # this will hold the number of days since the last new moon
    Prev_Full_Moon_Date = []                        # this will hold the date of the previous full moon
    Days_Since_Prev_Full_Moon = []                  # this will hold the number of days since the last new moon
    
    print("Begin Web Scraping")

    # going though each row of the inputted excel sheet
    for ind in df.index:
        print("Current Date", df['Dates'][ind] )
        year = df['Dates'][ind][:4]                 # storing year of the current row
        month = df['Dates'][ind][5:7]               # storing month of the current row
        day = df['Dates'][ind][8:10]                # storing day of the current row
        data_time = df['Dates'][ind][11:16]         # storing time hh:mm of the current row
        latitude = df["Latitude"][ind]              # stores the latitude of the current row
        longitude = df['Longitude'][ind]            # stores the longitude of the current row

        url = "https://www.mooncalc.org/#/" + latitude + "," + longitude + ",3/" + year + "." + month + "." + day + "/" + data_time +"/1/3"
        URL.append(url)                             # Adding constructed URL to list 
        
        driver.get(url)                             # searching using our constructed URL
        time.sleep(.25)                             # need a little bit to wait to make sure we have finished grabbing the values
        
        # insert html into soup so that we can search for the data we want
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Grabbing The Moon Rise Time
        Moon_Rs = soup.find('span', id='clickSunrise').contents[0]  # Grabbing data from the html file (using known id)
        Moon_Rise.append(Moon_Rs)                                   # append data to ther proper list

        # Grabbing the Moon Culmination
        Moon_Cul = soup.find('span', id='clickSunrise').contents[0] # Grabbing data from the html file (using known id)
        Moon_Culmination.append(Moon_Cul)                           # append data to the proper list

        # Grabbing the moon set 
        Moon_St = soup.find('span', id='clickSunset').contents[0]   # Grabbing data from the html file (using known id)
        Moon_Set.append(Moon_St)                                    # append data to the proper list

        # Grabbing the moon distance
        Moon_Dist = soup.find('span', {"class":"time-span twilight dawn-time"}).contents[0] # Grabbing data from the html file (based on class)
        Moon_Dist = Moon_Dist.replace("km", "")                                             # Getting rid of the km from the data 
        Moon_Distance.append(Moon_Dist)                                                     # append data to the proper lsit

        # Grabbing the moon altitude
        Moon_Alt = soup.find('span', id="sunhoehe").contents[0]     # Grabbing data from the html file (using known id)
        Moon_Alt = Moon_Alt.replace("°","")                         # getting rid of °
        Moon_Altitude.append(Moon_Alt)                              # append data to proper list

        # Grabbing the moon azimuth
        Moon_Azi = soup.find('span', id='azimuth').contents[0]      # Grabbing data from the html file (using known id)
        Moon_Azi = Moon_Azi.replace("°","")                         # Getting rid of °
        Moon_Azimuth.append(Moon_Azi)                               # append data to proper list
        
        # Grabbing both the moon Phase and Moon Illumination
        Phase_and_Illumination = soup.find('span', {"class":"moontext dusk-time"}).contents[0].split('/')   # Grabbing data from the html file (based on the class)
        Moon_Phase.append(Phase_and_Illumination[0])                                                        # inputting Phase into proper list
        Phase_and_Illumination[1] = Phase_and_Illumination[1].replace("%","")                               # Getting rid of % in result
        Disk_Illumination.append(Phase_and_Illumination[1])                                                 # inputting Illumination into proper list
        
        # Calculations

        Current_Date = df['Dates'][ind][:10]                        # grabbing the date we are working on
        
        # Calculation for Next New Moon (Date + Days Till)
        New_Moon = soup.find('span', {"class":"moontext neumond"}).contents[0]  # Grabbing data from the html file (based on the class)
        New_Moon = New_Moon.split(" ")                                          # Splitting data based on format: Next_NM_Date Time_Until
        Next_NM_DT= New_Moon[0].split(".")                                      # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_NM_DT = Next_NM_DT[2] + "-" + Next_NM_DT[1] + "-" + Next_NM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_New_Moon_Date.append(Next_NM_DT)                                   # Appending Next New Moon Date to Proper List
        Next_NM_Days = days_between(Current_Date, Next_NM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_New_Moon.append(Next_NM_Days)                            # Appending Days between next New Moon + Inputted date to proper list
        
        # Calculation for Next Full Moon (Date + Days Till)
        Full_Moon = soup.find('span', {"class":"moontext vollmond"}).contents[0]# Grabbing data from the html file (based on the class)
        Full_Moon = Full_Moon.split(" ")                                        # Splitting data based on format: Next_FM_Date Time_Until
        Next_FM_DT = Full_Moon[0].split('.')                                    # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_FM_DT = Next_FM_DT[2] + "-" + Next_FM_DT[1] + "-" + Next_FM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_Full_Moon_Date.append(Next_FM_DT)                                  # appending Next Full Moon Date to proper list
        Next_FM_Days = days_between(Current_Date, Next_FM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_Full_Moon.append(Next_FM_Days)                           # Appending Days between next Full Moon + Inputted date to proper list
        
        # Calculation for Prev New Moon
        Lunar_Phase = 29         

        Prev_NM_DT = subtract_days(Next_NM_DT, Lunar_Phase)[:10]                # calculating date of previous new moon via inputting: next one - lunar phase
        
        Prev_New_Moon_Date.append(Prev_NM_DT)                                   # appending Previous New Moon Date into proper list
        Prev_NM_Days = days_between(Current_Date, Prev_NM_DT)                   # calculating the number of days between the inputted date and the date of previous new moon
        Days_Since_Prev_New_Moon.append(Prev_NM_Days)                           # Appending Days between previous New Moon + Inputted date to proper list
        
        # Calculation for Prev Full Moon
        Prev_FM_DT = subtract_days(Next_FM_DT, Lunar_Phase)[:10]                # calculating date of previous full moon via inputting: next one - lunar phase             
        
        Prev_Full_Moon_Date.append(Prev_FM_DT)                                  # appending Previous Full Moon Date into proper list
        Prev_FM_Days = days_between(Current_Date, Prev_FM_DT)                   # calculating the number of days between the inputted date and the date of previous full moon
        Days_Since_Prev_Full_Moon.append(Prev_FM_Days)                          # Appending Days between previous Full Moon + Inputted date to proper list
        
        
        driver.delete_all_cookies()
        # Loop Complete, onto the next row + URL

    print("Complete Web Scraping")

    driver.quit()                       # close out driver
    
    print("Driver Closed")
    
    # creating our final daraframe 
    df_final = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates, "Moon Rise":Moon_Rise, "Moon Culmination":Moon_Culmination,
                             "Moon Set":Moon_Set, "Moon Distance (km)":Moon_Distance,"Moon Altitude (°)":Moon_Altitude,
                             "Moon Azimuth (°)":Moon_Azimuth, "Moon Phase":Moon_Phase,"Disk Illumination (%)":Disk_Illumination,
                             "Next New Moon Date":Next_New_Moon_Date, "Days Till Next New Moon":Days_Till_Next_New_Moon,
                             "Next Full Moon Date":Next_Full_Moon_Date, "Days Till Full New Moon":Days_Till_Next_Full_Moon,
                             "Prev New Moon Date":Prev_New_Moon_Date, "Days Since New Moon":Days_Since_Prev_New_Moon,
                             "Prev Full Moon Date":Prev_Full_Moon_Date, "Days Since Full New Moon":Days_Since_Prev_Full_Moon,
                             "URL":URL})
    
    # created the moon scrape dataframe, now adding it to excel sheet
    filename = File_Name.rsplit("/", 1)
    print(filename[0] + new_excel_name + ".xlsx")
    df_final.to_excel(filename[0]  + "/" + new_excel_name + ".xlsx")


    print("Scraping of Moon Data Complete!!!")

    return

def excel_to_new_sheet_Moon_Data(File_Name:str, Sheet_Name:str, Date_Column_Name:str, Comment_Column:str, latitiude:str, longitude:str, New_Sheet_Name:str):
    """
    In this function, we intake an excel file that may contain several sheets with lots if information. We are looking to 
    we want to grab dates and comments from the sheet name we are inputting, and then adding them into a new dataframe.
    Once that is done, we activate the chrome driver and begin constructing URLs so that we can grab the data we want from 
    the website. We grab each url, parse the html to grab the data we need, and insert it into our dataframe. We finish by 
    exiting the chrome driver, inserting all of the scraped data into our dataframes, and input it into a new sheet on the
    old excel sheet. 
    INPUTS:
        File_Name: Name of the .excl file we want to grab moon data for
        Sheet_Name: The sheet in the file where we will grab our initial data
        Date_Column: The column that contains the date we want to scrape data for 
        Comment_Column: The column that contains comments associated with dates
        latitude: string representing the latitude of the aquarium where the data was recorded
        longitude: string representing the longitude of the aquarium where the data was recorded
    OUTPUT:
        We want to add a sheet to the inputted spread sheet containing the moon data for all of the dates recorded
        in the excel file. 
    """
    df = pd.read_excel(io=File_Name, sheet_name=Sheet_Name)

    Dates = []
    Descriptions = []

    for ind in df.index:                            # going through our document and grabbing each line
        date = str(df[Date_Column_Name][ind])            # grabbing the dates, placing in variable
        desc = df[Comment_Column][ind]

        if (date=="" and desc==""):    # we got all the dates, the rest of the cols don't matter
            break
        if (date== "NaT"): # this means the cell was empty 
            pass
        else:
            Dates.append(date)
            Descriptions.append(desc)

    df = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates})
    
    print("Setting Up Web Driver")

    driver = webdriver.Chrome()                     # creating our web driver
    driver.minimize_window()                        # minimizing the window so that it is not blocking the screen

    print("Web Driver Set Up Complete")

    # These are all of the lists that will hold the data that we scrape
    URL = []                                        # this will hold the URL used to scrape the data
    Moon_Rise = []                                  # this will hold the time that the moon rose that day
    Moon_Culmination = []                           # this will hold the the time the moon passes over the meridian (culmination)
    Moon_Set = []                                   # this will hold the time when the moon touches the horizon
    Moon_Distance = []                              # this will hold the distance the moon is from the earth
    Moon_Altitude = []                              # this will hold the Altitude: The angle between the center of moon and the horizon including refraction.
    Moon_Azimuth = []                               # this will hold the Azimuth: The angle between the meridional plane of the earth and the vertical plane of the moon.
    Moon_Phase = []                                 # this will hold the moon phase
    Disk_Illumination = []                          # this will hold the percentage of the disk that is illuminated
    # Calculations
    Next_New_Moon_Date = []                         # this will hold the date of the next new moon
    Days_Till_Next_New_Moon = []                    # this will hold the number of days until the next new moon
    Next_Full_Moon_Date = []                        # this will hold the date of the next full moon
    Days_Till_Next_Full_Moon = []                   # this will hold the number of days until the next full moon             
    Prev_New_Moon_Date = []                         # this will hold the date of the previous new moon
    Days_Since_Prev_New_Moon = []                   # this will hold the number of days since the last new moon
    Prev_Full_Moon_Date = []                        # this will hold the date of the previous full moon
    Days_Since_Prev_Full_Moon = []                  # this will hold the number of days since the last new moon
    
    print("Begin Web Scraping")

    # Moving through initial dataframe to scrape for each date
    for ind in df.index:
        year = df['Dates'][ind][:4]
        month = df['Dates'][ind][5:7]
        day = df['Dates'][ind][8:10]
        data_time = df['Dates'][ind][11:16]

        url = "https://www.mooncalc.org/#/" + latitiude + "," + longitude + ",3/" + year + "." + month + "." + day + "/" + data_time +"/1/3"
        URL.append(url)                             # Adding constructed URL to list 
        
        driver.get(url)                             # searching using our constructed URL
        time.sleep(.25)                             # need a little bit to wait to make sure we have finished grabbing the values
        
        # insert html into soup so that we can search for the data we want
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Grabbing The Moon Rise Time
        Moon_Rs = soup.find('span', id='clickSunrise').contents[0]  # Grabbing data from the html file (using known id)
        Moon_Rise.append(Moon_Rs)                                   # append data to ther proper list

        # Grabbing the Moon Culmination
        Moon_Cul = soup.find('span', id='clickSunrise').contents[0] # Grabbing data from the html file (using known id)
        Moon_Culmination.append(Moon_Cul)                           # append data to the proper list

        # Grabbing the moon set 
        Moon_St = soup.find('span', id='clickSunset').contents[0]   # Grabbing data from the html file (using known id)
        Moon_Set.append(Moon_St)                                    # append data to the proper list

        # Grabbing the moon distance
        Moon_Dist = soup.find('span', {"class":"time-span twilight dawn-time"}).contents[0] # Grabbing data from the html file (based on class)
        Moon_Dist = Moon_Dist.replace("km", "")                                             # Getting rid of the km from the data 
        Moon_Distance.append(Moon_Dist)                                                     # append data to the proper lsit

        # Grabbing the moon altitude
        Moon_Alt = soup.find('span', id="sunhoehe").contents[0]     # Grabbing data from the html file (using known id)
        Moon_Alt = Moon_Alt.replace("°","")                         # getting rid of °
        Moon_Altitude.append(Moon_Alt)                              # append data to proper list

        # Grabbing the moon azimuth
        Moon_Azi = soup.find('span', id='azimuth').contents[0]      # Grabbing data from the html file (using known id)
        Moon_Azi = Moon_Azi.replace("°","")                         # Getting rid of °
        Moon_Azimuth.append(Moon_Azi)                               # append data to proper list
        
        # Grabbing both the moon Phase and Moon Illumination
        Phase_and_Illumination = soup.find('span', {"class":"moontext dusk-time"}).contents[0].split('/')   # Grabbing data from the html file (based on the class)
        Moon_Phase.append(Phase_and_Illumination[0])                                                        # inputting Phase into proper list
        Phase_and_Illumination[1] = Phase_and_Illumination[1].replace("%","")                               # Getting rid of % in result
        Disk_Illumination.append(Phase_and_Illumination[1])                                                 # inputting Illumination into proper list
        
        # Calculations

        Current_Date = df['Dates'][ind][:10]                        # grabbing the date we are working on
        
        # Calculation for Next New Moon (Date + Days Till)
        New_Moon = soup.find('span', {"class":"moontext neumond"}).contents[0]  # Grabbing data from the html file (based on the class)
        New_Moon = New_Moon.split(" ")                                          # Splitting data based on format: Next_NM_Date Time_Until
        Next_NM_DT= New_Moon[0].split(".")                                      # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_NM_DT = Next_NM_DT[2] + "-" + Next_NM_DT[1] + "-" + Next_NM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_New_Moon_Date.append(Next_NM_DT)                                   # Appending Next New Moon Date to Proper List
        Next_NM_Days = days_between(Current_Date, Next_NM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_New_Moon.append(Next_NM_Days)                            # Appending Days between next New Moon + Inputted date to proper list
        
        # Calculation for Next Full Moon (Date + Days Till)
        Full_Moon = soup.find('span', {"class":"moontext vollmond"}).contents[0]# Grabbing data from the html file (based on the class)
        Full_Moon = Full_Moon.split(" ")                                        # Splitting data based on format: Next_FM_Date Time_Until
        Next_FM_DT = Full_Moon[0].split('.')                                    # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_FM_DT = Next_FM_DT[2] + "-" + Next_FM_DT[1] + "-" + Next_FM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_Full_Moon_Date.append(Next_FM_DT)                                  # appending Next Full Moon Date to proper list
        Next_FM_Days = days_between(Current_Date, Next_FM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_Full_Moon.append(Next_FM_Days)                           # Appending Days between next Full Moon + Inputted date to proper list
        
        # Calculation for Prev New Moon
        Lunar_Phase = 29         

        Prev_NM_DT = subtract_days(Next_NM_DT, Lunar_Phase)[:10]                # calculating date of previous new moon via inputting: next one - lunar phase
        
        Prev_New_Moon_Date.append(Prev_NM_DT)                                   # appending Previous New Moon Date into proper list
        Prev_NM_Days = days_between(Current_Date, Prev_NM_DT)                   # calculating the number of days between the inputted date and the date of previous new moon
        Days_Since_Prev_New_Moon.append(Prev_NM_Days)                           # Appending Days between previous New Moon + Inputted date to proper list
        
        # Calculation for Prev Full Moon
        Prev_FM_DT = subtract_days(Next_FM_DT, Lunar_Phase)[:10]                # calculating date of previous full moon via inputting: next one - lunar phase             
        
        Prev_Full_Moon_Date.append(Prev_FM_DT)                                  # appending Previous Full Moon Date into proper list
        Prev_FM_Days = days_between(Current_Date, Prev_FM_DT)                   # calculating the number of days between the inputted date and the date of previous full moon
        Days_Since_Prev_Full_Moon.append(Prev_FM_Days)                          # Appending Days between previous Full Moon + Inputted date to proper list
        
        
        driver.delete_all_cookies()
        # Loop Complete, onto the next row + URL

    print("Complete Web Scraping")

    driver.quit()                           # close out driver

    print("Driver Closed")
    
    # creating a new dataframe
    df_final = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates, "Moon Rise":Moon_Rise, "Moon Culmination":Moon_Culmination,
                             "Moon Set":Moon_Set, "Moon Distance (km)":Moon_Distance,"Moon Altitude (°)":Moon_Altitude,
                             "Moon Azimuth (°)":Moon_Azimuth, "Moon Phase":Moon_Phase,"Disk Illumination (%)":Disk_Illumination,
                             "Next New Moon Date":Next_New_Moon_Date, "Days Till Next New Moon":Days_Till_Next_New_Moon,
                             "Next Full Moon Date":Next_Full_Moon_Date, "Days Till Full New Moon":Days_Till_Next_Full_Moon,
                             "Prev New Moon Date":Prev_New_Moon_Date, "Days Since New Moon":Days_Since_Prev_New_Moon,
                             "Prev Full Moon Date":Prev_Full_Moon_Date, "Days Since Full New Moon":Days_Since_Prev_Full_Moon,
                             "URL":URL})
    
    # created the moon scrape dataframe, now adding it to excel sheet
    with pd.ExcelWriter(
            File_Name,
            mode="a",
            engine="openpyxl",
            if_sheet_exists="replace",
        ) as writer:
        df_final.to_excel(writer, sheet_name=New_Sheet_Name) 

    print("Scraping of Moon Data Complete!!!")
    
    return

def L_excel_to_new_sheet_Moon_Data(File_Name:str, Sheet_Name:str, Date_Column_Name:str, Comment_Column:str, Latitude_Col_Name:str, Longitude_Col_Name:str, New_Sheet_Name:str):
    """
    In this function, we intake an excel file that may contain several sheets with lots if information. We are looking to 
    we want to grab dates and comments from the sheet name we are inputting, and then adding them into a new dataframe.
    Once that is done, we activate the chrome driver and begin constructing URLs so that we can grab the data we want from 
    the website. We grab each url, parse the html to grab the data we need, and insert it into our dataframe. We finish by 
    exiting the chrome driver, inserting all of the scraped data into our dataframes, and input it into a new sheet on the
    old excel sheet. 
    INPUTS:
        File_Name: Name of the .excl file we want to grab moon data for
        Sheet_Name: The sheet in the file where we will grab our initial data
        Date_Column: The column that contains the date we want to scrape data for 
        Comment_Column: The column that contains comments associated with dates
        latitude: string representing the latitude of the aquarium where the data was recorded
        longitude: string representing the longitude of the aquarium where the data was recorded
    OUTPUT:
        We want to add a sheet to the inputted spread sheet containing the moon data for all of the dates recorded
        in the excel file. 
    """
    df = pd.read_excel(io=File_Name, sheet_name=Sheet_Name)

    Dates = []                                      # Will store the dates we want to scrape from site
    Descriptions = []                               # Will store the descriptions we want to scrape from site
    Longitude = []
    Latitude = []

    for ind in df.index:                            # going through our document and grabbing each line
        date = str(df[Date_Column_Name][ind])            # grabbing the dates, placing in variable
        desc = df[Comment_Column][ind]
        lat = str(df[Latitude_Col_Name][ind])
        long = str(df[Longitude_Col_Name][ind])

        if (date=="" and desc==""):    # we got all the dates, the rest of the cols don't matter
            break
        if (date== "NaT"):
            pass
        else:
            Dates.append(date)
            Descriptions.append(desc)
            Latitude.append(lat)
            Longitude.append(long)


    # creating a dataframe 
    df = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates, "Latitude":Latitude, "Longitude":Longitude})
    
    print("Setting Up Web Driver")

    driver = webdriver.Chrome()                     # creating our web driver
    driver.minimize_window()                        # minimizing the window so that it is not blocking the screen

    print("Web Driver Set Up Complete")

    # These are all of the lists that will hold the data that we scrape
    URL = []                                        # this will hold the URL used to scrape the data
    Moon_Rise = []                                  # this will hold the time that the moon rose that day
    Moon_Culmination = []                           # this will hold the the time the moon passes over the meridian (culmination)
    Moon_Set = []                                   # this will hold the time when the moon touches the horizon
    Moon_Distance = []                              # this will hold the distance the moon is from the earth
    Moon_Altitude = []                              # this will hold the Altitude: The angle between the center of moon and the horizon including refraction.
    Moon_Azimuth = []                               # this will hold the Azimuth: The angle between the meridional plane of the earth and the vertical plane of the moon.
    Moon_Phase = []                                 # this will hold the moon phase
    Disk_Illumination = []                          # this will hold the percentage of the disk that is illuminated
    # Calculations
    Next_New_Moon_Date = []                         # this will hold the date of the next new moon
    Days_Till_Next_New_Moon = []                    # this will hold the number of days until the next new moon
    Next_Full_Moon_Date = []                        # this will hold the date of the next full moon
    Days_Till_Next_Full_Moon = []                   # this will hold the number of days until the next full moon             
    Prev_New_Moon_Date = []                         # this will hold the date of the previous new moon
    Days_Since_Prev_New_Moon = []                   # this will hold the number of days since the last new moon
    Prev_Full_Moon_Date = []                        # this will hold the date of the previous full moon
    Days_Since_Prev_Full_Moon = []                  # this will hold the number of days since the last new moon
    
    print("Begin Web Scraping")

    # Moving through initial dataframe to scrape for each date
    for ind in df.index:
        year = df['Dates'][ind][:4]
        month = df['Dates'][ind][5:7]
        day = df['Dates'][ind][8:10]
        data_time = df['Dates'][ind][11:16]
        latitude = df["Latitude"][ind]              # stores the latitude of the current row
        longitude = df['Longitude'][ind]            # stores the longitude of the current row

        url = "https://www.mooncalc.org/#/" + latitude + "," + longitude + ",3/" + year + "." + month + "." + day + "/" + data_time +"/1/3"
        URL.append(url)
        
        driver.get(url)                             # searching using our constructed URL
        time.sleep(.25)                             # need a little bit to wait to make sure we have finished grabbing the values
        
        # insert html into soup so that we can search for the data we want
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # Grabbing The Moon Rise Time
        Moon_Rs = soup.find('span', id='clickSunrise').contents[0]  # Grabbing data from the html file (using known id)
        Moon_Rise.append(Moon_Rs)                                   # append data to ther proper list

        # Grabbing the Moon Culmination
        Moon_Cul = soup.find('span', id='clickSunrise').contents[0] # Grabbing data from the html file (using known id)
        Moon_Culmination.append(Moon_Cul)                           # append data to the proper list

        # Grabbing the moon set 
        Moon_St = soup.find('span', id='clickSunset').contents[0]   # Grabbing data from the html file (using known id)
        Moon_Set.append(Moon_St)                                    # append data to the proper list

        # Grabbing the moon distance
        Moon_Dist = soup.find('span', {"class":"time-span twilight dawn-time"}).contents[0] # Grabbing data from the html file (based on class)
        Moon_Dist = Moon_Dist.replace("km", "")                                             # Getting rid of the km from the data 
        Moon_Distance.append(Moon_Dist)                                                     # append data to the proper lsit

        # Grabbing the moon altitude
        Moon_Alt = soup.find('span', id="sunhoehe").contents[0]     # Grabbing data from the html file (using known id)
        Moon_Alt = Moon_Alt.replace("°","")                         # getting rid of °
        Moon_Altitude.append(Moon_Alt)                              # append data to proper list

        # Grabbing the moon azimuth
        Moon_Azi = soup.find('span', id='azimuth').contents[0]      # Grabbing data from the html file (using known id)
        Moon_Azi = Moon_Azi.replace("°","")                         # Getting rid of °
        Moon_Azimuth.append(Moon_Azi)                               # append data to proper list
        
        # Grabbing both the moon Phase and Moon Illumination
        Phase_and_Illumination = soup.find('span', {"class":"moontext dusk-time"}).contents[0].split('/')   # Grabbing data from the html file (based on the class)
        Moon_Phase.append(Phase_and_Illumination[0])                                                        # inputting Phase into proper list
        Phase_and_Illumination[1] = Phase_and_Illumination[1].replace("%","")                               # Getting rid of % in result
        Disk_Illumination.append(Phase_and_Illumination[1])                                                 # inputting Illumination into proper list
        
        # Calculations

        Current_Date = df['Dates'][ind][:10]                        # grabbing the date we are working on
        
        # Calculation for Next New Moon (Date + Days Till)
        New_Moon = soup.find('span', {"class":"moontext neumond"}).contents[0]  # Grabbing data from the html file (based on the class)
        New_Moon = New_Moon.split(" ")                                          # Splitting data based on format: Next_NM_Date Time_Until
        Next_NM_DT= New_Moon[0].split(".")                                      # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_NM_DT = Next_NM_DT[2] + "-" + Next_NM_DT[1] + "-" + Next_NM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_New_Moon_Date.append(Next_NM_DT)                                   # Appending Next New Moon Date to Proper List
        Next_NM_Days = days_between(Current_Date, Next_NM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_New_Moon.append(Next_NM_Days)                            # Appending Days between next New Moon + Inputted date to proper list
        
        # Calculation for Next Full Moon (Date + Days Till)
        Full_Moon = soup.find('span', {"class":"moontext vollmond"}).contents[0]# Grabbing data from the html file (based on the class)
        Full_Moon = Full_Moon.split(" ")                                        # Splitting data based on format: Next_FM_Date Time_Until
        Next_FM_DT = Full_Moon[0].split('.')                                    # Taking first element of contents, seperating based on periods based on format: MM.DD.YYYY
        Next_FM_DT = Next_FM_DT[2] + "-" + Next_FM_DT[1] + "-" + Next_FM_DT[0]  # Formatting the date into proper format to feed into function
        
        Next_Full_Moon_Date.append(Next_FM_DT)                                  # appending Next Full Moon Date to proper list
        Next_FM_Days = days_between(Current_Date, Next_FM_DT)                   # calculating the number of days between the inputted date and the date of next new moon
        Days_Till_Next_Full_Moon.append(Next_FM_Days)                           # Appending Days between next Full Moon + Inputted date to proper list
        
        # Calculation for Prev New Moon
        Lunar_Phase = 29         

        Prev_NM_DT = subtract_days(Next_NM_DT, Lunar_Phase)[:10]                # calculating date of previous new moon via inputting: next one - lunar phase
        
        Prev_New_Moon_Date.append(Prev_NM_DT)                                   # appending Previous New Moon Date into proper list
        Prev_NM_Days = days_between(Current_Date, Prev_NM_DT)                   # calculating the number of days between the inputted date and the date of previous new moon
        Days_Since_Prev_New_Moon.append(Prev_NM_Days)                           # Appending Days between previous New Moon + Inputted date to proper list
        
        # Calculation for Prev Full Moon
        Prev_FM_DT = subtract_days(Next_FM_DT, Lunar_Phase)[:10]                # calculating date of previous full moon via inputting: next one - lunar phase             
        
        Prev_Full_Moon_Date.append(Prev_FM_DT)                                  # appending Previous Full Moon Date into proper list
        Prev_FM_Days = days_between(Current_Date, Prev_FM_DT)                   # calculating the number of days between the inputted date and the date of previous full moon
        Days_Since_Prev_Full_Moon.append(Prev_FM_Days)                          # Appending Days between previous Full Moon + Inputted date to proper list
        
        
        driver.delete_all_cookies()
        # Loop Complete, onto the next row + URL

    print("Complete Web Scraping")

    driver.quit()                           # close out driver

    print("Driver Closed")
    
    # creating a new dataframe
    df_final = pd.DataFrame({'Descriptions':Descriptions, "Dates":Dates, "Moon Rise":Moon_Rise, "Moon Culmination":Moon_Culmination,
                             "Moon Set":Moon_Set, "Moon Distance (km)":Moon_Distance,"Moon Altitude (°)":Moon_Altitude,
                             "Moon Azimuth (°)":Moon_Azimuth, "Moon Phase":Moon_Phase,"Disk Illumination (%)":Disk_Illumination,
                             "Next New Moon Date":Next_New_Moon_Date, "Days Till Next New Moon":Days_Till_Next_New_Moon,
                             "Next Full Moon Date":Next_Full_Moon_Date, "Days Till Full New Moon":Days_Till_Next_Full_Moon,
                             "Prev New Moon Date":Prev_New_Moon_Date, "Days Since New Moon":Days_Since_Prev_New_Moon,
                             "Prev Full Moon Date":Prev_Full_Moon_Date, "Days Since Full New Moon":Days_Since_Prev_Full_Moon,
                             "URL":URL})
    
    # created the moon scrape dataframe, now adding it to excel sheet
    with pd.ExcelWriter(
            File_Name,
            mode="a",
            engine="openpyxl",
            if_sheet_exists="replace",
        ) as writer:
        df_final.to_excel(writer, sheet_name=New_Sheet_Name) 

    print("Scraping of Moon Data Complete!!!")
    
    return

"""
# Testing Doc to Excel
Latitude = "33.75749697"
Longitude = "-84.389665108"
FN = "GAQ CW11 dropped eggs log.docx"

doc_to_excel_Moon_Data(FN, Latitude, Longitude)

# Testing Excel to New Excel
Latitude = "32.8678"
Longitude = "-117.2496"
FN = "Tester.xlsx"
SN = "Sheet1"
DC = 'EggDrop/TransferDate'
CC = "Comments"

excel_to_new_sheet_Moon_Data(FN, SN, DC, CC, Latitude, Longitude)

# Testing Excel to New Sheet in Established Excel
Latitude = "32.8678"
Longitude = "-117.2496"
FN = "Birch Egg Transfers and drops.xlsx"
SN = "Egg Drops Reformatted by Nancy"
DC = 'EggDrop/TransferDate'
CC = "Comments"

excel_to_prev_excel_Moon_Data(FN, SN, DC, CC, Latitude, Longitude)
"""