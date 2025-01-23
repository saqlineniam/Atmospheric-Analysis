import os
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import logging
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def plot_total_precipitation(file_path, date_str, output_dir='plots'):
    try:
        ds = xr.open_dataset(file_path)
        total_precip = ds['tp'].sel(
            latitude=slice(28, 20),
            longitude=slice(85, 94)
        )
        
        times = pd.to_datetime(total_precip.valid_time.values)
        target_date = pd.to_datetime(date_str).date()
        date_indices = [i for i, date in enumerate(times) if date.date() == target_date]
        
        if not date_indices:
            logging.warning(f"No data found for date {target_date}")
            return
        
        daily_precip = total_precip[date_indices].mean(dim='valid_time')
        
        fig = plt.figure(figsize=(18, 12))
        ax = plt.axes(projection=ccrs.PlateCarree())
        
        lons, lats = np.meshgrid(daily_precip.longitude, daily_precip.latitude)
        
        im = ax.contourf(lons, lats,
                        daily_precip.values * 1000,
                        levels=20,
                        cmap='YlGnBu',
                        transform=ccrs.PlateCarree())
        
        ax.coastlines()
        ax.add_feature(cfeature.BORDERS)
        ax.gridlines(draw_labels=True)
        
        ax.set_extent([84, 95, 19, 29])
        
        plt.title(f'Daily Average Precipitation (East of 85°E, South of 28°N)\n{target_date}')
        plt.colorbar(im, label='Precipitation (mm/day)')
        
        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'precip_{target_date}.png')
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        plt.close()
        
        logging.info(f"Plot saved as '{output_file}'")
        
    except Exception as e:
        logging.error(f"Error processing {date_str}: {str(e)}")

def main():
    file_path = "C:/Users/saqli/Desktop/Climate_@/9ac60cdbd23b2d20be022c0614fdbdb4.nc"
    
    # Generate dates from August 6 to August 31
    start_date = datetime(2024, 8, 6)
    end_date = datetime(2024, 8, 31)
    
    current_date = start_date
    while current_date <= end_date:
        date_str = current_date.strftime('%Y-%m-%d')
        logging.info(f"Processing {date_str}")
        plot_total_precipitation(file_path, date_str)
        current_date += timedelta(days=1)

if __name__ == "__main__":
    main()