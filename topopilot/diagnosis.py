"""Deterministic mesh checks that do not depend on Blender."""

from collections import Counter
from math import sqrt


def _distance(a, b):
    return sqrt(sum((left - right) ** 2 for left, right in zip(a, b)))


def diagnose_mesh(mesh, name="mesh"):
    vertices = mesh.get("vertices", [])
    faces = mesh.get("faces", [])
    edges = Counter()
    degenerate_faces = []
    face_areas = []

    for face_index, face in enumerate(faces):
        if len(face) < 3 or len(set(face)) < 3:
            degenerate_faces.append(face_index)
            continue
        points = [vertices[index] for index in face]
        area = 0.0
        for index in range(1, len(points) - 1):
            ax, ay, az = (points[index][i] - points[0][i] for i in range(3))
            bx, by, bz = (points[index + 1][i] - points[0][i] for i in range(3))
            area += 0.5 * sqrt((ay * bz - az * by) ** 2 + (az * bx - ax * bz) ** 2 + (ax * by - ay * bx) ** 2)
        face_areas.append(area)
        for index, start in enumerate(face):
            end = face[(index + 1) % len(face)]
            edges[tuple(sorted((start, end)))] += 1

    boundary_edges = sorted(edge for edge, count in edges.items() if count == 1)
    non_manifold_edges = sorted(edge for edge, count in edges.items() if count > 2)
    used_vertices = {index for face in faces for index in face if 0 <= index < len(vertices)}
    warnings = []
    if boundary_edges:
        warnings.append("boundary_edges")
    if non_manifold_edges:
        warnings.append("non_manifold_edges")
    if degenerate_faces:
        warnings.append("degenerate_faces")
    if any(index < 0 or index >= len(vertices) for face in faces for index in face):
        warnings.append("invalid_vertex_index")

    diagonal = 0.0
    if vertices:
        for first in vertices:
            for second in vertices:
                diagonal = max(diagonal, _distance(first, second))

    return {
        "schema_version": "1",
        "name": name,
        "metrics": {
            "vertex_count": len(vertices),
            "face_count": len(faces),
            "edge_count": len(edges),
            "boundary_edge_count": len(boundary_edges),
            "non_manifold_edge_count": len(non_manifold_edges),
            "degenerate_face_count": len(degenerate_faces),
            "unused_vertex_count": len(set(range(len(vertices))) - used_vertices),
            "surface_area": round(sum(face_areas), 6),
            "bounding_diagonal": round(diagonal, 6),
        },
        "warnings": warnings,
        "details": {
            "boundary_edges": [list(edge) for edge in boundary_edges],
            "non_manifold_edges": [list(edge) for edge in non_manifold_edges],
            "degenerate_faces": degenerate_faces,
        },
        "operations": [],
    }
