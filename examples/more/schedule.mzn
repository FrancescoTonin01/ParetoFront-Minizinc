int: n;
var int: pavimento;
var int: accatastate;
array[1..n,1..3] of int: scatola;


array[1..n] of var 0..n: sotto;

% Una scatola non puo` essere sopra se stessa
constraint forall(i in 1..n)
            (sotto[i]!=i);

% Se la scatola i e` sopra una scatola sotto[i], allora sotto[i] deve essere piu` grande in entrambe le dimensioni
constraint forall(i in 1..n)
  (  if sotto[i]>0 
     then forall(dimension in 2..3)
                    (scatola[i,dimension]<=scatola[sotto[i],dimension])
     else true 
     endif
  );

constraint 
  forall(i in 1..n)
    (forall(j in 1..n where j>i)
      ( if sotto[i]>0
        then sotto[i] != sotto[j]
        else true
        endif
      )
    );


constraint pavimento = sum([sotto[i] = 0 | i in 1..n]);
constraint accatastate = sum([scatola[i, 2] * scatola[i, 3] | i in 1..n where sotto[i] = 0]);

solve minimize pavimento, minimize accatastate;
