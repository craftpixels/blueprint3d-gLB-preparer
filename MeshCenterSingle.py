import bpy
from mathutils import Vector, Matrix


C = bpy.context
mesh = C.active_object

def centerMeshByGeometricBounds(mesh):
    xvalues = []
    yvalues = []
    zvalues = []
    
    for bvalue in mesh.bound_box:
        xvalues.append(bvalue[0])
        yvalues.append(bvalue[1])
        zvalues.append(bvalue[2])
    
    minX = min(xvalues)
    maxX = max(xvalues)
    
    minY = min(yvalues)
    maxY = max(yvalues)
    
    minZ = min(zvalues)
    maxZ = max(zvalues)
    
    width, height, depth = maxX - minX, maxZ - minZ, maxY - minY
    cx, cy, cz = (width * 0.5) + minX, (depth * 0.5) + minY, (height * 0.5) + minZ
    
    
    m = Matrix.Translation((-cx, -cy, -cz))
    for v in mesh.data.vertices:
        v.co = m@v.co
    
    
    
centerMeshByGeometricBounds(mesh)
