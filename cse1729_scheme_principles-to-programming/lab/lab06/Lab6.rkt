"Lab 6 - Eric Wang"

"1A - List Functions"
(define (count-positives lst)
  (if (null? lst)
      0
      (if (> (car lst) 0)
          (+ 1 (count-positives (cdr lst)))
          (count-positives (cdr lst)))))

"1B - List Product"
(define (multiply-list lst)
  (if (null? lst)
      1
      (* (car lst) (multiply-list (cdr lst)))))

"1C - Consecutive Integers"
(define (consecutive-ints a b)
  (if (> a b)
      '()
      (cons a (consecutive-ints (+ a 1) b))))

"1D - Counsecutive Squares"
(define (square x)
  (* x x))

(define (consecutive-squares a b)
  (if (> a b)
      '()
      (cons (square a) (consecutive-squares (+ a 1) b))))

"2 - List Elements"
(define (count-if f lst)
  (if (null? lst)
      0
      (if (f (car lst))
          (+ 1 (count-if f (cdr lst)))
          (count-if f (cdr lst)))))

"3A - Interesting Natural Numbers"
(define (nth-filtered f n)
  (define (helper f accum s)
    (cond ((= accum 0) (- s 1))
          ((f s) (helper f (- accum 1) (+ s 1)))
          (else (helper f accum (+ s 1)))))
  (helper f n 1))

(nth-filtered even? 3)
(nth-filtered odd? 1)

(define (nth-filtered f n)
  (define (n-check f k)
    (if (f k) 1 0))
  (define (n-count f accum k n)
    (if (= accum n)
        (- k 1)
        (n-count f (+ accumt (n-check f k) (+ k 1) n))))
  (n-count f 0 1 n))

(nth-filtered even? 3)
(nth-filtered odd? 1)

"3B - Approx min value"
(define (min-value f a b)
  (let ((m (/ (+ b a) 2)))
  (if (< (abs (- a b)) 0.0001)
      (f a)
      (min (min-value f a m) (min-value f m b)))))
