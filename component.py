"""mesh a polyline.
    Inputs:
        polylines: polylines to polygonal profile pipe
        radius: radius of pipe polygon profile
        numSides: sides of pipe polygon profile
    Output:
        mesh: polygonal pipe as mesh
    
    "Tony Yu - NExT Lab / Robotics Lab"
    "2025.03.31"
"""
                
import Rhino.Geometry as rh
import ghpythonlib.parallel
import System.Collections.Generic as scg
                
def makePlanes(i):
    """
    given a polyline, generate planes at each kink that is oriented perpendicular to each kink
    """
    _thisPt = rh.Vector3d(pl[i])
    #vector business
    if i == 0:
        _fDir = rh.Vector3d(pl[i+1]) - _thisPt
        pass
    elif i == pl.Count-1:
        _fDir = _thisPt - rh.Vector3d(pl[i-1])
        pass
    else:
        _prevDir = _thisPt - rh.Vector3d(pl[i-1])
        _nextDir = rh.Vector3d(pl[i+1]) - _thisPt
        _fDir = _prevDir + _nextDir
                
    #make plane
    _plane = rh.Plane(pl[i],_fDir,up)
    _planes_[i] = (_plane)
                
def makeMeshBuffer(i):
    """
    given a plane belonging to a polyline, generate vertices and mesh faces for that cross section
    """
            
    #construct vertex list
    _tf = rh.Transform.PlaneToPlane(rh.Plane.WorldXY,_planes_[i])
    _temp = makePolygon(numSides)
    _temp.Transform(_tf)
                    
    for ns in range(_temp.Count-1):
        _i = (i * numSides) + ns
        _vbuffer_[_i] = _temp[ns]
                        
        if i < len(_planes_)-1:
            #if last item in the polygon, gotta close
            if ns == _temp.Count-2:
                _fbuffer_[_i] = rh.MeshFace(_i, _i+numSides, _i+1, _i-numSides+1)
            else:
                _fbuffer_[_i] = rh.MeshFace(_i, _i+numSides, _i+numSides+1, _i+1)
                
def makePolygon(numSides):
    _cirPlane = rh.Plane(rh.Point3d(0,0,0),rh.Vector3d(1,0,0))
    _polygon = rh.Polyline.CreateInscribedPolygon(rh.Circle(_cirPlane,radius/2),numSides)
                
    return _polygon
                    
        
pl = polylines
                
#sanitize inputs
if numSides < 3 or numSides is None:
    numSides = 3
numSides = int(numSides)
                
if radius is None or radius < 0.0:
    radius = 1.0
radius = float(radius)
        
        
"""
 first make planes alongside polyline in one shot parallel
 second, use planes to generate mesh components
 it is split into two steps so it's less messy, it could technically be done in one step
 calculating all the necessary information per polyline kink, but this just feels cleaner and
 easier to understand. 
"""
        
if pl is not None:
    #_globals_
    # generate planes along a polyline and writes them to _planes_
    up = rh.Vector3d(0,0,1)
    _planes_ = [None] * pl.Count
    indices = range(pl.Count)
    ghpythonlib.parallel.run(makePlanes, indices)
                    
    #_globals_
    # make some global buffers for vertices and mesh faces
    _vbuffer_ = [None] * len(_planes_)*numSides
    _fbuffer_ = [None] * (len(_planes_)-1)*numSides
    indices = range(len(_planes_))
    ghpythonlib.parallel.run(makeMeshBuffer,indices)
                    
    print(len(_fbuffer_))
                    
    #write to mesh using the vertex and mesh faces buffers
    _geo_ = rh.Mesh()
    #this is the way to call a specific overloaded method
    _geo_.Vertices.AddVertices.Overloads[scg.IEnumerable[rh.Point3d]](_vbuffer_)
    _geo_.Faces.AddFaces.Overloads[scg.IEnumerable[rh.MeshFace]](_fbuffer_)
    _geo_.RebuildNormals()
                    
                    
    mesh = _geo_
