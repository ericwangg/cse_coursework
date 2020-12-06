"Lab2 - 2018/09/11"

"Problem 1 - Combinations"
(define (factorial x)
  (if (= x 0)
      1
      (* x (factorial (- x 1)))))

(define (n-choose-k n k)
  (if (or (< n k) (< k 0))
      0
      (/ (factorial n)
         (* (factorial (- n k))
            (factorial k)))))

"Problem 2 - Exponentiation"
(define (pow b e)
  (expt b e))

"Problem 3 - Recusive"
(define (zeno n)
  (if (= n 1)
      (/ 1 2) 
      (+ (/ 1 (pow 2 n)) (zeno (- n 1)))))

"Problem 4 - Number of Digits"
(define (num-digits n)
  (if (< n 10)
      1
      (+ 1 (num-digits (/ n 10)))))
  
"Problem 5 - Yung Jean"
"5a Jeanie's Number of Ancestors"
(define (a n)
  (if (= 1 n)
      2
      (* 2 (a(- n 1)))))

"5B Jeanie's Total Ancestors"
(define (num-ancestors n)
  (if (= 1 n)
      2
      (+ (a n) (num-ancestors (- n 1)))))