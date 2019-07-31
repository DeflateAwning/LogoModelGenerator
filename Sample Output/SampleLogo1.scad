filename = "SampleLogo1.txt"; // filename of logo export from Python

origLength = 800;
finalLength = 160;

origWidth = 333;
finalWidth = finalLength/origLength * origWidth;

standAngle = 30; // angle from vertical of stand
standHeightPercent = 100; // how far up the width of the plaque to go
standThickness = 10;

MakeLogo();
//MakeStand();

module MakeLogo() {
    intersection() {
        mirror([0,1,0]) scale([finalLength/origLength, finalLength/origLength, 1]) surface(filename);
        
        // Future: optionally make rounded rectangle bounding box
    
    }
}

module MakeStand() {
    w = finalWidth * sin(standAngle);
    h = finalWidth * cos(standAngle);
    
    linear_extrude(standThickness) polygon([[0,0], [0, w], [h, w]]);
   
    echo("Angle is: ", 90-atan(h/w), " degrees");
} 