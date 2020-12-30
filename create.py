import math
from typing import List, Tuple
import simplejson as json
import numpy as np
from svgwrite import drawing

# Budapest: 47.496215, 19.033440
# Pécs: 46.079573, 18.234001

def resample_to_points(elevations: np.ndarray, n_points: int, original_distances: np.ndarray = None) -> np.ndarray:
    # Resample elevations. Original distances must be in the 0...1 range
    # If original_distances is None, assumes equally distributed distances.
    n_orig = len(elevations)
    if original_distances is None:
        original_distances = np.linspace(0, 1, n_orig)
    return np.interp(
        np.linspace(0, 1, n_points), # query points
        original_distances,  # original X points
        elevations)

def normalize_elevations(elevations: List[float], min_height: float=10.0, multiplier: float=30.0) -> List[float]:
    e_max = max(elevations)
    e_min = min(elevations)
    elevations = [10 + 30 * (e - e_min) / (e_max - e_min)
        for e in elevations]
    return elevations


def create_stl(elevations, filename: str, n_points=100) -> None:
    # create STL model for 3D printing
    import stl
    # normalize elevations
    elevations = normalize_elevations(elevations, 10.0, 30,0)
    lengths = [180.0 / len(elevations) for pt in elevations]

    model = stl.Solid(filename.replace("json", "stl").replace("gpx", "stl"))
    hills = stl.Feature(stl.Vector(0, 0, 0), stl.Coords.X, 30.0, lengths, elevations)
    model.add(hills)
    model.write()


def create_svg(elevations: List[float], filename: str, n_points=100) -> None:
    # create SVG file for laser cutting
    elevations = normalize_elevations(elevations, 10.0, 30.0)
    step = 180.0 / len(elevations)

    import svgwrite
    file = svgwrite.Drawing(filename=filename)


    # helper function to draw line
    def line(x0, y0, x1, elevation):
        from svgwrite import mm
        file.add(file.line(start=(x0*mm, y0*mm), end=(x1*mm, elevation*mm),
            stroke="red", stroke_width=0.5*mm))
        return elevation
    
    # draw hills
    prev_elev = elevations[0]
    for i, elev in enumerate(elevations[1:]):
        prev_elev = line(i*step, prev_elev, (i+1)*step, elev)
    
    # draw box
    end_x = (len(elevations)-1) * step
    end_y = elevations[-1]
    line(0, 0, end_x, 0) # horizontal bottom
    line(0, 0, 0, elevations[0]) # vertical left
    line(end_x, 0, end_x, end_y) # vertical right
    file.save()



def elev_from_json(filename: str) -> Tuple[List[float], None]:
    # get elevations from json
    with open(filename, "r") as reader:
        response = reader.read()
    points = json.loads(response)["results"]
    elevations = [pt["elevation"] for pt in points]
    return (elevations, None)


def elev_from_gpx(filename: str) -> Tuple[List[float], List[float]]:
    import gpxpy # https://pypi.org/project/gpxpy/
    import gpxpy.gpx
    gpx = gpxpy.parse(open(filename, "r"))
    points = gpx.tracks[0].segments[0].points

    # when importing from json, the elevations are surely equally distributed over the distance
    # When importing from GPX, this is not the case,so we have to calculate distances and interpolate
    # https://stackoverflow.com/questions/27928/calculate-distance-between-two-latitude-longitude-points-haversine-formula
    lats = np.array([point.latitude * math.pi / 180.0 for point in points])
    lons = np.array([point.longitude * math.pi / 180.0 for point in points])
    elevs = np.array([point.elevation for point in points])

    dLat = np.diff(lats)
    dLon = np.diff(lons)
    R = 6371.0 # Radius of the earth in kilometres

    a = np.sin(dLat/2) * np.sin(dLat/2) + \
        np.cos(lats[:-1]) * np.cos(lats[1:]) * \
        np.sin(dLon/2) * np.sin(dLon/2)
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    distances = np.cumsum(R * c) # total distances from zero
    distances /= distances[-1] # set to 0...1 range
    distances = np.insert(distances, 0, 0.0)

    elevations = [point.elevation for point in points]
    return (elevations, distances)


if __name__ == "__main__":
    N = 180 # 100 points will be generated
    # filename = "dobogoko-sorgyar.json"
    # elevations, distances = elev_from_json(filename)
    elevations, distances = elev_from_gpx("gpx/Dobog_k_.gpx")
    elevations = resample_to_points(elevations, N, distances)
    # create_stl(elevations, "from_gpx_resampled.stl")
    create_svg(elevations, "from_gpx_resampled.svg")