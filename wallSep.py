import sys
import bpy
import csv
import os


# MAKE SURE ENOUGH ARGUMENTS WERE PASSED
if len(sys.argv) > 1:
    index = sys.argv.index("--") + 1
    argv = sys.argv[index:]
    print(argv)

    # get the coefficients from the cmd arguments
    a = float(argv[0])
    b = float(argv[1])
    c = float(argv[2])
    d = float(argv[3])

    # loop through each vertex and remove anything that isn't the wall
    # for vertex in coords:
    #     # get the constant of the current vector in the equation
    #     x, y, z = vertex.to_tuple()
    #     key = a*x + b*y + c*z
    #     # if the vector too far from the wall
    #     if abs(key - d) >= 0.5:
    #         print("DELETE" + str(vertex.to_tuple()))
    #         vertex.delete()
    #         vertex.select = True

    csv_path = os.getcwd() + os.path.sep + "data.csv"
    csv_file = open(csv_path)
    csv_reader = csv.reader(csv_file)
    csv_data = list(csv_reader)
    # process the csv data
    new_data = []
    for line in csv_data:
        # check if the vertex is on the plane
        line = line[0].split(';')
        x = float(line[0])
        y = float(line[1])
        z = float(line[2])
        key = a*x + b*y + c*z
        # if the point is near the plane, add it to the final list
        if(abs(d-key) >= 0.8):
            new_data.append([x, y, z])

    # EXPORT THE DATA TO CSV
    cwd = os.getcwd()
    outputFile = cwd + os.path.sep + "wall_data.csv"
    csvLines = [ ";".join([ str(v) for v in co ]) + "\n" for co in new_data ]
    f = open( outputFile, 'w' )
    f.writelines( csvLines )
    f.close()

else:
    print("NOO")
