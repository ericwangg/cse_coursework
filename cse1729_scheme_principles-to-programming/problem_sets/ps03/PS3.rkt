;;  code that provides random function

;ensure that random is defined at top level
(define (random) .5)

; initialize random, optionally with given seed between 1 and 2^31-1
; if no seed given, uses 1043618065
(define (init-random . user-seed)
  (define (next-val seed)
    (let* ((a 16807.0) ; 7^5
           (m 2147483647.0) ; 2^31-1
           (t (* a seed)))
      (- t (* m (floor (/ t m))))))
  (set! random
        (let ((seed  (if (null? user-seed) 1043618065 (car user-seed))))
          (lambda()
            (set! seed (next-val seed))
            (/ seed 2147483647.0)))))

(init-random)

; after this, (random) will produce a pseudorandom number r, 0.0 < r < 1.0

"Problem Set 3 - Eric Wang"

"Problem 1A - Harmonic Numbers"
(define (harmonic n)
  (if (= n 1)
      1
      (+ (/ 1.0 n) (harmonic (- n 1)))))

"P1A - Test "
(harmonic 5)

"Problem 1B"
(define (euler-approx n)
  (- (harmonic n) (log n)))



"Problem 2A"
(define (prime? n)
  (define (divisor? k) (= 0 (modulo n k)))
  (define (divisors-upto k)
  (and (> k 1)
       (or (divisor? k) (divisors-upto (- k 1)))))
  (not (divisors-upto (- n 1))))

(define (nth-prime-from n k)
  (if (and (= n 1) (prime? k))
      k
      (cond ((prime? k) (nth-prime-from (- n 1) (+ k 1)))
            ((not (prime? k)) (nth-prime-from n (+ k 1))))))

"Problem - 2B"
(define (nth-prime n)
  (nth-prime-from n 2))



"Problem 3A"
(define (lucas n)
  (cond
   ((= n 0) 2)
   ((= n 1) 1)
   (else (+ (Lucas (- n 1)) (Lucas (- n 2))))))

"Problem 3B"
(define (lucas-ratio n)
  (/ (+ 0.0 (lucas n)) (+ 0.0 (lucas (- n 1)))))

(define (fibonacci n)
  (cond
    ((= n 0) 0)
    ((= n 1) 1)
    (else (+ (fibonacci (- n 1))
             (fibonacci (- n 2))
             )
          )
    )
  )

(define (fibonacci-ratio n)
  (/ (+ 0.0 (fibonacci n))
     (+ 0.0 (fibonacci (- n 1)))
     )
  )

"P3B - Test"
(fibonacci-ratio 20)
(fibonacci-ratio 21)
(fibonacci-ratio 22)
"The Fibonacci ratio is converges upon a number 'Phi', about 1.618, the further we take this fibonacci ratio,
 the more accurate the number is to Phi"

"Problem 4A"
(define (square z)
  (* z z))

(define (power base exp)
  (cond
    (( = exp 0) 1)
    (else
     (* base (power base (- exp))))))

(define (fast-expt b e)
  (cond
    ((= e 0) 1)
    ((even? e) (fast-expt (square b) (/ e 2)))
    (else (* b (fast-expt (square b) (/ (- e 1) 2))))))

"P4A - Tests"
(fast-expt 5 4)
(fast-expt 4 5)

"Problem 4B - nth root approximation"
(define (nth-root-approx x n tol)
  (define (nth-root-converge a b)
    (let ((avg (/ (+ (* a (- n 1.0)) b) n)))
      (if (< (abs (- a b)) tol)
              a
              (if (> (fast-expt avg n) x)
                  (nth-root-converge a avg)
                  (nth-root-converge avg b)))))
    (nth-root-converge 1 x))

(nth-root-approx 1000 3 0.000001)

"Problem 4C - nth root of n"
(define (nth-root-of-n-approx n tol)
  (nth-root-approx n n tol))

"Problem 5A - Golden Ratio"
(define (golden n)
  (define (layers n)
    (if (= n 1)
        1
        (/ 1 (+ 1 (layers (- n 1))))))
  (+ 1 (layers n)))

(golden 5)

"Problem 5B - Golden Square Root"
(define (golden-sqrt n)
  (if (= n 0)
      1
      (sqrt (+ 1 (golden-sqrt (- n 1))))))

;(golden-sqrt 5)

"Problem - 6A"
(define (tosses-taken a b)
  (define (helper a b c)
    (let ((percent (random)))
      (cond ((= a 0) c)
            ((= b 0) (* -1 c))
            ((> percent 0.5) (helper (- a 1) (+ b 1) (+ c 1)))
            (else (helper (+ a 1) (- b 1) (+ c 1))))))
  (helper a b 0))

(tosses-taken 4 6)

"Problem - 6B"
(define (count-wins a b n)
  (define (helper a b n count)
    (let ((total (tosses-taken a b)))
      (cond ((= n 0) count)
            ((< total 0) (helper a b (- n 1) (+ count 1)))
            (else (helper a b (- n 1) count)))))
    (helper a b n 0))

(count-wins 4 6 10)
             
  

"Problem 7A - Approximating Pi with Random Dart Throws"
(define (one-sample)
  (define (morph z) (- (* 2 z) 1 ))
  (let ((x (morph (random)))
        (y (morph (random))))
    (if (< (sqrt (+ (* x x)(* y y))) 1)
        #t
        #f)))

"Problem - 7B"
(define (one-sample2)
  (define (morph z) (- (* 2 z) 1 ))
  (let ((x (morph (random)))
        (y (morph (random))))
    (if (< (sqrt (+ (* x x)(* y y))) 1)
        1
        0)))

(define (pi-samples k)
  (if (= k 0)
      0
      (+ (one-sample2)
         (pi-samples (- k 1)))))

"Problem - 7C"
(define (pi-approx k)
  (* 4 (/ (pi-samples k) k)))

"P7C - Test"
(pi-approx 1000)

"Problem - 8A"
(define (interval-sum m n)
  (if (= m n)
      m
      (+ n (interval-sum (- n 1)))))

(define (interval-sum m n)
  (if (= m n)
      m
      (+ m (interval-sum (+ m 1) n))))

(define (interval-sum2 m n)
  (if (= m n)
      m
      (+ m
         (inteval-sum2 (+ m 1) (- n 1)
                       n))))

;Previous given methods of summing the intergers between m & n, interval-sum2 should fix the issue where
;the previous functions don't work with certain pairs of m & n.

(define (ok-for-interval-sum2 m n)
  (if (= m n)
      n
      (+ m ok-for-interval-sum2 (- n 1))))