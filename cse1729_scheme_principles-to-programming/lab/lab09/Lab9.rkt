"Lab 9 - Eric Wang"
(define (make-heap v H1 H2)
  (list v H1 H2))

(define (h-min H) (car H))

(define (left H) (cadr H))

(define (right H) (caddr H))

"1A heap-insert, adds element to heap w/ 1st order relation"
"(define (heap-insert f x H)
  (cond ((null? H) (make-heap x '() '()))
        ((> x (h-min H)) (make-heap x (right H) (heap-insert f (h-min H) (left H))))
        ((< x (h-min H)) (make-heap (h-min H) (right H) (heap-insert f x (left H))))))"

(define (heap-insert f x H)
  (if (null? H)
      (make-heap x '() '())
      (if (f x (h-min H))
          (make-heap x (right H) (heap-insert f (h-min  H) (left H)))
          (make-heap (h-min H) (right H) (heap-insert f x (left H))))))

;min-heap
(heap-insert < 100 (heap-insert < 10 (list)))
;(10 () (100 () ()))

;max-heap
(heap-insert > 100 (heap-insert > 10 (list)))
;(100 () (10 () ()))

"1B - heap-insert-list, inserts all elements in list into heap w/ 1st order relation"
(define (heap-insert-list f elements H)
  (if (null? elements)
      H
      (heap-insert-list f (cdr elements) (heap-insert f (car elements) H))))

"1C - combine, combines 2 heaps"
(define (collapse l)
  (cond ((null? l) '())
        ((pair? (car l))
         (append (collapse (car l))
                 (collapse (cdr l))))
        (else (cons (car l) (collapse (cdr l))))))

(define (combine f Ha Hb)
  (cond ((null? Ha) Hb)
        ((null? Hb) Ha)
        ((f (h-min Ha) (h-min Hb))
         (make-heap (h-min Ha)
                      Hb
                      (combine f (left Ha) (right Ha))))
        (else (make-heap (h-min Hb)
                           Ha
                           (combine f (left Hb) (right Hb))))))

(define Ha (heap-insert-list > (list 9 5 7 3) (list)))
(define Hb (heap-insert-list > (list 2 8 4 6) (list)))
(combine > Ha Hb)
;(9 (7 () (5 () (3 () ()))) (8 (4 () ()) (6 () (2 () ()))))

"1D - empty?, if Heap is empty"
(define (empty? H)
  (if (null? H)
      #t
      #f))

"1E - heap-remove, removes root, reshuffles heap using 1st order relation"
(define (heap-remove f H)
  (combine f (left H) (right H)))

(heap-remove > (combine > Ha Hb))
;(8 (6 (2 () ()) (4 ())) (7 () (5 () (3 () ()))))