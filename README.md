# TopoPilot

TopoPilot is a local-first Blender mesh diagnosis starter project for checking AI-generated assets before they move further through an art or game pipeline.

It provides a small, deterministic Python core, a JSON report, and a Blender add-on skeleton. AI is optional: the fixture workflow works offline and does not require an API key or a Blender installation.

[![Download](https://img.shields.io/badge/Download-Latest-2ea44f?style=for-the-badge&logo=github)](DOWNLOAD_URL_HERE)

## What is included

- Mesh fixture diagnosis for boundary edges, non-manifold edges, degenerate faces, and basic density metrics.
- A CLI that runs without `bpy`.
- A Blender N-panel and operator that safely diagnose the active mesh without changing the scene.
- JSON reports suitable for local smoke tests and future pipeline steps.
- Tests for the core fixture and CLI behavior.

The current package is intentionally small. It does not promise ideal quad topology, automatic rigging, or production-ready repair, retopology, UV, LOD, or material results. Complex assets still need artist review and engine-specific validation.

## Quick start

```text
python -m venv .venv
python -m pip install -e ".[test]"
python -m topopilot --help
python -m topopilot diagnose --sample
python -m unittest discover -s tests -v
```

Write a report to a file:

```text
python -m topopilot diagnose --sample --output report.json
```

The CLI is local-first and offline by default. Any future provider adapter should be explicit, replaceable, and unable to mutate a Blender scene directly.

## Blender add-on

Install the `topopilot/blender_addon` package as an add-on in Blender, or zip that directory for Blender's Extensions/Add-ons installer. Open the 3D View sidebar with `N`, choose the `TopoPilot` tab, and run **Diagnose Active Mesh**. The operator reports counts and warnings without editing the active object.

The add-on skeleton is kept separate from the CLI so importing `topopilot` and running its tests does not require Blender.

## Reports and limitations

Reports include the fixture or object name, topology counts, density metrics, warning codes, and a schema version. A diagnosis is evidence for review, not a certification that a mesh is ready for every engine. Boundary detection cannot infer whether an open edge is intentional, and geometric checks do not replace visual inspection.

## License

MIT. See [LICENSE](LICENSE).
