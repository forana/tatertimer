pt = 0.2; // printer tolerance
pth = pt/2;
$fn = 16;

piHeight = 30.3;
piWidth = 65;
piR = 3;
piBoardThickness = 1.5;

mountDiameter = 2.4;
mountRadius = mountDiameter / 2;
mountClearance = 6.8;
mountInset = mountClearance/2;

switchBoardWidth = 18.1;
switchBoardHeight = 23.5;
switchX = piWidth - 11 - switchBoardWidth;
switchY = piHeight - 4.2 - switchBoardHeight;
switchExtraDepth = 3;
switchExtraInset = 4;
switchExtraX = switchX + switchExtraInset;
switchExtraY = switchY;
switchExtraWidth = switchBoardWidth - 2*switchExtraInset;
switchExtraHeight = switchBoardHeight/2;

screenWidth = 27.5;
screenHeight = 27.5;
screenX = 7.5;
screenY = (piHeight - screenHeight)/2;

screenCornerWidth = 3.8;

boardAndScreenThickness = 12;
boardAndSwitchThickness = 8;
screenRiserHeight = boardAndScreenThickness - boardAndSwitchThickness;

switchWellHeight = 5;
switchWellWidth = 14;
switchWellX = switchX + ((switchBoardWidth - switchWellWidth)/2);
switchWellY = switchY + ((switchBoardWidth - switchWellWidth)/2) + (switchBoardHeight - switchBoardWidth);

// floor
caseTopThickness = 5;
caseThickness = 2;
// walls
wallThickness = 2;
// holding clips
clipThickness = 1;


translate([-piWidth/2, piHeight/2, 0])
    caseTop();
translate([-piWidth/2, -piHeight*3/2, 0])
    caseBottom();


module caseTop() {
    difference() {
        linear_extrude(0, 0, caseTopThickness)
            roundedRectWithHoles(piWidth, piHeight, piR, mountInset, mountRadius + pth);
        // mounting corners
        translate([0, 0, caseThickness])
            linear_extrude(0, 0, caseTopThickness) union() {
                translate([-mountClearance, -mountClearance, 0])
                    roundedRect(2*mountClearance, 2*mountClearance, piR);
                translate([piWidth-mountClearance, -mountClearance, 0])
                    roundedRect(2*mountClearance, 2*mountClearance, piR);
                translate([piWidth-mountClearance, piHeight-mountClearance, 0])
                    roundedRect(2*mountClearance, 2*mountClearance, piR);
                translate([-mountClearance, piHeight-mountClearance, 0])
                    roundedRect(2*mountClearance, 2*mountClearance, piR);
        }
        // screen well
        linear_extrude(0, 0, screenRiserHeight)
            translate([screenX-pth, screenY-pth, 0])
                square([screenWidth+pt, screenHeight+pt]);
        // screen cutout w/ corner clips
        linear_extrude(0, 0, caseTopThickness + 1) // +1 to cut through in preview
            translate([screenX-pth, screenY-pth, 0]) union() {
                roundedRect(screenWidth+pt, screenHeight+pt, screenCornerWidth);
            }
        // switch well
        linear_extrude(0, 0, switchWellHeight + 1) // +1 to cut through in preview
            translate([switchWellX-pth, switchWellY-pth, 0])
                square(switchWellWidth+pt);
        // switch extras well
        linear_extrude(0, 0, switchExtraDepth)
            translate([switchExtraX-pth, switchExtraY-pth, 0])
                square([switchExtraWidth+pt, switchExtraHeight+pt]);
    }
}

module caseBottom() {
        linear_extrude(0, 0, caseThickness)
            intersection() {
                union() {
                    difference() {
                        roundedRectWithHoles(piWidth, piHeight, 0, mountInset, mountRadius + pth);
                        translate([mountClearance, piHeight - mountClearance, 0])
                            square([piWidth - 2*mountClearance, mountClearance]);
                    }
                    translate([0, piHeight, 0])
                        square([piWidth, mountClearance]);
                }
                roundedRectWithHoles(piWidth, piHeight + mountClearance, piR, mountInset, mountRadius + pth);
            }
}

module roundedRect(w, h, r) {
    if (r > 0) {
        translate([r, r, 0]) minkowski() {
            circle(r);
            square([w - 2*r, h - 2*r]);
        }
    } else {
        square([w, h]);
    }
}

module roundedRectWithHoles(w, h, r, inset, hr) {
    difference () {
        roundedRect(w, h, r);
        translate([inset, inset, 0]) circle(hr);
        translate([w-inset, inset, 0]) circle(hr);
        translate([w-inset, h-inset, 0]) circle(hr);
        translate([inset, h-inset, 0]) circle(hr);
    }
}