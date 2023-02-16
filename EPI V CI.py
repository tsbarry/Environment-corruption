from sqlalchemy import create_engine, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import pandas as pd
import matplotlib.pyplot as plt

#connect to databse and create an epi object
engine = create_engine('postgresql+psycopg2://postgres:thierno@localhost:5432/epi')
Base = automap_base()
Base.prepare(engine, reflect=True)
epi_country = Base.classes.epi_country 
session = Session(engine) 

#requesting data from the table epi_country
country_epi_data = session.query(epi_country.country, epi_country.air_h, epi_country.population07, epi_country.water_h, epi_country.biodiversity, epi_country.fisheries, epi_country.geo_subregion)
rows_epi = country_epi_data.all()
print(rows_epi)

#saving epi_country into a pandas dataframe
epi_df = pd.DataFrame(rows_epi, columns=['country', 'air_h', 'population07', 'water_h', 'biodiversity', 'fisheries', 'geo_subregion'])
print(epi_df)

#filter epi data to get data for the geographical subregion of Western Africa 
epi_wa = epi_df[epi_df["geo_subregion"] == "Western Africa"]
print(epi_wa)

# read the CPI csv file into a pandas dataframe
cpi_df = pd.read_csv('CPI-2010-new_200601_105629.csv') 
print(cpi_df)

cpi_df.head()

null_val= cpi_df.dropna(inplace=True)
print(null_val)

#using the dataframe to create a table in sql using the pandas to_sql method
cpi_df.to_sql('corruption', engine)

#join epi and cpi using left join, joining on country 
cpi_epi = epi_wa.merge(cpi_df, how='left', on='country')
print(cpi_epi)
null= cpi_epi.dropna(inplace=True)
print(null)

#visualization that describe the relationship between countries and its corruption rank 
rank_sorted = cpi_epi.sort_values(by='rank', ascending=False)
rank_bar= rank_sorted.head(20).plot.bar(x='country', y='rank', title= 'countries rank in corruption')
print(rank_bar)
plt.savefig('countryrank.png') 

#visualization that describe the relationship between countries and its corruption score 
rank_sorted = cpi_epi.sort_values(by='score', ascending=False)
bar = rank_sorted.head(20).plot.bar(x='country', y='score', title= 'countries score in corruption') 
print(bar)
plt.savefig('countryscore.png')

#visualization that describe the relationship between corruption score and water health
water_score = cpi_epi.plot.scatter(x='score', y='water_h', title= 'corruption score v water health')
print(water_score)
plt.savefig('waterscore.png') 

#visualization that describe the relationship between corruption rank and air health
air_rank = cpi_epi.plot.scatter(x='rank', y='air_h', title= 'corruption rank v air health')
print(air_rank)
plt.savefig('airrank.png')

#histogram that display the correlation between countries and water health
epi_wa['water_h'].plot.hist(bins=50)
plt.savefig('histwater_h.png')

engine.dispose()  