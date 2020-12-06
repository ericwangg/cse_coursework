"Lab 3 - Eric Wang"

"Problem 1A"
(define (candy-left daynum pieces)
  (if (= daynum 1)
      (* 0.5 pieces)
      (* (- 1
            (/ 1 daynum))
            (candy-left (- daynum 1) pieces))))
       

       
"Problem 1A - Test"
(candy-left 2 100)
(candy-left 3 100)

"Problem 1B"
(define (candy-left-discrete daynum pieces)
  (floor (if (= daynum 1)
      (* 0.5 pieces)
      (* (- 1
            (/ 1 daynum))
            (candy-left-discrete (- daynum 1) pieces)))))

"Problem 1B - Test"
(candy-left-discrete 2 100)
(candy-left-discrete 3 100)

"Problem 2A"
(define (pell-num n)
  (cond
    ((= n 0) 0.0)
    ((= n 1) 1.0)
    (else (+ (* 2.0 (pell-num (- n 1))) (pell-num (- n 2))))))


"Problem 2A - Test"
(pell-num 3)
 
"Problem 2B"
(define (comp-pell-num n)
  (cond
    ((= n 0) 2.0)
    ((= n 1) 2.0)
    (else (+ (* 2.0 (comp-pell-num (- n 1))) (comp-pell-num (- n 2))))))

"Problem 2A - Test"
(comp-pell-num 3)


"Problem 2C"
(define (sqrt-2-approx n)
  (/ (/ (comp-pell-num n) (pell-num n)) 2))

"Problem 2C - Test"
(sqrt-2-approx 6)

"Problem 3A Binary Exponentiation"
(define (square x)
  (* x x))

(define (power base exp)
  (cond
    (( = exp 0) 1)
    (else
     (* base (power base (- exp))))))

(define (fastexp b e)
  (cond
    ((= e 0) 1)
    ((even? e) (square (fastexp b (/ e 2))))
    (else (* b (square (fastexp b (/ (- e 1) 2)))))))

"problem 3B"
"fastexp method is faster than 2^k because it considers for the evenness or oddness of the exponent,
then exvaluates the expressionl directly, as opposed to having to multiple 2*2*2*2... etc., which would be
much slower for a larger k"

"Problem 4A Square Root Continued Fraction"
(define (cont-frac k x)
  (if (= k 0)
      0
      (/ (- x 1)
         (+ 2 (cont-frac (- k 1) x)))))

"Problem 4B"
(define (new-sqrt x n)
  (define (cont-frac k)
    (if (= k 0)
        0
        (/ (- x 1) (+ 2 (cont-frac (- k 1))))))
    (+ 1 (cont-frac n)))

