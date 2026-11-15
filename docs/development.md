# Development and Testing

## Standalone Python retrieval demonstration

Python 3.10+ is sufficient. No third-party packages are required for the example:

```bash
python examples/gower_demo.py
python -m unittest discover -s tests -v
```

The synthetic demonstration shows weighted mixed-type similarity and family gating. It does **not** use actual NASA experimental records or compute combustion outcomes.

For a live interactive preview of the scientific architecture, open `docs/index.html` in a browser. GitHub Pages can serve this file from the `docs/` folder.

## Full application distinction

The current live EMBER application is deployed separately at https://ember-mvp-one-man-orbit.vercel.app/. The Python example and static explainer are not the same implementation as the current production server.

## Scientific change checklist

1. Identify the NASA experimental record, scientific reference, or original algorithm.
2. Preserve measured inputs and their units.
3. Define material/geometry/domain restrictions.
4. Distinguish observation, mathematical calculation, and statistical prediction.
5. Add regression tests for invalid inputs, missing features, zero denominators and out-of-domain cases.
6. Explain extrapolation limitations and abstention conditions.

Never claim a test suite alone proves physical validation or spacecraft fire safety.
