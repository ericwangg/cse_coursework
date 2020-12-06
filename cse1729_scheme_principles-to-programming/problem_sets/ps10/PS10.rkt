"Problem Set 10 - Eric Wang"

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
  (cons-stream a (enumerate-integers-from (+ a 1))))

(define (prime? x)
  (define (is-factor? k x)
    (= (modulo x k) 0))
  (define (has-factor-le? j)
    (cond ((< j 2) #f)
          ((is-factor? j x) #t)
          (else
           (has-factor-le? (- j 1)))))
    (not (has-factor-le? (round (sqrt x)))))

(define (stream-filter f str)
  (cond ((empty-stream? str) '())
        ((f (stream-car str))
         (cons-stream (stream-car str) (stream-filter f (stream-cdr str))))
        (else (stream-filter f (stream-cdr str)))))

(define (stream-map f str)
  (if (empty-stream? str)
      '()
      (cons-stream (f (stream-car str))
                   (stream-map f (stream-cdr str)))))

"1A - primes, Stream primes"
(define (primes)
  (stream-filter
   prime?
   (enumerate-integers-from 2)))

"1B - mersenne-candidates, Mersenne (2^k-1)"
(define (mersenne-candidates)
  (stream-map (lambda (k) (- (expt 2 k) 1)) (primes)))

"1C - mersenne-primes, Mersenne primes"
(define (mersenne-primes)
  (stream-filter prime? (mersenne-candidates)))



"2A - facts, factorial stream"
(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(define facts (stream-map (lambda (x) (factorial x)) (enumerate-integers-from 0)))

"2B - pow-seven, stream of power of 7"
(define pow-seven (stream-map (lambda (x) (expt 7 x)) (enumerate-integers-from 0)))



"3A - e-terms, the value of 'e' expressed by its power series terms"
(define (facts-to-inf)
  (stream-map (lambda (x) (factorial x))
              (enumerate-integers-from 0)))

(define (e-terms)
  (define (helper n)
    (cons-stream (/ 1 (stream-car n)) (helper (stream-cdr n))))
  (helper (facts-to-inf)))

"3B - e-approx, successive approximations of 'e'"
(define (partial-sums str)
  (define (ps-aux str sofar)
    (cond ((empty-stream? str) (cons-stream sofar '()))
          (else (cons-stream sofar (ps-aux (stream-cdr str)
                                           (+ sofar (stream-car str)))))))
  (if (empty-stream? str)
      '()
      (ps-aux (stream-cdr str) (stream-car str))))

(define (e-approx)
  (partial-sums (e-terms)))



"4A - stream-merge, merge 2 streams in increasing order"
(define (stream-merge str1 str2)
  (cond ((empty-stream? str1) str2)
        ((empty-stream? str2) str1)
        ((and (empty-stream? str1) (empty-stream? str2)) str1)
        ((> (stream-car str1) (stream-car str2)) (cons-stream
                                                  (stream-car str2)
                                                  (stream-merge str1 (stream-cdr str2))))
        ((> (stream-car str2) (stream-car str1)) (cons-stream
                                                  (stream-car str1)
                                                  (stream-merge (stream-cdr str1) str2)))
        (else (cons-stream
               (stream-car str1)
               (stream-merge (stream-cdr str1) (stream-cdr str2))))))

"4B - 235-stream, sorted stream of prime factors of 2, 3, 5 only"
(define (scale-stream k str)
  (cond ((empty-stream? str) '())
        (else (cons-stream (* k (stream-car str))
                           (scale-stream k (stream-cdr str))))))
   
(define (235-stream)
  (cons-stream 1 (stream-merge (scale-stream 5 (235-stream))
                               (stream-merge
                                (scale-stream 2 (235-stream))
                                (scale-stream 3 (235-stream))))))

(235-stream)



"5A - merge-weighted, merge w/ consideration of weight factor"
(define (merge-weighted str1 str2 w)
  (cond ((empty-stream? str1) str2)
        ((empty-stream? str2) str1)
        ((equal? (stream-car str1) (stream-car str2))
         (cons-stream (stream-car str1)
                      (merge-weighted (stream-cdr str1) (stream-cdr str2) w)))
        ((< (w (stream-car str1)) (w (stream-cdr str2)))
         (cons-stream (stream-car str1)
                      (merge-weighted (stream-cdr str1) str2 w)))
        (else (cons-stream (stream-car str2)
                           (merge-weighted str1 (stream-cdr str2) w)))))

"5B - weighted-pairs, computes weighting function from 2 stream pairs"
(define (weighted-pairs str1 str2 w)
  (cond ((empty-stream? str1) '())
        ((empty-stream? str2) '())
        ((and (empty-stream? str1) (empty-stream? str2)) '())
        (else
         (cons-stream (cons (stream-car str1)
                            (stream-car str2))
                      (merge-weighted
                       (stream-map (lambda (x) (cons (stream-car str1) x))
                                   (stream-cdr str2))
                       (weighted-pairs (stream-cdr str1) str2 w)
                       w)))))

"(define (weighted-pairs str1 str2 w)
  (if (or (empty-stream? str1) (empty-stream? str2))
      '()
      (cons-stream (cons (car str1) (car str2))
                   (merge-weighted (stream-map (lambda (x) (cons (car str1) x)) (stream-cdr str2))
                                   (weighted-pairs (stream-cdr str1) str2 w)
                                   w))))"
                                              

"(define test (weighted-pairs (enumerate-integers-from 1)
                             (enumerate-integers-from 2)
                             (lambda (x) (+ (car x) (cdr x)))))"

(define (stream-nth n stream)
  (if (= n 1)
      (stream-car stream)
      (stream-nth (- n 1) (stream-cdr stream))))

(define (str-to-list str n)
  (cond ((or (empty-stream? str) (= n 0)) '())
        (else (cons (stream-car str) (str-to-list (stream-cdr str) (- n 1))))))

;(str-to-list test 10)


"5C - weighted-pairs-stream, evaulates to stream of all poisitive integers (i,j)
ordered according to i+j"
(define (plus-wt x) (+ (car x) (cdr x)))
(define pos-ints (stream-cdr (enumerate-integers-from 0)))

; OLD weighted-pairs-stream 
;(define weighted-pairs-stream
;  (weighted-pairs pos-ints pos-ints plus-wt))

(define (weighted-pairs-stream)
  (weighted-pairs pos-ints pos-ints (lambda (x) (+ (car x) (cdr x)))))

"5D - ramanujan, ???"
"(define (find-seq-matches wt str)
  (define (fsm-next str prev)
    (if (= (wt (strea-car str)) (wt prev))
        (cons str
              (list (wt prev) prev (stream-car str)))
        (fsm-next (stream-cdr str) (stream-car str))))
  (let ((found-one (fsm-next (stream-cdr str)
                             (stream-car str))))
    (cons-stream (cdr found-one)
                 (find-seq-matches wt (car found-one)))))

(define cube-wt (lambda (wt) (* wt wt wt)))

(define ram-stream
  (stream-map
   car
   (find-seq-matches
    cube-wt
    (weighted-pairs pos-ints pos-ints cube-wt))))

(define ram-pairs
  (find-seq-matches
   cube-wt
   (weighted-pairs pos-ints pos-ints cube-wt)))"


"6A - Encode, "
(define (encode-ps pair)
  (let ((f (expt 2 (car pair))))
    (cond ((and (= (car pair) 1) (= (cdr pair) 1)) 1)
          ((= (car pair) 1)
           (- (* 2 (cdr pair)) 2))
          (else (+ (- f 1) (if (= (cdr pair) 1)
                               0
                               (/ f 2))
                   (* f (if (>= (cdr pair) 2)
                            (- (cdr pair) 2)
                            0)))))))
                 
"6B - Decode, "
(define (decode-ps n)
  (define (helper c)
    (let ((f (- n (- (expt 2 c) 1) (expt 2 (- c 1)))))
      (cond ((= n 1) (cons 1 1))
            ((< f 0) (cons c 1))
            ((= f 0) (cons c 2))
            ((= (modulo f (expt 2 c)) 0)
             (cons c (/ f (expt 2 c))))
            (else (helper (+ c  1))))))
  (helper 1))
