"""Module with functions for 3D geometrical operations"""

import numpy as np
import mapbox_earcut as earcut
import pyvista as pv

def surface_normal(poly):
    n = [0.0, 0.0, 0.0]

    for i, v_curr in enumerate(poly):
        v_next = poly[(i+1) % len(poly)]
        n[0] += (v_curr[1] - v_next[1]) * (v_curr[2] + v_next[2])
        n[1] += (v_curr[2] - v_next[2]) * (v_curr[0] + v_next[0])
        n[2] += (v_curr[0] - v_next[0]) * (v_curr[1] + v_next[1])

    normalised = [i/np.linalg.norm(n) for i in n]

    return normalised

def project_2d(points, normal):
    origin = points[0]
    
    if normal[2] > 0.001 or normal[2] < -0.001:
        x_axis = [1, 0, -normal[0]/normal[2]];
    elif normal[1] > 0.001 or normal[1] < -0.001:
        x_axis = [1, -normal[0]/normal[1], 0];
    else:
        x_axis = [-normal[1] / normal[0], 1, 0];
    
    y_axis = np.cross(normal, x_axis)
     
    return [[np.dot(p - origin, x_axis), np.dot(p - origin, y_axis)] for p in points]

def triangulate(mesh):
    """Triangulates a mesh in the proper way"""
    
    final_mesh = pv.PolyData()
    n_cells = mesh.n_cells
    for i in np.arange(n_cells):
        if not mesh.cell_type(i) in [5, 6, 7, 9, 10]:
            continue

        pts = mesh.cell_points(i)
        p = project_2d(pts, mesh.face_normals[i])
        result = earcut.triangulate_float32(p, [len(p)])

        t_count = len(result.reshape(-1,3))
        triangles = np.hstack([[3] + list(t) for t in result.reshape(-1,3)])
        
        new_mesh = pv.PolyData(pts, triangles, n_faces=t_count)
        for k in mesh.cell_arrays:
            new_mesh[k] = [mesh.cell_arrays[k][i] for _ in np.arange(t_count)]
        
        final_mesh = final_mesh + new_mesh
    
    return final_mesh

def triangulate_polygon(face, vertices):
    """Returns the points and triangles for a given CityJSON polygon"""

    points = vertices[np.hstack(face)]
    normal = surface_normal(points)
    holes = [0]
    for ring in face:
        holes.append(len(ring) + holes[-1])
    holes = holes[1:]

    points_2d = project_2d(points, normal)

    result = earcut.triangulate_float32(points_2d, holes)

    t_count = len(result.reshape(-1,3))
    if t_count == 0:
        return points,  []
    triangles = np.hstack([[3] + list(t) for t in result.reshape(-1,3)])

    return points, triangles