import gpxpy
import json


def convert_normalize(filename, points_count):
    gpx_file = open(filename, 'r')

    gpx = gpxpy.parse(gpx_file)

    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append({
                    'lat': point.latitude,
                    'lng': point.longitude,
                })

    waypoints = []
    for waypoint in gpx.waypoints:
        waypoints.append({
            'lat': waypoint.latitude,
            'lng': waypoint.longitude,
        })

    clean_points = []
    clean_points.append(waypoints[0])
    skip_step = int(len(points) / points_count)
    current_step = 0
    for p in points:
        current_step += 1
        if current_step >= skip_step:
            clean_points.append(p)
            current_step = 0
    clean_points.append(waypoints[-1])

    print('%s' % len(points))
    print('%s' % len(clean_points))

    content = json.dumps({
        'start_point': waypoints[0],
        'end_point': waypoints[-1],
        'checkpoints': clean_points
    })
    result_file = open(filename.split(".")[0] + ".json", "w")
    result_file.write(content)


convert_normalize('amsterdam_delfzijl.gpx', 50)
convert_normalize('oldenburg_alkmaar.gpx', 75)
