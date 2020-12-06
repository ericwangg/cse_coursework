"Lab 13 Final Exam Practice - Eric Wang"

"Expression Evaluations"
(+ 4 8 15 16 23 42)

(* 653854321 241304201)

(/ (+ 5 4 (- 2 (- 3 (+ 6 0.8))))
                  (* 3 (- 6 2) (- 7 2)))


"1 - Simple Function"
"1A - Absolute value "
(define (abs-val x)
  (sqrt (* x x)))

;solution code
(define (absolute x)
  (if (< x 0)
      (- x )
      x))

;Absolute value of 4 * -8
(abs-val 4)
(abs-val -8)

"1B - Fahrenheit to Celcius & Back"
(define (C-to-F C)
  (+ (* (/ 9 5) C) 32))

;10 degrees, 30 degrees Celcius to Fahrenheit
(C-to-F 10)
(C-to-F 30)

(define (F-to-C F)
  (* (/ 5 9) (- F 32)))

;32 deg, 212 deg Fahrenheit to Celcius
(F-to-C 32)
(F-to-C 212)

"1C - discount, product discounted price"
(define (discount price discount)
  (* price (- 1 discount)))

;$10 item, 10% off, 50% off
(discount 10.0 0.1)
(discount 10.0 0.5)

"1D - Tip at restaurant"
(define (tip bill)
  (ceiling (* bill 0.20)))

;$93.57 bill, find tip
(tip 93.57)

"1E - Paint & Stain Job"
(define (paint x)
  (/ x 400))

(define (stain x)
  (/ x 500))

(define (floor-job l w job)
  (let ((sq-ft (* l w)))
    (if (equal? job paint)
      (paint sq-ft)
      (stain sq-ft))))

;floor 30 ft. long 50 ft. wide (1500 sq. ft), painting it, then staining it
(floor-job 30 50 paint)
(floor-job 30 50 stain)

"1F - Painting Hemisphere ceilings"
(define pi 3.1415926535)

(define (hemi-ceil r)
  (paint (* 2 pi r r)))

;paint hemisphere ceiling w/ 5 ft. radius
(hemi-ceil 5)



