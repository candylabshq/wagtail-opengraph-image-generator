All available configuration options with their defaults.

---
## Image dimensions

Width and height of the generated image.

```python
WAGTAIL_OG_GENERATOR_IMAGE_WIDTH = 1200
WAGTAIL_OG_GENERATOR_IMAGE_HEIGHT = 630
```

---
## Image padding

Controls the amount of padding of the image.

```python
WAGTAIL_OG_GENERATOR_IMAGE_PADDING = 32
```

---
## Collection name

Name of the collection that the generated images will get sorted into. Will be created if it doesn't exist yet.

```python
WAGTAIL_OG_GENERATOR_COLLECTION_NAME = 'OpenGraph'
```

---
## Tab name

Name of the tab within the page edit/create views.

```python
WAGTAIL_OG_GENERATOR_TAB_NAME = 'Open Graph image'
```

---
## Page model

Path to your custom Page model, if any. Only matching object instances will be considered by the addon for image creation.

```python
WAGTAIL_OG_GENERATOR_PAGE_MODEL = 'wagtailcore.Page'
```

---
## Automatic image creation

If `True` an image will be automatically created and saved when matching objects, defined by `WAGTAIL_OG_GENERATOR_PAGE_MODEL` are saved.

```python
WAGTAIL_OG_GENERATOR_CREATE_AUTOMATICALLY = True
```

---
## Dynamic Fields

If your page model includes additional fields, you can use the following settings to make these fields accessible by the generator. For example, if your page has a field for a background image, this image can also be used as a background image for the Open Graph image.

Note: The `LOGO` field expects a SVG file, so basically a foreign key to a `wagtaildocs.Document` with valid SVG data.

```python
WAGTAIL_OG_GENERATOR_FIELD_SUBTITLE = ''
WAGTAIL_OG_GENERATOR_FIELD_BACKGROUND_IMAGE = ''
WAGTAIL_OG_GENERATOR_FIELD_LOGO = ''
```