import simplejson as json
import stl

from typing import List

# Budapest: 47.496215, 19.033440
# Pécs: 46.079573, 18.234001


def create_model(elevations, filename: str, n_points=100):
    # resample elevations
    from numpy import linspace, interp
    n_orig = len(elevations)
    elevations = interp(
        linspace(0, n_orig-1, n_points), # query points
        linspace(0, n_orig-1, n_orig),  # original X points
        elevations)

    # normalize elevations
    e_max = max(elevations)
    e_min = min(elevations)
    elevations = [10 + 30 * (e - e_min) / (e_max - e_min)
        for e in elevations]

    lengths = [2.0 for pt in elevations]

    model = stl.Solid(filename.replace("json", "stl").replace("gpx", "stl"))
    hills = stl.Feature(stl.Vector(0, 0, 0), stl.Coords.X, 30.0, lengths, elevations)
    model.add(hills)
    model.write()


def elev_from_json(filename: str) -> List[float]:
    # get elevations from json
    with open(filename, "r") as reader:
        response = reader.read()
    points = json.loads(response)["results"]
    elevations = [pt["elevation"] for pt in points]
    return elevations


def elev_from_gpx(filename: str) -> List[float]:
    import gpxpy # https://pypi.org/project/gpxpy/
    import gpxpy.gpx
    gpx = gpxpy.parse(open(filename, "r"))
    points = gpx.tracks[0].segments[0].points
    return [point.elevation for point in points]
    # point.latitude, point.longitude


if __name__ == "__main__":
    # filename = "dobogoko-sorgyar.json"
    # elevations = elev_from_json(filename)
    elevations = elev_from_gpx("gpx/Dobog_k_.gpx")
    print(len(elevations))
    create_model(elevations, "from_gpx.stl")