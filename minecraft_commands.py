########################################################################################################################
# Function: fill
# Description:
#   Writes a Minecraft 'fill' command to a file
# Arguments:
#   local_file:         Minecraft function file including path
#   start:              Start [X, Y, Z] coordinate of the fill command
#   end:                End [X, Y, Z] coordinate of the fill command
#   tileName:           Type of tile to fill with
#   tileData:           Variant of tile to fill with
#   mode:               Fill mode
#   replaceTileName:    Type of tile to replace when mode="replace"
#   replaceDataValue:   Variant of tile to replace when mode="replace"
########################################################################################################################
def fill(local_file, start, end, tileName, tileData="", mode="", replaceTileName="", replaceDataValue="",
         start_coords=["", "", ""], end_coords=["", "", ""]):
    local_file.write("fill")
    for i in range(3):
        if start_coords[i] == "rel":
            local_file.write(" ~")
        else:
            local_file.write(" ")
        local_file.write(f"{start[i]}")
    for i in range(3):
        if end_coords[i] == "rel":
            local_file.write(" ~")
        else:
            local_file.write(" ")
        local_file.write(f"{end[i]}")
    local_file.write(f" {tileName}")
    if tileData != "":
        local_file.write(f" {tileData}")
    if mode != "":
        local_file.write(f" {mode}")
    if replaceTileName != "":
        local_file.write(f" {replaceTileName}")
    if replaceDataValue != "":
        local_file.write(f" {replaceDataValue}")
    local_file.write("\n")