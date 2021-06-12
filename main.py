import argparse
import os.path

from minecraft_create import create_from_stl_at_directions
from imutils import paths

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-sp", "--stl_path", required=True,)
    ap.add_argument("-s", "--stl", required=False,
                    help="Path to input *.stl file")
    ap.add_argument("-fp", "--function_path", required=True,
                    help="Path to functions directory")
    ap.add_argument("-f", "--function", required=False,
                    help="Name of Minecraft Function")
    ap.add_argument("-i", "--voxel_interval", required=False,
                    help="Interval to voxelize STL file")
    ap.add_argument("-d", "--num_directions", required=False,
                    help="Number of directions to create (up to 4)")
    ap.add_argument("-bt", "--block_type", required=False,
                    help="Primary block type")
    ap.add_argument("-bd", "--block_data", required=False,
                    help="Primary block data (variant number)")

    args = vars(ap.parse_args())

    stl_paths = list(paths.list_files(args["stl_path"], "stl"))

    # Handle missing optional arguments
    if args["num_directions"] is None:
        num_directions = 1
    else:
        num_directions = int(args["num_directions"])

    if args["voxel_interval"] is None:
        voxel_interval = 1
    else:
        voxel_interval = int(args["voxel_interval"])

    if args["stl"] is None:
        for stl_file in stl_paths:
            if args["block_type"] is None:
                block_type = (os.path.normpath(stl_file).split(os.path.sep))[-3]
                if args["block_data"] is None:
                    block_data = int((os.path.normpath(stl_file).split(os.path.sep))[-2])
                else:
                    block_data = args["block_data"]
                print(block_type)
            else:
                block_type = args["block_type"]
                if args["block_data"] is None:
                    block_data = 0
                else:
                    block_data = args["block_data"]

            function_name = os.path.splitext((os.path.normpath(stl_file).split(os.path.sep))[-1])[0]
            stl = os.path.split(stl_file)
            stl_filename = (os.path.normpath(stl_file).split(os.path.sep))[-1]
            create_from_stl_at_directions(stl[0], stl[1], args["function_path"], function_name,
                                          num_directions, voxel_interval, center=[True, False, False],
                                          block_type=block_type, block_data=block_data)
    else:
        if args["block_type"] is None:
            block_type = (os.path.normpath(args["stl_path"]).split(os.path.sep))[-1]
            block_data = (os.path.normpath(args["stl_path"]).split(os.path.sep))[-1]
            print(block_type)
        else:
            block_type = args["block_type"]

        if args["block_data"] is None:
            block_data = 0
        else:
            block_data = int(args["block_data"])

        if args["function"] is None:
            function_name = os.path.splitext(args["stl"])[0]
        else:
            function_name = args["function"]

        create_from_stl_at_directions(args["stl_path"], args["stl"], args["path"], function_name, num_directions,
                                      voxel_interval, center=[True, False, False], block_type=block_type,
                                      block_data=block_data)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
