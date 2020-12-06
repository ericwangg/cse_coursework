"Problem Set 8 - Eric Wang"
(define (make-tree value left right) (list value left right))

(define (value tree) (car tree))

(define (left tree) (cadr tree))

(define (right tree) (caddr tree))

(define empty-tree? null?)

(define (leaf? T)
  (and (empty-tree? (left T)) (empty-tree? (right T))))

(define (two-subtrees? T)
  (and (not (empty-tree? (left T))) (not (empty-tree? (right T)))))

(define (one-subtree? T)
  (or (not (empty-tree? (left T))) (not (empty-tree? (right T)))))

(define example
  (make-tree
   '+
   (make-tree
    '* (make-tree 2 '() '()) (make-tree 3 '() '()))
   (make-tree
    '*
    (make-tree
     '+
     (make-tree 4 '() '())
     (make-tree '- '() (make-tree 5 '() '())))
    (make-tree '1/ '() (make-tree 6 '() '())))))

(define (bst-smallest bs-tree)
  (if (empty-tree? bs-tree)
      'undefined
      (if (leaf? bs-tree)
          (value bs-tree)
          (bst-smallest (left bs-tree)))))

(define (bst-largest bs-tree)
  (if (empty-tree? bs-tree)
      'undefined
      (if (leaf? bs-tree)
          (value bs-tree)
          (bst-largest (right bs-tree)))))

"1 - BST Check, returns true for search tree property"
(define (bst? T)
  (cond ((empty-tree? T) #t)
        ((leaf? T) #t)
        ((and (not (empty-tree? (right T)))
              (< (bst-smallest (right T)) (value T)))
         #f)
        ((and (not (empty-tree? (left T)))
              (> (bst-largest (left T)) (value T)))
         #f)
        ((and (bst? (left T)) (bst (right T)))
         #t)
        (else #t)))


"2A - Rotate Left, left rotation on BST"
(define (rotate-left T)
  (if (empty-tree? T)
      '()
      (make-tree (value (right T))
                 (make-tree (value T) (left T) (left (right T)))
                 (right (right T)))))

"2B - Rotate Right, right rotation on BST"
(define (rotate-right T)
  (if (empty-tree? T)
      '()
      (make-tree (value (left T))
                 (left (left T))
                 (make-tree (value T) (right (left T)) (right T)))))

"2C - Tree-repair"
(define (depth? tree)
  (if (null? tree)
      0
      (+ 1 (max (depth? (left tree))
                (depth? (right tree))))))

(define (tree-repair T)
  (cond ((> (depth? (left T)) (+ 1 (depth? (right T)))) (rotate-right T))
        ((> (depth? (right T)) (+ 1 (depth? (left T)))) (rotate-left T))
        (else T)))

"3 - Heapsort, returns list of same #s in sorted order"
(define (create-heap v H1 H2)
  (list v H1 H2))

(define (insert x H)
  (if (null? H)
      (create-heap x '() '())
      (let ((child-value (max x (value H)))
            (root-value (min x (value H))))
        (create-heap root-value
                     (right H)
                     (insert child-value (left H))))))

(define (combine-heaps H1 H2)
  (cond ((null? H1) H2)
        ((null? H2) H1)
        ((< (value H1) (value H2))
         (create-heap (value H1)
                      H2
                      (combine-heaps (left H1) (right H2))))
        (else (create-heap (value H2)
                           H1
                           (combine-heaps (left H2) (right H1))))))

(define (remove-minimum H)
  (combine-heaps (left H) (right H)))

(define (hsort elements)
  (define (hsort-into-heap elements)
    (if (null? (cdr elements))
        (create-heap (car elements) '() '())
        (insert (car elements) (hsort-into-heap (cdr elements)))))
  (define (hsort-backto-list heap)
    (if (null? heap)
        '()
        (cons (value heap) (hsort-backto-list (remove-minimum heap)))))
  (if (null? elements)
      elements
      (hsort-backto-list (hsort-into-heap elements))))

; hsort (list 1 9 0 8 3 2 7 4 6 2), returns (0 1 2 3 5 8 9)
(hsort (list 1 9 0 8 3 2 7 5 6 2))

"4A - "

; heap functions from lab9
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

(define (heap-remove f H)
  (combine f (left H) (right H)))

(define (heap-insert f x H)
  (if (null? H)
      (make-heap x '() '())
      (if (f x (h-min H))
          (make-heap x (right H) (heap-insert f (h-min  H) (left H)))
          (make-heap (h-min H) (right H) (heap-insert f x (left H))))))

; heap-insert-list, inserts entire list into heap
(define (heap-insert-list f elements H)
  (if (null? elements)
      H
      (heap-insert-list f (cdr elements)
                        (heap-insert f (car elements) H))))

(define (equalize-heaps heap-pair)
  (let ((x1 (car (car heap-pair)))
        (x2 (car (car heap-pair)))
        (H1 (cdr (car heap-pair)))
        (H2 (cdr (cdr heap-pair))))
    (cond ((<= (abs (- x1 x2)) 1)
               heap-pair)
          ((> (- x1 x2) 1)
           (equalize-heaps (cons
                            (cons (- x1 1) (combine > (left H1) (right H1)))
                            (cons (- x2 1) (heap-insert < (value H1) H2)))))
          (else (equalize-heaps (cons (cons
                                       (+ x1 x2) (heap-insert > (value H2) H1))
                                      (cons (+ x2 1)
                                            (combine < (left H2) (right H2))
                                            )
                                      )
                                )
                )
          )
    )
  )


; 4A - moodle answer
(define (equalize-heaps heap-pair)
  (let ((heap1-count (caar heap-pair))
        (heap2-count (cadr heap-pair))
        (heap1 (cdar heap-pair))
        (heap2 (cddr heap-pair))))
  (if (> (abs (- heap1-count heap2-count)) 1)
      (if (> heap1-count heap2-count)
          (equalize-heaps (cons (cons (- heap1-count 1)
                                      (heap-remove > heap1))
                                (cons (+ heap2-count 1)
                                      (heap-insert < (value heap1) heap2))))
          (equalize-heaps (cons (cons (+ heap1-count 1)
                                      (heap-insert > (value heap2) heap1))
                                (cons (- heap20count 1)
                                      (heap-remove < heap2)))))))

"4B -"
(define (add-number x heap-pair)
  (let ((x1 (car (car heap-pair)))
        (x2 (car (cdr heap-pair)))
        (H1 (cdr (car heap-pair)))
        (H2 (cdr (cdr sheap-pair)))))
    (cond ((and (null? (value H1)) (null? (value H2)))
           (cons (car heap-pair) (cons (+ x2 1) (make-tree x (list (list)))))
          ((< x (value H2))
           (equalize-heaps (cons (cons (+ x1 1) (heap-insert > x H1))
                                 (cdr heap-pair))))
          (else (equalize-heaps (cons (car heap-pair)
                                      (cons (+ x2 1) (heap-insert < x H2))))))))

; 4B - moodle answer
(define (add-number x heap-pair)
  (if (or (null? (cddr heap-pair))
          (< x (value (cddr heap-pair))))
      (equalize-heaps (cons (cons (+ (caar heap-pair) 1)
                                  (heap-insert > x (cdar heap-pair)))
                            (cdr heap-pair)))
      (equalize-heaps (cons (car heap-pair)
                            (cons (+ (cadr heap-pair) 1)
                                  (heap-insert < x (cddr heap-pair)))))))
          
"4C - "
(define (avg a b) (/ (+ a b) 2))

(define (get-median heap-pair)
 (let ((int1 (caar heap-pair))
       (int2 (cadr heap-pair))
       (H1 (cdar heap-pair))
       (H2 (cddr heap-pair)))
   (cond ((= int1 int2) (avg (value H1) (value H2)))
         ((> int1 int2) (value H1))
         ((< int1 int2) (value H2)))))

; 4C - moodle answer 
(define (get-median  heap-pair)
  (let ((heap1-count (caar heap-pair))
        (heap2-count (cadr heap-pair))
        (heap1 (cdar heap-pair))
        (heap2 (cddr heap-pair))))
  (cond ((= heap1-count heap2-count)
         (/ (+ (value heap1) (value heap2)) 2))
        ((< heap1-count heap2-count))
        (else (value heap1))))
                     
       
   