import simplejson as json
import stl

# Budapest: 47.496215, 19.033440
# Pécs: 46.079573, 18.234001


def create_model(response):
    points = response["results"]
    elevations = [pt["elevation"] for pt in points]
    # subsample
    elevations = elevations[0::2]
    # normalize elevations
    e_max = max(elevations)
    e_min = min(elevations)
    elevations = [10 + 30 * (e - e_min) / (e_max - e_min) for e in elevations]

    lengths = [2.0 for pt in points]

    model = stl.Solid("Budapest-Pecs.stl")
    hills = stl.Feature(stl.Vector(0, 0, 0), stl.Coords.X, 30.0, lengths, elevations)
    model.add(hills)
    model.write()


def get_saved_file():
    # testing only
    with open("sample.json", "r") as reader:
        return reader.read()


if __name__ == "__main__":
    response = get_saved_file()
    obj = json.loads(response)

    create_model(obj)