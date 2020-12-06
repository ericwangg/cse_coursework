"Problem Set 1 - Eric Wang"

"1A"
(define (square x)
  (* x x))

"1B"
(define (cube x)
  (* x x x))

"1C"
(define (p x)
  (+(*(cube x)
      (square x))
    (* 11
       (square x)
       (square x))
    (* 24
       (cube x))
    (- x)
    39))
     
(define (sp x)
  (square(p x)))


"1D"
(define (eighth x)
  (*(cube x)
    (cube x)
    (square x)))

"1E"
(define (sixty-fourth x)
  (eighth(eighth x)))

"2A"
(define (is-triangle? a b c)
  (if (and (>= (+ a b) c)
           (>= (+ a c) b)
           (>= (+ b c) a))
      #t
      #f))

"2B"
(define (s2b a b c)
  (/ (+ a b c)2))
(define (area a b c)
  (sqrt
   (*(s2b a b c)
     (-(s2b a b c)a)
     (-(s2b a b c)b)
     (-(s2b a b c)c))))

"2C"
(define (op-angle a b c)
  (acos(/
        (+
         (square b)
         (square c)
         (- (square a)))
        (* 2 b c))))

"3"
(define (fib-cf n)
  (* (/ 1 (sqrt 5))
     (- (expt (/
               (+ 1 (sqrt 5))
               2)
              n)
        (expt (/
               (- 1 (sqrt 5))
               2)
              n))))

"4A"
(define (root1 a b c)
  (/ (+ (- b)
        (sqrt (-
               (square b)
               (* 4 a c))))
     (* 2 a)))

"4B"
(define (root2 a b c)
  (/ (- (- b)
        (sqrt (-
               (square b)
               (* 4 a c))))
     (* 2 a)))

"4C"
(define (number-of-roots a b c)
  (if (= (root1 a b c)
         (root2 a b c))
      1
      2))

"4D"
(define (real-roots? a b c)
  (if (>= (-
           (square b)
           (* 4 a c))
      0)
  #t
  #f))
         
        
        
  
  

  
