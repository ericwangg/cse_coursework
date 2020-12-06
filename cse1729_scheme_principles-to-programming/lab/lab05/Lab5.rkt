"Lab 5 - Preliminary Examination 1 Review"

"Problem 1A - USB to Bitcoin"
(define (USD-to-Bitcoin x)
  (/ x 389.943))

"Problem 1B - Energy from Mass"
(define (energy-from-mass m)
  (let ((c 299792458))
  (* m c c)))

"Problem 1C - Area of triangle"
(define (area-of-tri b h)
  (* 0.5 b h))

"Problem 1D - Change in Drawer"
(define (cash q d n p)
  (+ (* q 0.25)
     (* d 0.10)
     (* n 0.05)
     (* p 0.01)))

"Problem 2A - Repeated Decimal"
(define (repeat-decimal n)
  (if (= n 1)
      0
      (floor n)))

(repeat-decimal 3)


"Sum f(x) + g(x)"
(define (sum-function f g)
  (lambda (x) (+ (f x) (g x))))