#Akul Patel, Final Project MATH 4730
#University of Georgia, FALL 2024
#--------------------------------------------------------------#

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns



# Load the dataset
filedata = 'cleaned_data.csv'
data = pd.read_csv(filedata)


# Visualizing the distribution of key parameters related to habitability
sns.histplot(data['st_teff'], kde=True, bins=30, color='blue')
plt.title('Star Temperatures')
plt.xlabel('Temperature in Kelvin')
plt.ylabel('Frequency')
plt.show()


sns.histplot(data['pl_eqt'], kde=True, bins=30, color='red')
plt.title('Equilibriums of Exoplanet Temperatures')
plt.xlabel('Equilibrium Temperatures in Kelvins')
plt.ylabel('Frequency')
plt.show()


# Define constants 
#assume similar albedo and emissivity as that of Earth
sigma = 5.67e-8  #(W/m^2/K^4)
albedo = 0.3  
emissivity = 1.0  

#function to compute surface temperature for exoplanet
def getSurfaceTemp(row):
    if pd.notnull(row['st_teff']) and pd.notnull(row['pl_orbsmax']):
        
        #exoplanet host star properties
        starTemp = row['st_teff'] 
        starRadius = row['st_rad'] * 6.957e8  #in meters

        #get distance to start
        distance = row['pl_orbsmax'] * 1.496e11 #in meters

        #calculate solar constant and luminosity
        #using formula SolarConstant = (Luminosity / 4* pi * distance^2)
        Luminosity = 4 * np.pi * (starRadius**2) * sigma * (starTemp**4)
        
        #check for empty cells and apply formula
        if not np.isnan(distance):
            #get solar constatn
            sConstant = Luminosity / (4 * np.pi * distance**2)
        else: 
            sConstant = np.nan

        #compute suface temperature by [(sConstant*(1-albedo))/(4*sigma)]^(1/4)
        if not np.isnan(sConstant): 
            #get surfacetemp
            surfaceTemp = ((sConstant * (1 - albedo)) / (4 * sigma))**0.25
        else:     
            surfaceTemp = np.nan
        
        return surfaceTemp
        


#apply surface temperature computation to data
data['T_surface'] = data.apply(getSurfaceTemp, axis=1)

#screen for planets that have a temperature from 273 Kelvin to 373 Kelvin, as this assumeed habitable temp.
habitable_planets = data[(data['T_surface'] >= 273) & (data['T_surface'] <= 373)]


#compare to earth by making similar assumputions
#comparing radius, mass, and orbital eccentricity to that of earths
habitable_planets = habitable_planets[(habitable_planets['pl_rade'] >= 0.5) & (habitable_planets['pl_rade'] <= 2) &
    (habitable_planets['pl_bmasse'] >= 0.1) & (habitable_planets['pl_bmasse'] <= 10) &(habitable_planets['pl_orbeccen'] <= 0.2)]

#after planets screened for ones most similar to Earth,
#print list of planets
print(habitable_planets[['pl_name', 'hostname', 'st_teff', 'pl_orbsmax', 'pl_rade', 'pl_bmasse', 'pl_orbeccen', 'T_surface']])


print(habitable_planets['pl_name'])
habitable_planets.to_csv('habitable_planets.csv', index=False)
print("Refined habitable planets saved to 'habitable_planets.csv'.")





#extra plots
#--------------------------------------------------------------------------------------


#CORRELATION HEATMAP

#Features listed in corresponding oreder to majorFeatures

# Orbital period, Semi-major axis ,Planet radius (Earth radii), Planet radius (Jupiter radii), 
# Planet mass (Earth mass), Planet mass (Jupiter mass), Orbital eccentricity, Insolation flux, 
# Equilibrium temperature ,Stellar effective temperature, Stellar radius, Stellar mass, 
# Stellar metallicity, Stellar surface gravity, Distance from Earth

majorFeatures = [
    'pl_orbper', 'pl_orbsmax', 'pl_rade', 'pl_radj', 'pl_bmasse', 'pl_bmassj', 
    'pl_orbeccen', 'pl_insol', 'pl_eqt', 'st_teff', 'st_rad', 'st_mass',    
    'st_met', 'st_logg', 'sy_dist'        
]

#generate matrix
correlation_df = data[majorFeatures].apply(pd.to_numeric, errors='coerce')
correlation_matrix = correlation_df.corr()

#display
plt.figure(figsize=(8, 8))
sns.heatmap(correlation_matrix, annot=True,cmap='RdBu',center=0,fmt='.2f',square=True,)

plt.title('Correlation Matrix')
plt.tight_layout()
plt.show()



#visualizing the distribution of various exoplanet features 

data['temp_celsius'] = data['pl_eqt'].astype(float) - 273.15  # Convert K to C

#4x4 sublot of planetaryt features.
plt.figure(figsize=(15, 10))

#EXOPLANET radius
plt.subplot(221)
sns.histplot(data=data, x='pl_rade', bins=30)
plt.title('Distribution of Exoplanet Radius')
plt.xlabel('Exoplanet Radius')

#comparing temperature vs radius
plt.subplot(222)
sns.scatterplot(data=data, x='pl_rade', y='temp_celsius')
plt.title('Temperature Compared to Radius')
plt.xlabel('Exoplanet Radius')
plt.ylabel('Temperature in °C')

#length of orbital period
plt.subplot(223)
sns.histplot(data=data, x='pl_orbper', bins=30)
plt.title('Distribution of Orbital Periods')
plt.xlabel('Orbital Period (days)')

#when the exoplanets were found
plt.subplot(224)
sns.countplot(data=data, x='disc_year')
plt.title('Discoveries per Year')
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
