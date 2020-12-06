"Lab 7 - Eric Wang"

"1A - Explode, Positive Integer to List"
(define (explode x)
  (if (< x 10)
      (list x)
      (append (explode (floor (/ x 10)))
              (list (- x (* 10 (floor (/ x 10))))))))

"1B - Implode, Base 10 Digits to Integer"
(define (implode l)
  (define (add-digits l place)
    (if (null? l)
        0
        (+ (* (car l) (expt 10 place))
           (add-digits (cdr l) (+ place 1)))))
  (add-digits (reverse l) 0))

"1C - Interger Has Property"
(define (sum-list list)
  (if (null? list)
      0
      (+ (car list)
         (sum-list (cdr list)))))

(define (has-property x)
  (let* ((int (explode x))
        (sum-digits (sum-list int))
        (sum (explode sum-digits))
        (sum-rev (implode (reverse sum))))
    (= (* sum-digits sum-rev) x)))

"1D - Find, nth value of sequence"
(define (find sequence test n)
  (define (find-help x found)
    (let ((fx (sequence x)))
      (if (test fx)
          (if (= (+ found 1) n)
              fx
              (find-help (+ x 1) (+ found 1)))
          (find-help (+ x 1) found))))
  (find-help 1 0))

"1E - Find Integers with Fujiwara Property"
(find (lambda (x) x) has-property 1)
(find (lambda (x) x) has-property 2)
(find (lambda (x) x) has-property 3)

"2A Swap First Two Elements in a list"


"2B - Swap First Two, > 2 Elements in List"
"(define (swap-first-two lst)
  (if (null? lst)
      '()
      (if (< (length lst) 2)
           (car lst)
           (cons (car (cdr lst)) (cons (car lst) (cdr (cdr lst)))))))"

(define (swap-first-two lst)
  (cond ((null? lst) '())
        ((< (length lst) 2) (car lst))
        (else (cons (car (cdr lst)) (cons (car lst) (cdr (cdr lst)))))))

"2C - Bubble-Up largest item in list to end of list"
(define (bubble-up lst)
  (if (null? (cdr lst))
      lst
      (if (> (car lst) (car (cdr lst)))
          (cons (car (swap-first-two lst)) (bubble-up (cdr (swap-first-two lst))))
          (cons (car lst) (bubble-up (cdr lst))))))

"(define (bubble-up lst)
  (cond ((null? (cdr lst)) lst)
        ((> (car lst) (car (cdr lst))) (bubble-up (cdr (swap-first-two lst))))
        (else (cons (car lst) (bubble-up (cdr lst))))))"

(bubble-up '(1 7 3 8))

"2D - Bubble-Sort-Aux, uses Bubble-Up for each list element"
(define (bubble-sort-aux lst n)
  (if (= n 0)
      lst
      (bubble-up (bubble-sort-aux lst (- n 1)))))

"2E - Bubble-Sort"
(define (bubble-sort lst)
  (bubble-sort-aux lst (length lst)))