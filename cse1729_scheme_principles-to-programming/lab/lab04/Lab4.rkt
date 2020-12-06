"Lab 4 - Eric Wang"

"Problem - 1A - Lucas Ratio Slow?"
(define (Lucas n)
  (cond
   ((= n 0) 2)
   ((= n 1) 1)
   (else (+ (Lucas (- n 1)) (Lucas (- n 2))))))

;(Lucas 30)
;(Lucas 35)
;(Lucas 40)
"Attempting to compute Lucas of n = 50 would result in the program timing out, it would take forever
with the current method"

"Problem - 1B - Fast Lucas Ratio"
(define (fast-Lucas-help n k lucas-a lucas-b)
  (if (= n k)
      lucas-a
      (fast-Lucas-help n (+ k 1) (+ lucas-a lucas-b) lucas-a)))

(define (fast-Lucas n) (fast-Lucas-help n 1 1 2))

"Problem - 2A Improved Harmonic Function"
(define (harmonic n)
  (if (= n 1)
      1
      (+ (/ 1.0 n) (harmonic (- n 1)))))

(define (sum term a next b)
  (if (> a b)
    0
    (+ (term a)
       (sum term (next a) next b))))

"(define sum-i term a next b)
  (define (iter a result)
    (if (> a b)
        result
        (iter ))))"

"(define (sum-iter index n sum)
  (if (= n index)
      (+ sum index)
      (+ (sim-iter n (+ index 1) (+ sum index)))))

(define (sum-i a b)
  (sum-iter a b 0))"

(define (sum-i term a next b)
  (define (iter acc x)
    (if (> x b)
        acc
        (iter (+ acc (term x)) (next x))))
  (iter 0 a))

(define (harmonic-i n)
  (sum-i (lambda (x) (/ 1 x)) 1 (lambda (x) (+ x 1)) n))
              
"Problem - 2C"
(harmonic-i 1.0)
(harmonic-i 50.0)
(harmonic-i 100.0)



"Problem - 3 SICP 1.42"
(define (compose f g)
  (lambda (x) (f (g x))))

"Problem - 4 SICP 1.43"
(define (repeated f n)
  (if (= n 1)
      f
      (compose f (repeated f (- n 1)))))

"Problem - 5"
(define (m91 x)
  (cond ((> x 100) (- x 10))
        ((<= x 100) ((repeated m91 91) (+ x 901))     )))