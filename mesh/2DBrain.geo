cl2 = 0.003;
radius = 0.03;
outer = 0.1;

// Circle & surrounding structured-quad region
Point(5) = {0, 0, 0, cl2};
Point(6) = {0,  radius, 0, cl2};
Point(7) = {0, -radius, 0, cl2};
Point(8) = {0,  outer, 0, cl2};
Point(9) = {0, -outer, 0, cl2};
Point(10) = {radius,  0, 0, cl2};
Point(11) = {-radius, 0, 0, cl2};
Point(12) = {outer,  0, 0, cl2};
Point(13) = {-outer, 0, 0, cl2};

Circle(5) = {7, 5, 10};
Circle(6) = {6, 5, 11};
Circle(7) = {8, 5, 13};
Circle(8) = {9, 5, 12};


Circle(13) = {10, 5, 6};
Circle(14) = {11, 5, 7};
Circle(15) = {13, 5, 9};
Circle(16) = {12, 5, 8};


Line Loop(1) = {7, 15, 8, 16}; // Exterior
Line Loop(2) = {6, 14, 5, 13}; // Interior

Plane Surface(1) = {1, 2};

Extrude {0,0,0.006} {
  Surface{1};
}

