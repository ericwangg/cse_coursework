"Lab 10 Prelim 2 - Eric Wang"

"1 - Same length lists"
"(define (same-length-list lst1 lst2)
  (if ("

"2 - Isomorphic compound intlists"
(define (isomorphic? l1 l2)
  (cond ((and (integer? l1) (integer? l2) #t))
        ((and (null? l1) (null? l2)) #t)
        ((or (null? l1) (null? l2)) #f)
        ((or (not (pair? l1)) (not (pair? l2))) #f)
        ((and (isomorphic? (car l1) (car l2))
              (isomorphic? (cdr l1) (cdr l2))) #t)
        (else #f)))

;isomorphic lists: #t
(isomorphic? (list 1 2) (list 3 4))

;two non-isomorphic lists: #f
(isomorphic? (list 1 (list 2)) (list 3 4))

;an interger and a list: #f
(isomorphic? 1 (list 3 4))

;two empty litss: #t
(isomorphic? '() '())

"3 - Average of all list values"
(define (lst-avg lst)
  (if (null? lst)
      0
      ((car lst))))

"4 - Filter"
(define (filter f L)
  (cond ((null? L) '())
        ((f (car L)) (cons (car L) (filter f (cdr L))))
        (else (filter f (cdr L)))))

;iterative "filter"
(define (filter-acc f L)
  (define (helper acc L)
    (cond ((null? L) '())
          ((f ( car L)) (helper (cons (car L) acc) (cdr L)))
          (else (helper acc (cdr L)))))
  (helper '() L))

;iterative, let helper "named helper" method
(define (filter-acc2 f L)
  (let helper ((acc '()) (L L))
    (cond ((null? L) '())
          ((f ( car L)) (helper (cons (car L) acc) (cdr L)))
          (else (helper acc (cdr L))))))

(filter-acc2 (lambda (x) (> x 0)) '(1 -1 2 -2))
(filter-acc2 (lambda (x) (< x 0)) '(1 -1 2 -2))
(filter-acc2 (lambda (x) (> x 0)) '())



"5 - New-append, append using only cons, car, cdr"
(define (new-append l1 l2)
  (cond ((null? l1) l2)
        ((null? l2) l1)
        (else (cons (car l1) (new-append (cdr l1) l2)))))

; empty l1, list l2
(new-append '() '(1 2 3))

; 2 empty lists
(new-append '() '())

; 2 lists
(new-append '(1 2) '(3 4))

"6 - Remove-zero, removes zeroes from list"
(define (remove-zeros L)
  (define (is-not-zero? x) (not (= x 0)))
  (filter is-not-zero? L))

; Remove-zero, use "filter', lambda for "not-zero"
(define (remove-zeros-la L)
  (lambda (x) (not (= x 0)) L))

"8 - Intersection"
(define (intersection l1 l2)
  (define (is-member? x l)
    (cond ((null? l) #f)
          ((= (car l) x) #t)
    (else (is-member? x (cdr l))))
  (cond ((or (null? l1) (null? l2)) '())
        ((is-member? (car l1) l2) (cons (car l1) (intersection (cdr l1) l2)))
        (else (intersection (cdr l1) l2)))))

; should be (2 4)
(intersection (list 1 2 3 4) (list (2 4 6 8)))

; intersection with empty list: '()
(intersection '() (list 2 4 6 8))

(intersection (list 1 2 3 4) (list 2 4 6 8 0 3))


"9 - replace, finds a value in list and replaces it"
(define (replace find rplc lst)
  (cond ((null? lst) '())
        ((= (car lst) find) (cons rplc (cdr lst)))
        (else (cons (car lst) (replace find rplc lst (cdr lst))))))

(replace 0 1 '(3 4 1 0 5))
(replace 0 1 '(3 4 1 0 5))
(replace 0 1 '(3 4 1 0 5))

"10 - replace-all, replace all values indicated in the list"
(define (replace-all find rplc lst)
  (cond ((null? lst) '())
        ((= (car lst) find) (cons rplc (replace find rplc (cdr lst))))
        (else (cons (car lst) (replace find rplc lst (cdr lst))))))

(replace-all 0 1 '(3 1 4 1 0 1 5))