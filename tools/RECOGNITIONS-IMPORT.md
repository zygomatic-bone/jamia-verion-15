# Importing the original Awards & Recognition photographs

The legacy site (jameululoom.org/Recognitions.html) could not be reached from the build environment, and the original
main-site files were never supplied, so no photographs were imported or invented.

To add them (no code changes needed):
1. Put the original image files in `public/portal-assets/recognitions/` (keep original names/aspect ratios).
2. Create `tools/recognitions.json`:
   `[{"file": "award1.jpg", "caption": "Original caption", "alt": "What the photo actually shows"}, ...]`
3. Run `python tools/build.py`. `Recognitions.html` then gains a "Photographs" gallery (whole images, original ratio,
   responsive). With no JSON file the page is unchanged.
