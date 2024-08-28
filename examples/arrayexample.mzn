% Definizione delle variabili
array[1..2] of var int: x;  % Array di variabili intere
var int: z;
% Vincoli
constraint x[1] >= 0;            % x[1] deve essere maggiore o uguale a 0
constraint x[2] >= 5;            % x[2] deve essere maggiore o uguale a 5
constraint x[1] + x[2] <= 20;    % La somma delle due variabili deve essere minore o uguale a 20
constraint x[1] <= 10;           % x[1] deve essere minore o uguale a 10
constraint x[2] - z <= 10;    % La differenza tra x[2] e x[1] deve essere minore o uguale a 10

% Risoluzione del problema
solve maximize x[1], maximize x[2];
