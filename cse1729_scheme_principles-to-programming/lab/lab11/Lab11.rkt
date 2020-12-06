"Lab 11 - Eric Wang"

"1A - New Factorial"
(define (fact n)
  (let ((product 1)
        (count 0))
    (define (helper)
      (cond ((= count n) 'done)
            (else (set! count (+ count 1))
                  (set! product (* product count))
                  (helper))))
    (helper)
    product))

(fact 5)

"1B - Hailstone Sequence"
(define (hailstone n)
  (let ((lst '() ))
    (define (helper)
      (set! lst (cons n lst))
      (if (> n 1)
          (begin
            (if (even? n)
                (set! n (/ n 2))
                (set! n (+ (* 3 n) 1)))
            (helper))
          '() ))
    (helper)
    (reverse lst)))

(hailstone 1)
(hailstone 3)
(hailstone 9)


"      (hailstone-sequence 
       (cond ((= n 1) 1)
             ((even? n) (/ (hailstone-sequence n) 2))
             (else (+ (* 3 (hailstone-sequence n)) 1)))))
"

"2 - Bank with 'withdraw', 'accrue', and 'setrate'"
(define (new-account initial-balance)
  (let ((balance initial-balance)
        (rate 0.01))
    (define (deposit f)
      (set! balance (+ balance f))
      balance)
    (define (withdraw f)
      (cond ((> f balance) "Insufficient Funds" (display balance) (display (- f balance)))
            (else
             (set! balance (- balance f))
             balance)))
    (define (bal-inq) balance)
    (define (accrue) (set! balance (* balance (+ 1 rate))))
    (define (setrate r) (set! rate r))
    (lambda (method)
      (cond ((eq? method 'deposit) deposit)
            ((eq? method 'withdraw) withdraw)
            ((eq? method 'balance-inquire) bal-inq)
            ((eq? method 'accrue) accrue)
            ((eq? method 'setrate) setrate)))))

"3 - 2 Indepedently Modifiable Bank"
(define Herbst (new-account 10000000))

(define EWang (new-account 5))

((Herbst 'withdraw) 500)
((Herbst 'deposit) 10000)
((Herbst 'setrate) 0.05)
((Herbst 'accrue))
((Herbst 'balance-inquire))

((EWang 'deposit) 2)
((EWang 'setrate) 0.025)
((EWang 'accrue))
((EWang 'withdraw) 3)
((Ewang 'balance-inquire))



"4 - Stacks as Obects"
(define (make-stack)
  (let ((stack '() ))
    (define (is-empty?)
      (null? stack))
    (define (push x)
      (set! stack (cons x stack)))
    (define (top)
      (car stack))
    (define (pop)
      (let ((value (car stack)))
        (begin (set! stack (cdr stack))
               value)))
    (lambda (meth-name) 
      (cond ((eq? meth-name 'is-empty) is-empty?)
            ((eq? meth-name 'push) push)
            ((eq? meth-name 'top) top)
            ((eq? meth-name 'pop) pop)))))


"5A - nconc!, Destructive Append"
(define (nconc! x y)
  (define (help x1)
    (cond ((null? x1) y)
          ((null? (cdr x1)) (set-cdr! x1 y) x)
          (else (help (cdr x1)))))
    (help x))

"5B - Shows Append different from nconc!"
;(define a '(1 2 3))
;(define b '(4 5 6))
;(append a b)
;(append nconc! a b)