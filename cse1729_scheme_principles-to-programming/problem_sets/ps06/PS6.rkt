"Problem 6 - Eric Wang"

"1A - nNcode, Pairing Function computation"
(define (encode pair)
  (+ (* 0.5 (+ (car pair) (- (cdr pair) 2))
        (+ (car pair) (- (cdr pair) 1)))
     (car pair)))

(encode (cons 1 1))
(encode (cons 1 2))

"1B - Decode, Integer to Pair"
(define (decode z)
  (let* ((w (floor (- (sqrt (* 2 z)) 0.5)))
    (t (floor (/ (+ (* w w) w) 2)))
    (x (- z t))
    (y (+ (- w x) 2)))
    (cons x y)))

(decode 1)
(decode 2)



"2 - Collapse, reduce lists to single on 'same level'"
(define (collapse l)
  (cond ((null? l) '())
        ((pair? (car l))
         (append (collapse (car l))
                 (collapse (cdr l))))
        (else (cons (car l) (collapse (cdr l))))))


"3 - Deep-reverse, list of elements reversed & sublists reversed"
(define (deep-reverse l)
  (cond ((or (null? l) (not (pair? l))) l)
        (else (append (deep-reverse (cdr l))
                      (list (deep-reverse (car l)))))))

(deep-reverse (list 1 2 3 4))
(deep-reverse (list (list 1 2) (list 4 3)))



"4A Explode, Integer to list"
(define (explode x)
  (if (< x 10)
      (list x)
      (append (explode (floor (/ x 10)))
              (list (- x (* 10 (floor (/ x 10))))))))



"4B - Implode, List to integer"
(define (implode l)
  (define (add-digits l place)
    (if (null? l)
        0
        (+ (* (car l) (expt 10 place))
           (add-digits (cdr l) (+ place 1)))))
  (add-digits (reverse l) 0))



"4C, D, E - Finding Two Sided truncatable primes"
(define (prime? n)
  (define (divisor a) (= (modulo n a) 0))
  (define ( smooth k)
    (and (>= k 2)
         (or (divisor k)
             (smooth (- k 1)))))
  (and (> n 1)
       (not (smooth (floor (sqrt n))))))

"Find - from Lab 7"
(define (find sequence test n)
  (define (find-help x found)
    (let ((fx (sequence x)))
      (if (test fx)
          (if (= (+ found 1) n)
              fx
              (find-help (+ x 1) (+ found 1)))
          (find-help (+ x 1) found))))
  (find-help 1 0))

"4Ci - Left Truncatable Primes"
(define (left-truncatable-prime? p)
  (cond ((< p 10) (prime? p))
        ((zero? (car (cdr (explode p)))) #f)
        ((not (prime? p)) #f)
        (else (left-truncatable-prime? (implode (cdr (explode p)))))))
 
(left-truncatable-prime? 9137)
(left-truncatable-prime? 137)

"4Cii - Nth Left truncatable Prime"
(define (nth-left-trunc-prime n)
  (find (lambda (x) x) left-truncatable-prime? n))

"4Di - Right Truncatable Primes"
(define (right-truncatable-prime? p)
  (cond ((< p 10) (prime? p))
        ((not (prime? p)) #f)
        (else (right-truncatable-prime? (floor (/ p 10))))))

(right-truncatable-prime? 7393)

"4Dii - nth Right Truncatable Prime"
(define (nth-right-trunc-prime n)
  (find (lambda (x) x) right-truncatable-prime? n))

"4Ei - Two-Sided Primes"                                       
(define (two-sided-prime? p)
  (and (left-truncatable-prime? p)(right-truncatable-prime? p)))

"4Eii - Nth Two Sided Prime"
(define (nth-two-sided-prime n)
  (find (lambda (x) x) two-sided-prime? n))



"5A - Split list, Odd & Even method"
"(define (odd l)
  (if (null? l)
      '()
      (if (null? (cdr l))
          (list (car l))
          (cons (car l) (odd (cddr l))))))"

(define (odd l)
  (cond ((null? l) '())
        ((null? (cdr l)) (list (car l)))
        (else (cons (car l) (odd (cddr l))))))

"(define (even l)
  (if (null? l)
      '()
      (if (null? (cdr l))
          '()
          (cons (cadr l) (even (cddr l))))))"

(define (even l)
  (cond ((null? l) '())
        ((null? (cdr l)) '())
        (else (cons (cadr l) (even (cddr l))))))

(define (split l)
  (cons (odd l) (even l)))

(split '(1 2 3 4))
(split '(1 3 4 6 5 8 2 3 9 4))

"5B - Merge 2 lists back in order"
(define (merge l1 l2)
  (cond ((null? l1) l2)
        ((null? l2) l1)
        ((< (car l1) (car l2)) (cons (car l1) (merge (cdr l1) l2)))
        (else (cons (car l2) (merge (cdr l2) l1)))))

(merge (list) (list 2))
(merge (list 1 2 3 4) (list 5 6 7 8))

"5C - Mergesort"
(define (mergesort l)
  (cond ((null? l) l)
        ((null? (cdr l)) l)
        (else (merge (mergesort (car (split l))) (mergesort (cdr (split l)))))))

(mergesort (list 1 2 3))
(mergesort (list 9 2 3 4 10))