# Assets

Static assets for the House Price Predictor Streamlit application.

## Files

- `hero-house.jpg` — main property/hero image.
- `about-house.jpg` — About page property image.
- `insights-house.jpg` — Insights page property image.
- `logo.svg` — navbar/project logo.
- `favicon.svg` — browser tab icon.
- `home.svg` — Home navigation icon.
- `predictor.svg` — Predictor navigation icon.
- `insights.svg` — Insights navigation icon.
- `about.svg` — About navigation icon.

## Suggested usage

```python
from pathlib import Path

ASSETS = Path(__file__).parent / "assets"

hero_image = ASSETS / "hero-house.jpg"
```

For Streamlit:

```python
st.image(str(hero_image), use_container_width=True)
```

The local images can replace the external Unsplash URLs currently used in `app.py`, so the project does not depend on those remote image URLs at runtime.
