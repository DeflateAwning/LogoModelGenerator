# LogoModelGenerator
Generates a Color 3D Printable Model from a Logo (With Various Depths).

## Project Description
Using Python 3, an OpenSCAD model is outputted, based on the original logo image. Each color is at a different depth, allowing for filament changes in FDM 3D Printers, resulting in different colors.  This OpenSCAD model can then be rendered into an STL.

## How to Use
1. Clone the repository.
2. Ensure Python dependencies are installed (requires: `sudo pip3 install opencv-python`)
3. Run the `Model Generator.py` script, following the prompts.
  1. Select the location of the image file.
  2. Answer some questions about the output size, depth between colors, etc.
  3. Select each color, and press any key when finished.
  4. Take note of the specified heights/predicted layer numbers to pause the print.
4. View the outputted OpenSCAD model. Open it with OpenSCAD, and render an STL.
5. 3D Print the Model
  1. Slice the model using your favourite tool, being sure to add pauses on the specified layers.
  2. Print the model, performing the suggested filament color changes on pauses.
  3. Enjoy!
