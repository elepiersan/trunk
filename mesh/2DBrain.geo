cl2 = 0.003;
radius = 0.03;
outer = 0.1;
P1x = 0.007;
theta = Asin(P1x/outer);
P1y = -outer*Cos(theta);
L = 0.13;
// Circle & surrounding structured-quad region
Point(5) = {0, 0, 0, cl2};

Point(6) = {0,  radius, 0, cl2};
Point(7) = {-P1x, P1y, 0, cl2};
Point(77) = {P1x, P1y, 0, cl2};

Point(8) = {0,  outer, 0, cl2};
Point(9) = {0, -radius, 0, cl2};
Point(10) = {radius,  0, 0, cl2};
Point(11) = {-radius, 0, 0, cl2};
Point(12) = {outer,  0, 0, cl2};
Point(13) = {-outer, 0, 0, cl2};

Point(14) = {-P1x, P1y-L, 0, cl2};
Point(15) = { P1x, P1y-L, 0, cl2};

Circle(5) = {9, 5, 10};
Circle(6) = {6, 5, 11};
Circle(7) = {8, 5, 13};
Circle(8) = {77, 5, 12};


Circle(13) = {10, 5, 6};
Circle(14) = {11, 5, 9};
Circle(15) = {13, 5, 7};
Circle(16) = {12, 5, 8};

Line(18) = {7, 14};
Line(19) = {14, 15};
Line(20) = {15, 77};

Line Loop(1) = {7, 15, 18, 19, 20, 8, 16}; // Exterior
Line Loop(2) = {6, 14, 5, 13}; // Interior

Plane Surface(1) = {1, 2};

Extrude {0,0,0.012} {
  Surface{1};
}

