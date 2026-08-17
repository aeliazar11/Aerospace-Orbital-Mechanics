import ephem 
import matplotlib.pyplot as plt
from datetime import datetime 
from skyfield.api import utc, load, Topos

station_data = load.tle('https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle')
iss = station_data['ISS (ZARYA)']
print(iss)

## Change to your specified time range. Current: 2 hours
time_scale = load.timescale()
minutes = range(60 * 2)
time_range = time_scale.utc(2026, 8, 12, 3, minutes)

altitudes = []
azimuths = []
for t in time_range: 
    # Calculate satellite position at each time step
    port_hedland = Topos(latitude='20.3123 S', longitude='118.64498 E')
    orbit = (iss - port_hedland).at(t)
    altitude, azimuth, distance = orbit.altaz()

    # Append the altitude and azimuth values to the lists
    altitudes.append(altitude.degrees)
    azimuths.append(azimuth.degrees)

plt.figure(figsize=(10, 5))
plt.plot(azimuths, altitudes, marker='o', linestyle='-')
plt.title("Satellite Path - ISS")
plt.xlabel("Azimuth (degrees)")
plt.ylabel("Altitude (degrees)")
plt.grid(True)
plt.show()


# Polar Plot Of Passes using Skyfield
from skyfield import api
from pytz import timezone
import numpy as np

## Change to time zone
time_zone = timezone('US/Central')

station_data = load.tle('https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=tle')
iss = station_data['ISS (ZARYA)']
print(iss)

# Current time range (in minutes) = 2 days
time_scale = load.timescale()
minutes = range(60 * 24 * 2)
time_range = time_scale.utc(2026, 8, 12, 3, minutes)
port_hedland = api.Topos(latitude='20.3123 S', longitude='118.64498 E')
orbit = (iss - port_hedland).at(time_range)
altitude, azimuth, distance = orbit.altaz()
print(f"Altitudes: {altitude}")
print(f"Azimuth: {azimuth}")
print(f"Distance: {distance}")

visible_pass = altitude.degrees > 0
indicies, = visible_pass.nonzero()
boundaries, = np.diff(visible_pass).nonzero()
print(boundaries)

boundaries = boundaries
passes = boundaries.reshape(len(boundaries) // 2, 2)
print(passes)

pass_to_observe = 0
specific_pass = passes[pass_to_observe]
rise, set = specific_pass
print(f'ISS Rises at {time_range[0].astimezone(time_zone)}')
print(f'ISS Sets at {time_range[1].astimezone(time_zone)}')

ax = plt.subplot(111, projection='polar')
plt.title("ISS Pass Polar Chart")
ax.set_rlim([0, 100])
ax.set_theta_zero_location('N')
ax.set_theta_direction(-1)

theta = azimuth.radians
r = 90 - altitude.degrees
ax.plot(theta[rise:set], r[rise:set], 'bo--')

for k in range(rise, set):
    text = time_range[k].astimezone(time_zone).strftime('%H:%M')
    ax.text(theta[k], r[k], text, ha='right', va='bottom')
plt.show()
