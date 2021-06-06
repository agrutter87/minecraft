from minecraft_stl import convert_stl_to_minecraft_function
from minecraft_commands import fill
from helpers import frange

import math


########################################################################################################################
# Function: create_from_stl_at_directions
# Description:
#   Converts the provided STL file into a number of *.mcfunction files or files used to generate the object with the
#   specified number of directions
# Arguments:
#   stl_path:       Path to the STL file to voxelize and use as source information
#   stl_file:       Filename of the *.STL file to voxelize and use as source information
#   function_path:  Path to of the Minecraft function directory file to output Minecraft command files into
#   function:       Root function name to use to determine naming of files at multiple directions
#   num_directions: Number of directions to create models for up to 4. (north, south, east, west)
#   voxel_interval: Voxelization interval, must be an integer from 1 to some yet to be discovered maximum.
#                   The larger this value is, the smaller the model will be.
#   center:         Determines whether the output model is centered with respect to where the model will be generated
#   origin:         The origin point, if absolute. Otherwise, the origin point will be the player running the command
########################################################################################################################
def create_from_stl_at_directions(stl_path, stl_file, function_path, function, num_directions, voxel_interval, center,
                                  origin=None):
    DIRECTIONS = ["north", "south", "east", "west"]
    # Loop over some number of *.mcfunction files to output
    for direction in range(num_directions):
        function_name = f'{function}_{DIRECTIONS[direction]}'

        # For each file, create a filename with one of the four directions
        filename = function_path + fr'\{function_name}'

        # Determine the rotation for the model output to this file
        rotation = (math.pi * 2) * (direction / 1)

        # Convert the *.stl file to a *.mcfunction file
        convert_stl_to_minecraft_function(stl_path, stl_file, filename, function_name,
                                          rotation, voxel_interval, center, origin)


########################################################################################################################
# Function: create_road
# Description:
#   Creates a hard-coded minecraft function file which generates a road
# Arguments:
#   local_file:     Minecraft function file including path
########################################################################################################################
def create_road(local_file):
    for road_block in range(100):
        # Black wool road
        fill(local_file, [-7, -1, 64 * road_block], [7, -1, (64 * (road_block + 1)) - 1], "wool", 15, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])
        # White wool side solid lines
        fill(local_file, [-6, -1, 64 * road_block], [-6, -1, (64 * (road_block + 1)) - 1], "wool", 0, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])
        fill(local_file, [6,  -1, 64 * road_block], [6,  -1, (64 * (road_block + 1)) - 1], "wool", 0, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])
        # Air above road (for cutting through mountains
        fill(local_file, [-7, 0, 64 * road_block], [7, 2, (64 * (road_block + 1)) - 1], "air", 0, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])
        # Dashed lines
        for line_num in range(int(64 / 4)):
            fill(local_file, [0, -1, (line_num * 4) + (road_block * 64)], [0, -1, (line_num * 4) + 1 + (road_block * 64)], "wool", 0, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])


########################################################################################################################
# Function: create_tower
# Description:
#   Creates a minecraft function file which generates a tower with the specified parameters
# Arguments:
#   local_file:     Minecraft function file including path
#   radius:         Radius of tower
#   height:         Height of tower
#   resolution:     Number of pillars to create the walls out of (For doing unfilled wall towers
#   block_type:     Type of block to make the tower out of
########################################################################################################################
def create_tower(local_file, radius, height, resolution, block_type):
    fill(local_file, [-radius, 0, -radius], [radius, height, radius], "air", 0, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])
    for rad in frange(0, 2 * math.pi, (math.pi / resolution)):
        x = int(radius * math.cos(rad))
        z = int(radius * math.sin(rad))
        fill(local_file, [x, 0, z], [x, height, z], block_type, 0, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])


########################################################################################################################
# Function: delete_above
# Description:
#   Deletes everything around player in a 64 x 64 area, and all the way to the top of the buildable area
# Arguments:
#   local_file:     Minecraft function file including path
########################################################################################################################
def delete_above(local_file):
    for y in range(256):
        fill(local_file, [-64, y, -64], [64, y, 64], "air", 0, start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])


