"Problem Set 5 - Eric Wang"

"1A - Prefix"
(define (is-prefix? a b)
  (if (= (car a) (car b))
       #t
       #f))

(is-prefix? '(1) '(1 2))
(is-prefix? '(1 2) '(1 2 3))

"1B - Common Prefix"
(define (longest-common-prefix a b)
  (cond ((null? a) '())
        ((null? b) '())
        ((= (car a) (car b))
         (cons (car a) (longest-common-prefix (cdr a) (cdr b))))
        (else '())))

(longest-common-prefix '(1 2) '(1 2 3))
(longest-common-prefix '(2 3 4) '(2 3 4 5 6))
(longest-common-prefix '(0 3 9) '(53 6 2 0 9 33 12 2 6))



"2A - Generalized Consecutives"
(define (gen-consecutive f a b)
  (if (> a b)
      '()
      (cons (f a) (gen-consecutive f (+ a 1) b))))

"2B - More General Consecutives"
(define (gen-sequence f a b next stop)
   (if (> a b)
      '()
      (cons (f a) (gen-consecutive f (+ a 1) b)))) 

"3 - Filter"
(define (filter f lst)
  (cond ((null? lst) '())
        ((f (car lst))
         (cons (car lst) (filter f (cdr lst))))
        (else (filter f (cdr lst)))))



"4 - Reverse Boolean of Functions"
(define (fun-not f)
  (lambda (x) (not (f x))))



"5A - Property holds for Every? list"
(define (every? f lst)
  (if (null? lst)
      #t
      (cond ((f (car lst)) (every? f (cdr lst)))
            (else #f))))

"5B - Property holds for Some? list"
(define (some? f lst)
  (if (null? lst)
      #f
      (cond ((f (car lst)) #t)
            (else (some? f (cdr lst))))))

  

"6A - List eval to value at kth position"
(define (value-at-position lst k)
  (define (counter lst k n)
    (cond ((= k n) (car lst))
          ((> n (length lst)) 0)
          (counter (cdr lst) k (+ m 1))))
  (counter lst k 1))

"6B - Nth primes"
(define (nth-prime-between a b n)
  (define (prime? n)
    (define (divisor a) (= (modulo n a) 0))
    (define (smooth k)
      (and (>= k 2)
           (or (divisor k)
               (smooth (- k 1)))))
    (and (> n 1)
         (not (smooth (floor (sqrt n))))))
  (if (> a b)
      '()
      (value-at-position
       (filter prime? (gen-consecutive
                       (lambda (x) (+ x 0)) a b))
       n)))


"Problem 7 - Complex Numbers"
;complex data type implementation
(define (make-complex a b)
  (cons a b))
;construct a complex number with real part "a" and imaginary part "b"

(define (real x)
  (car x))
; returns the real part of a complex number
(define (imag x)
  (cdr x))
; returns the imaginary part of a complex number

; utilities built from complex datatype
(define (complex-add x y)
  (make-complex
   (+ (real x) (real y))
   (+ (imag x) (imag y))))

(define (complex-sub x y)
  (make-complex
   (- (real x) (real y))
   (- (imag x) (imag y))))

(define (complex-mult x y)
  (make-complex
   (- (* (real x) (real y))
      (* (imag x) (imag y)))
   (+ (* (real x) (real y))
      (* (imag x) (imag y)))))

(define (complex-conj x)
  (make-complex (real x) (- (imag x))))

; Some fake code below
(define (complex-sqrt x) (+ x 1))

"7A - Complex Squar Root, Gamma"
;(define (complex-sqrt x)
;  (let ((square (* x x)))
;    (cond ((> a 0) (sqrt (/ (+ a (sqrt (+ (square a) (square b)))) 2)))
;          ((< a 0) (cond ((< b 0) ((sqrt (/ (+ (* -1 a) (sqrt (+ (square a) 1)))2))))
;                         ((= b 0) ((sqrt (/ (+ (* -1 a) (sqrt (square a))) 2))))
;                         (else ((sqrt (/ (+ (* -1 a) (sqrt (+ (square a) 1))) 2)))))))))

(define (make-complex a b)
  (cons a b))
(define (complex-sqrt x)
  (let ((a (car x)) (b (cdr x)))
    (let ((c (sqrt (+ (* a a) (* b b)))))
      (define (signum b)
        (if (> b 0)
            -1
            (if (= b 0)
                0
                1)))
      (define (gamma x)
        (sqrt (/ (+ a c) 2)))
      (define (delta x)
        (* (signum b) (sqrt (/ (+ (* -1 a) c) 2))))
      (cons (gamma x) (delta x)))))

"7B - Complex Square Root Better, delta = signum(b)"
;(define (complex-sqrt-better x)
;  (let ((square (* x x)))
;    (sqrt (/ (+ a (sqrt (+ (square a) (square b)))) 2))))

(define (complex-sqrt-better x)
  (let ((a (car x)) (b (cdr x)))
    (let ((c (sqrt (+ (* a a) (* b b)))))
      (define (signum b)
        (if (> b 0)
            -1
            (if (and (= b 0) (> a 0))
                0
                1)))
      (define (gamma x)
        (sqrt (/ (+ a c) 2)))
      (define (delta x)
        (* (signum b) (sqrt (/ (+ (* -1 a) c) 2))))
      (cons (gamma x) (delta x)))))