# AF_module_automatition
Python code for atomating the AF module

# Automated DH PSF rotation detection

For further information about the optical vortieces and DH PSFs see for example:

<div class="csl-entry">Bouchal, P., &#38; Bouchal, Z. (2017). Flexible non-diffractive vortex microscope for three-dimensional depth-enhanced super-localization of dielectric, metal and fluorescent nanoparticles. <i>Journal of Optics (United Kingdom)</i>, <i>19</i>(10). https://doi.org/10.1088/2040-8986/aa87fb</div>

## Scheme of the image processing

1. Threshold.
2. Cast image to binary mask.
3. Use funtion to find circles or another segmentation technique.
4. Get data about the circles.
5. Measure the absolute angle of the circles centres.