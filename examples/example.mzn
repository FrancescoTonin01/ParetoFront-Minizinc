var 0..40: x;
var 0..40: y;
% Constraint
constraint x + 2*y <=40;
constraint 3*x + y >= 36;
solve maximize x, maximize y;
