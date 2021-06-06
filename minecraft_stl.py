from minecraft_commands import fill
import trimesh
import math

# Maximum lines that can be put into a Minecraft Function file
MAX_FILE_LINES = 9999


########################################################################################################################
# Function: convert_stl_to_minecraft_function
# Description:
#   Converts the provided STL file into a *.mcfunction file or files used to generate the object
# Arguments:
#   stl_path:       Path to the STL file to voxelize and use as source information
#   stl_file:       Filename of the *.STL file to voxelize and use as source information
#   filename:       Root filename of the *.mcfunction file to output Minecraft commands into
#   function_name:  Function name to use to determine naming of secondary files needed when creating large models
#   rotate:         Angle to rotate the model in radians
#   interval:       Voxelization interval, must be an integer from 1 to some yet to be discovered maximum.
#                   The larger this value is, the smaller the model will be.
#   center:         Determines whether the output model is centered with respect to where the model will be generated
#   origin:         The origin point, if absolute. Otherwise, the origin point will be the player running the command
########################################################################################################################
def convert_stl_to_minecraft_function(stl_path, stl_file, filename, function_name, rotate=0, interval=1,
                                      center=[False, False, False], origin=None):
    print('Getting the mesh from the STL file...', end='')
    mesh = trimesh.load_mesh(fr"{stl_path}\{stl_file}", Process=False)
    print("complete")

    print(f"Mesh is wateright? {mesh.is_watertight}")
    # print(mesh.euler_number)

    print("Voxelizing STL file...", end='')
    voxels = mesh.voxelized(interval)
    print("complete")

    x_rotated = []
    y_rotated = []
    z_rotated = []

    print(f"Rotating voxels by desired {rotate} radians...", end='')
    # Preprocess voxels
    for voxel in voxels.points:
        # Rotate them the desired angle
        x_rotated.append(round(voxel[0] * math.cos(rotate) - voxel[1] * math.sin(rotate)))
        y_rotated.append(voxel[2])
        z_rotated.append(round(voxel[0] * math.sin(rotate) + voxel[1] * math.cos(rotate)))
    print("complete")

    print("Determining bounding box of model...")
    mins = [min(x_rotated), min(y_rotated), min(z_rotated)]
    print(f"\tMin [X, Y, Z]: {mins}")
    maxs = [max(x_rotated), max(y_rotated), max(z_rotated)]
    print(f"\tMax [X, Y, Z]: {maxs}\n")

    print(f"Calculating shift based on desired center settings: {center}")
    if center[0]:
        x_shift = mins[0] + ((maxs[0] - mins[0]) / 2)
    else:
        x_shift = mins[0]
    if center[1]:
        y_shift = mins[1] + ((maxs[1] - mins[1]) / 2)
    else:
        y_shift = mins[1]
    if center[2]:
        z_shift = mins[2] + ((maxs[2] - mins[2]) / 2)
    else:
        z_shift = mins[2]
    print(f"\tShift values [X, Y, Z]: [{x_shift}, {y_shift}, {z_shift}]\n")

    # Get the number of blocks
    lines = len(voxels.points)
    print(f"Lines to be written: {lines}")

    # Determine the number of files needed
    files = int(lines / MAX_FILE_LINES) + 1
    print(f"Files to be written: {files}")

    # Create the main file to only handle calling other functions
    main_filename = f"{filename}.mcfunction"
    # default the save_filename to match
    save_filename = main_filename

    # If more than one file is needed...
    if files > 1:
        print(f"Opening main file {main_filename} for multi-file function...", end='')
        main_file = open(main_filename, "w")
        print("complete")

    # Loop over the number of files to be written
    for file_num in range(files):
        # If looping over multiple files...
        if files > 1:
            # ...write the function call into the main function file
            main_file.write(f"function {function_name}{file_num}\n")
            # name the secondary file to be created
            save_filename = f"{filename}{file_num}.mcfunction"

        # Open the function file, whether primary or otherwise
        print(f"Opening function file {save_filename} for writing...", end='')
        file = open(save_filename, "w")
        print("complete")

        # Calculate the start/end line to write to this file
        file_start_line = file_num * MAX_FILE_LINES
        file_end_line = file_start_line + MAX_FILE_LINES - 1

        # If the file line is beyond the maximum, clamp it
        if file_end_line > lines:
            file_end_line = lines

        print(f"Looping over range: {file_start_line} - {file_end_line}")
        # Loop through each voxel
        for voxel_index in range(file_start_line, file_end_line):
            print(f"Adding lines {voxel_index} to file {file_num}...", end='\r')
            # Shift to desired location
            x_shifted = x_rotated[voxel_index] - x_shift
            y_shifted = y_rotated[voxel_index] - y_shift
            z_shifted = z_rotated[voxel_index] - z_shift

            # Scale to desired size
            x = x_scaled = x_shifted / interval
            y = y_scaled = y_shifted / interval
            z = z_scaled = z_shifted / interval

            # If the user didn't provide an origin value...
            if origin is None:
                # ...write to the file relative coordinates...
                fill(file,
                     [x, y, z],
                     [x, y, z],
                     "quartz_block", 0,
                     start_coords=["rel", "rel", "rel"], end_coords=["rel", "rel", "rel"])
            else:
                # ...otherwise shift the coodinates to their provided origin
                fill(file,
                     [origin[0] + x, origin[1] + y, origin[2] + z],
                     [origin[0] + x, origin[1] + y, origin[2] + z],
                     "quartz_block", 0,
                     start_coords=["abs", "abs", "abs"], end_coords=["abs", "abs", "abs"])
        # Close the file, whether primary or not
        print(f"\nClosing function file {save_filename}...", end='')
        file.close()
        print("complete")

    # Close the main file if this was a multi-file function
    if files > 1:
        print(f"Closing main file {main_filename} for multi-file function...", end='')
        main_file.close()
        print("complete")
    return