"2 - Recusion"
;Solution code wrong?
(define (towers-of-hanoi n source temp dest)
  (cond ((not (= n 0))
         (begin (towers-of-hanoi (- n 1) source temp dest)
                (display "Move disk ")
                (display n)
                (display " to peg ")
                (display dest)
                (display #\newline)
                (towers-of-hanoi (- n 1) temp dest source)))))

"Towers of Hanoi - 4 Ring"
(towers-of-hanoi 4 'A 'B 'C)
"Towers of Hanoi - 3 Ring"
(towers-of-hanoi 3 'A 'B 'C)

;Own Code
"(define (towers-of-hanoi n source temp dest)
  (cond ((even? n)
         (begin (towers-of-hanoi (- n 1)
        ((odd? n)
         (begin"


"Learning 'begin', 'set!', 'force'"
(begin
  (define x 10)
  x)

"3A - Count Non-negative numbers, recusion, iteration"
;Recursion
(define (count-nneg lst)
  (cond ((null? lst) 0)
        ((>= (car lst) 0)
         (+ 1 (count-nneg (cdr lst))))
        (else (count-nneg (cdr lst)))))

(count-nneg '(1 3 -4 -5 6 0 2 -3))
(count-nneg (list))
(count-nneg '(3 4 -1 -2 -3 0))

;Iteration
(define (count-nneg-it lst)
  (define (count-help acc lst)
    (cond ((null? lst) 0)
          ((>= (car lst) 0)
           (count-help (+ acc 1) (cdr lst)))
          (else (count-help acc (cdr lst)))))
  (count-help 0 lst))

(count-nneg '(1 3 -4 -5 6 0 2 -3))
(count-nneg (list))
(count-nneg '(3 4 -1 -2 -3 0))

"3B - Greatest Common Denominator"
(define (GrCD a b)
  (cond ((= a 0) b)
        ((= b 0) a)
        ((> a b) (GCD (- a b) b))
        (else (GCD a (- b a)))))

(GrCD 252 105)
(GrCD 1467 963)

"3C - Fast GCD, Lame's improvement"
(define (fast-gcd a b)
  (cond ((= a 0) b)
        ((= b 0) a)
        ((> a b) (fast-gcd b (modulo a b)))
        (else (fast-gcd (module a b) a))))

(fast-gcd 252 105)


"4A - SICP 1.43, "
(define (square x)
  (* x x))

(define (compose f g)
  (lambda (x) (f (g x))))

(define (repeated f n)
  (if (< n 1)
      (lambda (x) x)
      (compose f (repeated f (- n 1)))))

;evaluates to "625"  
((repeated square 2) 5)

"4B - SICP 1.44, smoothing function"
(define dx 0.000001)

(define (smooth x)
  (/ (+ (f (+  x dx))
        (f x)
        (f (- x dx)))
     3))

;with lambda
(define (smooth2 f dx)
  (lambda (x)
    (/ (+ (f (+  x dx))
          (f x)
          (f (- x dx)))
       3)))

;"smoother" & n-fold-smoother using repeated
(define (n-fold-smooth f n)
  (repeated smooth n) f)



"List Processing"

(car '(1 2))
(cdr '(1 2))
(cadr '(1 2))

"1A - Intercept of 2 points (lists)"
(define (intercept a b)
  (if (or (null? a) (null? b))
      (display "undefined\n")
      (let* ((m (/ (- (cadr b) (cadr a))
                   (- (car b) (car a))))
             (b (- (cadr a) (* m (car a)))))
        (cons m b))))

(intercept '(1 2) '(3 6))
(intercept '() '(3 6))

"1B - Unusual Canceling"
(define (unusual-cancel fraction)
  (let ((num-x (floor (/ (car fraction) 10)))
        (num-y (modulo (car fraction) 10))
        (denom-x (floor (/ (cadr fraction) 10)))
        (denom-y (modulo (cadr fraction) 10)))
    (if (= num-x denom-y)
        (= (/ (car fraction) (cadr fraction))
           (/ num-y denom-x))
        #f)))

(unusual-cancel '(64 16))
(unusual-cancel '(24 12))

;solution code
(define (unusual-canceling num denom)
  (let ((x-num (floor (/ num 10)))
        (y-num (modulo num 10))
        (x-denom (floor (/ denom 10)))
        (y-denom (modulo denom 10)))
    (if (= x-num y-denom)
        (= (/ num denom) (/ y-num x-denom))
        #f)))

(unusual-canceling 64 16)
(unusual-canceling 24 12)

"Definining Test Lists, and List Convention Tests"
(define test-lst1 '(1 2 3 4 5 6 7 8 9))
(define test-lst2 '(0 2 -3 5 0 2 -4 -9 3))

(car test-lst1)
(cadr test-lst1)
(caddr test-lst1)
(cddr test-lst1)
(cdr test-lst1)

"2A - Largest Distance of 2 adjacent elements"
(define (list-max-dif lst)
  (define (list-max-dif-helper lst max)
    (cond ((null? (cdr lst)) max)
          ((> (abs (- (car lst) (cadr lst))) max)
           (list-max-dif-helper (cdr lst) (abs (- (car lst) (cadr lst)))))
          (else (list-max-dif-helper (cdr lst) max))))
  (list-max-dif-helper lst 0))

(list-max-dif test-lst1)
(list-max-dif test-lst2)

;solution code
(define (max-pair-dist lst)
  (define (max-pair-dist-aux lst max)
    (if (null? (cdr lst))
        max
        (if (> (abs (- (car lst) (cadr lst))) max)
            (max-pair-dist-aux (cdr lst) (abs (- (car lst) (cadr lst))))
            (max-pair-dist-aux (cdr lst) max))))
  (max-pair-dist-aux lst 0))

(max-pair-dist test-lst1)
(max-pair-dist test-lst2)
        
        
"2B - List transform, Bi = A(i+1) - Ai"
;one term difference between "i+1" and "i"
(define (list-dif-transform lst)
  (if (null? (cdr lst))
      '()
      (cons (- (cadr lst) (car lst))
            (list-dif-transform (cdr lst)))))

(list-dif-transform test-lst1)
(list-dif-transform test-lst2)

"2C - Range in List"
(define (list-range lst)
  (define (list-range-aux lst min max)
    (if (null? lst)
        (cons min max)
        (let ((new-min (if (< min (car lst))
                           min
                           (car lst)))
              (new-max (if (> max (car lst))
                           max
                           (car lst))))
          (list-range-aux (cdr lst) new-min new-max))))
  (list-range-aux (cdr lst) (car lst) (car lst)))

(list-range test-lst1)
(list-range test-lst2)

"2F - list-insert"
(define (list-insert lst item pos)
  (if (= pos 1)
      (cons item lst)
      (cons (car lst) (list-insert (cdr lst) item (- pos 1)))))

(list-insert test-lst1 23 4)
(list-insert test-lst2 -69 8)


  
;tree-conventions
(define (make-tree v left-tree right-tree)
  (list v left-tree right-tree))
(define (value T) (car T))
(define (left T) (cadr T))
(define (right T) (caddr T))
(define (insert x T)
  (cond ((null? T) (make-tree x '() '()))
        ((eq? x (value T)) T)
        ((< x (value T)) (make-tree (value T)
                                    (insert x (left T))
                                    (right T)))
        ((> x (value T)) (make-tree (value T)
                                    (left T)
                                    (insert x (right T))))))

;test-trees
;(define test-tree1 (maketree 3
         
;heap-conventions
"3A - count-one-child, bst nodes w/ 1 child"
(define (count-one-child tree)
  (let ((left-child (left tree))
        (right-child (right tree)))
    (cond ((and (null? left-child)
                (null? right-child))
           0)
          ((and (not (null? left-child))
                (not (null? right-child)))
           (+ (count-one-child left-child)
              (count-one-child right-child)))
          ((null? left-child)
           (+ 1 (count-one-child right-child)))
          (else (+ 1 (count-one-child left-child))))))

;stream-conventions

"5A Objects - Lab 8 Bank Addition"
(define (new-account initial-balance password)
  (let ((balance initial-balance)
        (interestrate 0.01)
        (pw password))
    (define (deposit f password)
      (cond ((equal? pw password)
      (begin
        (set! balance
              (+ balance f))
        balance))))
    (define (withdraw f password)
      (cond ((equal? pw password)
      (begin
        (set! balance
              (- balance f))
        balance))))
    (define (bal-inq) balance)
    (define (accrue) (being (set! balance
                                  (+ balance
                                     (* balance
                                        1
                                        interestrate)))
                            balance))
    (define (setrate r) (set! interestrate r))
    (lambda (method)
      (cond ((eq? method 'deposit) deposit)
            ((eq? method 'withdraw) withdraw)
            ((eq? method 'balance-inquire) bal-inq)
            ((eq? method 'accrue) accrue)
            ((eq? method 'setrate) setrate)))))
         
"5B - Change Password"
(define (new-account initial-balance password)
  (let ((balance initial-balance)
        (interestrate 0.01)
        (pw password))
    (define (deposit f password)
      (cond ((equal? pw password)
      (begin
        (set! balance
              (+ balance f))
        balance))))
    (define (withdraw f password)
      (cond ((equal? pw password)
      (begin
        (set! balance
              (- balance f))
        balance))))
    (define (bal-inq) balance)
    (define (accrue) (being (set! balance
                                  (+ balance
                                     (* balance
                                        1
                                        interestrate)))
                            balance))
    (define (setrate r) (set! interestrate r))
    (define (change-password old new)
      (cond ((equal? old pw) (set! pw new))))
    (lambda (method)
      (cond ((eq? method 'deposit) deposit)
            ((eq? method 'withdraw) withdraw)
            ((eq? method 'balance-inquire) bal-inq)
            ((eq? method 'accrue) accrue)
            ((eq? method 'setrate) setrate)
            ((eq? method 'change-pw) change-password)))))

"5C -"
