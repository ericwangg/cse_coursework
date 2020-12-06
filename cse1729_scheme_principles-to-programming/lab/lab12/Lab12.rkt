"Lab 12 - Eric Wang"
;; stream primitives
(define-syntax cons-stream
  (syntax-rules ()
    ((cons-stream head tail)
     (cons head (delay tail)))))

(define (stream-car x)
  (car x))

(define (stream-cdr x)
  (force (cdr x)))

(define empty-stream? null?)

;; utiity for tracing function calls 
(define (tracer name . values)
  ;  usage: if at start of function defined (foo a b c)
  ;  put in (tracer 'foo a b c)
  ;  interesting to put into something that is delayed
  (define (display-spaced item)
    (display item)
    (display " "))
  (display-spaced name)
  (display-spaced "with parameter(s):")
  (for-each display-spaced values)
  (newline))
;;;;;;;;;;;;;;;;

(define (enumerate-integers-from a)
  (cons-stream
   a
   (enumerate-integers-from (+ a 1))))

(define test2 (enumerate-integers-from 1))
(stream-car test2)
(stream-car (stream-cdr test2))
test2
(stream-cdr test2)

(define (stream-length str)
  (if (null? str)
      0
      (+ 1 (stream-length (stream-cdr str)))))
            
"1 - str-to-list, easier debugging"
(define (str-to-list str k)
  (cond ((= k 0) '())
        ((empty-stream? str) '()) 
        (else (cons (stream-car str) (str-to-list (stream-cdr str) (- k 1)) ))))
  

"2A - stream-filter, returns stream where all 'p' elements are true"
(define (stream-filter p str)
  (cond ((empty-stream? str) '() )
        ((p (stream-car str)) (cons-stream (stream-car str) (stream-filter p (stream-cdr str))))
        (else (stream-filter p (stream-cdr str)))))
      
"2B - stream-map, returns stream by applying function 'f'"
(define (stream-map f str)
  (if (empty-stream? str)
      str
      (cons-stream (f (stream-car str)) (stream-map f (stream-cdr str)))))

"2C - stream-nth, returns nth element of stream, index of 1 corresponds to 1st element"
(define (stream-nth index str)
  (if (= index 1)
      (stream-car str)
      (stream-nth (- index 1) (stream-cdr str))))

"3A - scale-stream, multiply each element of str"
(define (scale-stream k str)
  (cond ((empty-stream? str) '())
        (else (cons-stream (* k (stream-car str))
                           (scale-stream k (stream-cdr str))))))

"3B - add-streams, adding elements of 2 streams pairwise"
(define (add-streams str1 str2)
  (cond ((empty-stream? str1) str2)
        ((empty-stream? str2) str1)
        (else (cons-stream (+ (stream-car str1) (stream-car str2))
                           (add-streams (stream-cdr str1) (stream-cdr str2))))))

"3C - mult-streams, multiply elements of 2 streams pairwise"
(define (mult-streams str1 str2)
  (cond ((empty-stream? str1) (cons-stream (* 0 (stream-car str2))
                                           (mult-streams str1 (stream-cdr str2))))
        ((empty-stream? str2) (cons-stream (* 0 (stream-car str1))
                                           (mult-streams (stream-cdr str1) str2)))
        (else (cons-stream (* (stream-car str1) (stream-car str2))
                           (mult-streams (stream-cdr str1) (stream-cdr str2))))))

"3D - append-streams, return stream with elements of str1 followed by str2"
(define (append-streams str1 str2)
  (cond ((empty-stream? str1) str2)
        ((empty-stream? str2) str1)
        (else (cons-stream (stream-car str2) (append-streams (stream-cdr str1) str2)))))

(append-streams (enumerate-integers-from 0) '())
(append-streams (enumerate-integers-from 0) (enumerate-integers-from 0))

"4A - odd-factors-of, all odd non-negative numbers evenly divisble by k"
(define (odd-factors-of k)
  (define (helper term k)
    (if (even? k)
        '()
        (if (and (odd? term) (= 0 (modulo term k)))
            (cons-stream term (helper (+ 1 term) k))
            (helper (+ 1 term) k))))
  (helper 0 k))

(odd-factors-of 7)
(odd-factors-of 5)
(odd-factors-of 4)

"4B - partial-sums, partial sums of str"
(define (partial-sums str)
  (define (helper-2 str2 sum)
    (if (empty-stream? (stream-cdr str2))
        (cons-stream sum (stream-cdr str2))
        (cons-stream sum (helper-2 (stream-cdr str2) (+ sum (stream-car (stream-cdr str2)))))))
  (if (empty-stream? str)
      str
      (helper-2 str (stream-car str))))

"4C - square-streams, squares of non-negative integers in ascending order"
(define (square-stream)
  (mult-streams (enumerate-integers-from 0) (enumerate-integers-from 0)))

(square-stream)




