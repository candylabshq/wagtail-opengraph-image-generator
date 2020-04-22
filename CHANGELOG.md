# 1.1

- New: Added custom hook `wagtail_opengraph_image_generator_generation` for total control of the image generation process
- New: Add support for a custom title field with the same behavior as the subtitle field. The fallback title is still the default Wagtail page title
- Fix: Reset the preview button on server errors
- Mention necessary `wagtail.contrib.settings` in the README

# 1.0.2

- Fix: Make addon work with externally hosted images, like S3
- Fix: Avoid cache issues on images hosted via a CDN by adding a random suffix

# 1.0.1

- Fix: Make addon work when creating new pages

# 1.0.0

- Initial release
