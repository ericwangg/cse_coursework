"Problem Set 4 - Eric Wang"
(define pi 3.14159265358979)

"Problem 1 - Pi Notation Iteration"
(define (product term a next b)
  (if (> a b)
      1
      (* (term a) (product term (next a) next b))))

"Problem 1B - Pi Notation Recusion"
(define (product-i term a next b) 
   (define (iter a acc) 
     (if (> a b)
         acc
         (iter (next a) (* (term a) acc)))) 
    (iter a 1))

"Problem 1C - Pi Approximation"
"Defining 'add1' for convenience"
(define (add1 n) (+ 1 n))

"(define (pi-approx n)
  (define (term x) (* x x))
  (define (next x) (+ x 2))
  (define limit (* n 2))
  (* 4 (/
        (/ (* 2 (product-i term 4 next (+ limit 2)))
           (+ limit 2))
        (product-i term 3 next (+ limit 1)))))"
    
"(define (pi-approx n)
((define (product-i term a next b) 
   (define (iter a acc) 
     (if (> a b)
         acc
         (iter (next a) (* (term a) acc)))) 
    (iter a 1)))
   (if (even? n) 
       (* 4 (product-i (/ (+ n 2) (+ n 1)) 1 next n) 
       (* 4 (product-i (/ (+ n 1) (+ n 2)) 1 next n)))))"

(define (pi-term n)
  (cond ((= n 0) 1)
        ((even? n) (/ (+ n 2) (+ n 1)))
        (else (/ (+ n 1) (+ n 2)))))

(define (quarter-pi-approx n)
  (product pi-term 1 add1 n))

(define (pi-approx n)
  (* 4 (quarter-pi-approx n)))

;Possible code for John Wallis formula by including product-i numberator and denoinator of pi-approx

; Test 1
; (/ (product-i (lambda (x) (* x (x + 2))) 2 (lambda (x) (+ x 2)) +inf.0)
; (product-i (lambda (x) (* x (+ x 2))) 3 (lambda (x) (+ x 2)) +inf.0))))

; Test 2
; (product (/ (+ n 2) (+ n 1)) 1 (- n 1) n)
; (product (/ (+ n 1) (+ n 2)) 1 (- n 1) n)))

"Problem 1D"
(pi-approx 6.0)
(pi-approx 100.0)
(pi-approx 1000.0)
"These test demonstrate that pi-approx can be approximated closer to the actual value of pi
the greater terms of 'n' we use, but the amount of digits for 'n' used, is the degree of accuracy 'pi' is"


"Problem 2A - Derivatives"
(define (der f h)
  (lambda (x) 
    (/ (- (f (+ x h)) (f x))
       h)))

"Problem 2B - Sines and Cosines Comparison"
"Sin 0"
((der sin 0.5) 0)
"Cosine 0"
(cos 0)
"Sin Pi/2"
((der sin 0.5) (/ pi 2))
"Cosine Pi/2"
(cos (/ pi 2))
"Sin Pi"
((der sin 0.5) pi)
"Cos Pi"
(cos pi)
"Sin 3pi/4"
((der sin 0.5) (* pi 0.75))
"Cos 3pi/4"
(cos (* pi 0.75))
     

"Problem 2C - Function"
(define (fun x)
  (+ (* 3 x x) (* -2 x) 7))

"Deriv 6X-2 (X = 1)"
(- (* 6 1) 2)
"Function Deriv X=1"
((der fun 0.01) 1)
"Deriv 6X-2 (X = 2)"
(- (* 6 2) 2)
"Function Deriv X=2"
((der fun 0.01) 2)
"Deriv 6X-2 (X = 3)"
(- (* 6 2) 3)
"Function Deriv X=3"
((der fun 0.01) 3)

"Problem 2D - nth Derivative"
(define (nth-deriv f n h)
  (cond
    ((= n 1) (der f h))
    ((der (nth-deriv f (- n 1) h) h))))

"Test nth-deriv of Sin 3 (limit 0.0001) 3"
((nth-deriv sin 3 0.0001) 3)
"Test cos of 3"
(* -1 (cos 3))
               



"Problem 3A - SICP 1.44 Smooth"
(define (smooth f dx)
  (lambda (x)
    (/ (+ (f x)
       (f (+ x dx))
       (f (- x dx)))
       3)))

"Problem 3B - Repeatedly Smoothed"
"Compose & Repeated from SICP 1.43"
(define (compose f g)
  (lambda (x) (f (g x))))
(define (repeated f n)
  (if (= n 1)
      f
      (compose f (repeated f (- n 1)))))

(define (smoother dx)
  (lambda (f) (smooth f dx)))

;nah screw smoother

(define (n-fold-smooth f dx n)
  (cond ((= n 1) (smooth f dx))
        ((smooth (n-fold-smooth f dx (- n 1)) dx))))

"(define (n-fold-smooth f dx n)
  (repeated (smooth f dx) n))  - this code also works, doesn't pass 3B"

"Problem 4 - Ackermann Function"
(define (ack m n)
  (cond
    ((= m 0) (+ n 1))
    ((and (> m 0)(= n 0)) (ack (- m 1) 1))
    (else (ack (- m 1) (ack m (- n 1))))))

(ack 3 4)
(ack 4 0)



"Problem 5 - Max, Use function that's greater"
(define (max-fg f g)
  (lambda (x)
    (if (> (f x) (g x))
        (f x)
        (g x))))



"Problem 6 - Romberg's Method"
(define (sum-i term a next b)
  (define (iter acc x)
    (if (> x b)
        acc
        (iter (+ acc (term x)) (next x))))
  (iter 0 a))

(define (power base exp)
  (cond
    (( = exp 0) 1)
    (else
     (* base (power base (- exp))))))

; h (sub) n  -   (* (/ 1 (power 2 n))(- b a))
; just recode, 
(define (h-sub-n a b n) (/ (- b a) (expt 2 n)))
; the "integrand" of summation for 2nd cond ladder term  -
;(* (f (+ a (- (* 2 k) 1))) (* (/ 1 (power 2 n))(- b a)))

(define (romberg f a b n m)
  (cond
      ((and (= n 0) (= m 0))
       (* (h-sub-n a b 1) (+ (f a) (f b))))
      ((and (not (= n 0)) (= m 0))
                 (+ (* (romberg f a b (- n 1) m) 0.5)
                    (* (h-sub-n a b n) (sum-i (lambda (k) (f (+ a (* (- (* 2 k) 1) (h-sub-n a b n)))))
                                         1 add1 (expt 2 (- n 1))))))
       ((+ (romberg f a b n (- m 1))
           (/ (- (romberg f a b n (- m 1)) (romberg f a b (- n 1) (- m 1)))
              (- (expt 4 m) 1))))))                                                                                            
                             
"(romberg (lambda (x) (+ (* 3.0 x x) x)) 0 5 2 0)"
(romberg (lambda (x) (+ (* 3.0 x x) x)) 0 5 2 0)

;Included helper function romberg-method, try again, include sum correctly
"((and (not n 0) (= m 0))
       (+ (* 0.5 (romberg-method (- n 1) 0)))
       (* (* (/ 1 (power 2 n))(- b a))
          (sum-i 1 a (- (power 2 n) 1) b)   
          (else (-
                 (+ (romberg-method n (- m 1))
                    (* (/ 1 (- (power 4 m) 1)) (romberg-method (n (- m 1)))))
                 (romberg-method (- n 1) (- m 1))))))))))"