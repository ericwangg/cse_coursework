"Problem Set 2 - Eric Wang"

"Problem 1A"
(define (number-sum n)
  (if (= n 0)
      0
      (+ n (number-sum (- n 1)))))
  
(define (odd-sum n)
  (if (= n 0)
      0
      (+ (- (* 2 n) 1) (odd-sum (- n 1)))))


"Problem 1B"
(odd-sum 1)
(odd-sum 2)
(odd-sum 3)
(odd-sum 4)
(odd-sum 5)
(odd-sum 6)
(odd-sum 7)
"It makes sense since adding the odd numbers from the given input, ex.): 5, (9+7+5+3+1) = 25, which gives the square of 5"


"Problem 1C"
(define (sum-from-to a b)
 (if (> a b)
     0
     (+ b (sum-from-to a (- b 1)))))


"Problem 2"
(define (k-product k)
  (if (= k 1)
     1
     (* (- 1 (/ 1 (expt k 2)))
        (k-product (- k 1)))))

  

"Problem 3A"
(define (babylonian x k)
  (if (= k 0)
      (/ x 2)
      (* 0.5 (+ (babylonian x (- k 1)) (/ x (babylonian x (- k 1)))))))


"Problem 3B"
(define (square x)
  (* x x))

(define (first-value-k-or-higher x tol k)
  (if (< (- (square (babylonian x k)) x) tol)
      k
      (first-value-k-or-higher x tol (+ k 1))))

(define (terms-needed x tol)
  (first-value-k-or-higher x tol 0))
                    
"Problem 4"
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(define (new-cos x n)
  (if (= n 0)
      1
      (+ (* (/ (expt x (* 2 n)) (factorial (* 2 n))) (expt -1 n)) (new-cos x (- n 1)))))