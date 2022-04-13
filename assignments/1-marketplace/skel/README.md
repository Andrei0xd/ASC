Pentru rezolvarea temei, am ales sa folosesc in mare parte liste, atat pentru cozile producerilor cat si pentru carturi.
Astfel, am avut acces la metode .add() si .remove() care sunt thread safe. Datorita acestui lucru, nu a trebuit sa folosesc si
alte mecanisme de sincronizare.

Rezolvarea deci consta intr-un dictionar unde cheile sunt id-urile producerilor, iar valorile sunt liste care reprezinta cozile acestora.
Aceeasi structura o au si carturile. Cand un consumer vrea sa isi puna un produs in cart, acesta verifica in toate cozile daca exista si il alege pe primul.
Cand un consumer vrea sa dea remove, el tine minte, in lista cartului, producerul de la care a venit si il poate pune inapoi in aceeasi coada din care l-a luat.


Pe langa metodele existente in schelet, am implementat o singura metoda in plus, de generare a unor id-uri unice pentru producer si pentru carturi.

Consider tema foarte utila pentru cineva care doreste sa invete python, deoarece trece prin multe lucruri necesare de stiut cum ar fi clase, sincronizare, linting, unit testing, logging.

O posibila problema cu enuntul/testele este urmatoarea: Am ales sa fac implementarea initial fara sa tin cont de queue_size_per_producer, iar la rularea testelor toate au trecut.