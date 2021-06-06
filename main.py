import argparse
from minecraft_create import create_from_stl_at_directions


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-sp", "--stl_path", required=True,)
    ap.add_argument("-s", "--stl", required=True,
                    help="Path to input *.stl file")
    ap.add_argument("-p", "--path", required=True,
                    help="Path to functions directory")
    ap.add_argument("-f", "--function", required=True,
                    help="Name of Minecraft Function")
    ap.add_argument("-i", "--voxel_interval", required=False,
                    help="Interval to voxelize STL file")
    ap.add_argument("-d", "--num_directions", required=False,
                    help="Number of directions to create (up to 4)")

    args = vars(ap.parse_args())

    # Handle missing optional arguments
    if args["num_directions"] is None:
        num_directions = 1
    else:
        num_directions = int(args["num_directions"])

    if args["voxel_interval"] is None:
        voxel_interval = 10
    else:
        voxel_interval = int(args["voxel_interval"])

    create_from_stl_at_directions(args["stl_path"], args["stl"], args["path"], args["function"], num_directions,
                                  voxel_interval, center=[True, False, False])

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
