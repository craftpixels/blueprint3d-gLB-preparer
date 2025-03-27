# Created by Craftpixels Team
# Mesh Center View Adjustment Script
import os, sys
import bpy
import json
from mathutils import Vector, Matrix

argv = sys.argv
argv = argv[argv.index("---") + 1:]


C = bpy.context
mesh = C.active_object

data = {
            "itemName": "Roof Lamp 3",
            "position": [0,0,0],
            "rotation": [0,0,0],
            "innerRotation": [0,0,0],
            "scale": [1,1,1],
            "size": [200, 25, 14],
            "modelURL": "models/glb/RoofItem/roof_lamp3.glb"
}

def importGLBAndPreProcess(filepath):
    bpy.ops.object.select_all(action="SELECT");
    bpy.ops.object.delete()
    bpy.ops.import_scene.gltf(filepath=filepath)
    bpy.ops.object.select_all(action="DESELECT")

def getMeshCollectionAndCenter(context, actualWidth):
    meshParts = []
    for o in context.scene.objects:
        if(o.type == 'MESH'):
            o.location = (0, 0, 0)
            o.scale = (1, 1, 1)
            meshParts.append(o)    
            
    return meshParts

def getMeshBounds(mesh):
    minBound = Vector((0,0,0))
    maxBound = Vector((0,0,0))
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
    
    minBounds = Vector((minX, minY, minZ))
    maxBounds = Vector((maxX, maxY, maxZ))
    
    return minBounds, maxBounds

def getCumulativeMeshCenter(meshes):
    minF, maxF = -sys.float_info.max, sys.float_info.max
    actualMin, actualMax = Vector((maxF, maxF, maxF)), Vector((minF, minF, minF))
    for mesh in meshes:
        minBounds, maxBounds = getMeshBounds(mesh)
        actualMin.x = min(minBounds.x, actualMin.x)
        actualMin.y = min(minBounds.y, actualMin.y)
        actualMin.z = min(minBounds.z, actualMin.z)
        
        actualMax.x = max(maxBounds.x, actualMax.x)
        actualMax.y = max(maxBounds.y, actualMax.y)
        actualMax.z = max(maxBounds.z, actualMax.z)
    
    width, height, depth = actualMax.x - actualMin.x, actualMax.z - actualMin.z, actualMax.y - actualMin.y
    cx, cy, cz = (width * 0.5) + actualMin.x, (depth * 0.5) + actualMin.y, (height * 0.5) + actualMin.z
    return Vector((cx, cy, cz)), Vector((width, depth, height))


def constructTransformationMatrix(boundsCenter, scaleRatio=1.0):
    cx, cy, cz = boundsCenter

    scaleX = Matrix.Scale(scaleRatio, 4, Vector((1.0, 0.0, 0.0)))
    scaleY = Matrix.Scale(scaleRatio, 4, Vector((0.0, 1.0, 0.0)))
    scaleZ = Matrix.Scale(scaleRatio, 4, Vector((0.0, 0.0, 1.0)))
    scaleMatrix = scaleX @ scaleY @ scaleZ
    translationMatrix = Matrix.Translation((-cx, -cy, -cz))
    transformation = scaleMatrix @ translationMatrix
    return transformation  

def centerMeshByTransformation(mesh, transformMatrix):
    for v in mesh.data.vertices:
        v.co = transformMatrix@v.co
    mesh.location = (0,0,0)


def exportMeshCollectionAsGLB(context, meshCollection, exportPath):
    bpy.ops.object.select_all(action="DESELECT");
    for m in meshCollection:
        m.select_set(True)

    bpy.ops.export_scene.gltf(filepath=exportPath, export_format='GLB', use_selection=True, export_draco_mesh_compression_enable=False, export_draco_mesh_compression_level=6, export_draco_position_quantization=14, export_draco_normal_quantization=10, export_draco_texcoord_quantization=12, export_draco_color_quantization=10, export_draco_generic_quantization=12)
    bpy.ops.object.select_all(action="DESELECT");
    

if __name__ == '__main__':
    glbFilePath = bpy.path.abspath(argv[0])
    
    glbFileDirectory = os.path.dirname(glbFilePath)
    glbFileName = argv[2]   
    glbExportPath = os.path.join(glbFileDirectory, glbFileName)
    glbActualWidth = float(argv[1])
    
    
    importGLBAndPreProcess(glbFilePath)
    meshCollection = getMeshCollectionAndCenter(C, glbActualWidth)
    multiPartsCenter, multiPartsSize = getCumulativeMeshCenter(meshCollection)
    scaleRatio = glbActualWidth / multiPartsSize.x
    
    unifiedTransformationMatrix = constructTransformationMatrix(multiPartsCenter, scaleRatio)
    for m in meshCollection:
        centerMeshByTransformation(m, unifiedTransformationMatrix)
    
    exportMeshCollectionAsGLB(C, meshCollection, glbExportPath)
    sys.exit(0)

