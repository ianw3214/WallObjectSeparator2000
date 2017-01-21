import bpy
from bpy import context
import random
import subprocess
import inspect, os
from shutil import copyfile

def getNormal(p1, p2, p3):
    """return the normal vector to the equation of a plane given by the 3 point vertices

    @type p1: (float, float, float)
    @type p2: (float, float, float)
    @type p3: (float, float, float)
    @rtype: (float, float, float)
    """
    # Get the direction vectors by subtracting the point vectors
    v1 = p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]
    v2 = p3[0]-p1[0], p3[1]-p1[1], p3[2]-p1[2]
    # Return the cross product of the two vectors which is orthigonal to the plane
    return v1[1]*v2[2] - v1[2]*v2[1], v1[0]*v2[2] - v1[2]*v2[0], v1[0]*v2[1] - v1[1]*v2[0]


def getConstant(normal, vector):
    """Return the constant of the equation to a plane given by a normal vector and a point

    @type normal: (float, float, float)
    @type vector: (float, float, float)
    @rtype: float
    """
    # The equation is ax + by + cz = d
    # where a, b, c are normal vector coefficients and x, y, z are points on the plane
    n1, n2, n3 = normal
    v1, v2, v3 = vector
    # Solve for the equation by plugging in all the values
    return n1*v1 + n2*v2 + n3*v3


print("+=====+")

# GET THE VERTICES CONTAINED IN THE BLENDER FILE
coords = []
for ob in bpy.data.objects:
    # MAKE SURE WE ONLY PROCESS MESHES OR SOMETHING WITH VERTICES
    if not ob.type in ['MESH','CURVE']:
        pass
    else:
        print (ob.name)
        coords += [(ob.matrix_world * v.co) for v in ob.data.vertices]

# KEEP LOOPING UNTIL AT LEAST HALF OF THE COMBINATIONS HAVE BEEN CHECKED
# keep track of which combinations we have checked to make sure we don't repeat checking any points
checked = {}
bar = len(coords)/2;
# result will be in the form of normal vectors and constant if found
result = None

for i in range(100):           # TODO: Change range(1000) to be minimum guaranteed of 3 spots along wall
    # Get 3 random vertices to check every time
    indices = range(len(coords))
    keys = random.sample(indices, 3)
    # store the vertex position data in seperate variables
    v1, v2, v3 = coords[keys[0]].to_tuple(), coords[keys[1]].to_tuple(), coords[keys[2]].to_tuple()
    # find the normal vector of the plane with the 3 points
    n1, n2, n3 = getNormal(v1, v2, v3)
    # get the constant of the plane with the normal vector and a point
    d = getConstant((n1, n2, n3), v1)
    # test all other vertices until the bar has been reached
    reached = 0                 # variable that keeps track of how many vertices are on the current plane
    for vertex in coords:
        # get the constant using the normal vector and current vertex
        key = getConstant((n1, n2, n3), vertex.to_tuple());
        # print out the results
        print("{} : {}".format(key, d));
        # if the difference is less than 1, then it is most likely on the same plane
        if abs(key - d) <= 1.0:
            reached += 1        # increment the reached count
            # stop looping if we have found enough to prove it is a wall
            if reached > bar:
                break
    # break out of the loop if we have found the plane
    if reached > bar:
        result = n1, n2, n3, d
        break

# check if we have found a suitable plane
if result is None:
    print("No suitable planes were found.")
else:
    # make 2 copies of the file and call scripts on the copies

    # SAMPLE COMMAND
    # subprocess.run(["COMMAND", "ARG1", "ARG2", "ARG3", "ARG4"])
    abs_path = os.getcwd() + os.path.sep + bpy.path.basename(bpy.context.blend_data.filepath)
    print(abs_path)

print("+=====+")
