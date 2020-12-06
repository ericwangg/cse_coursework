"Lab 8 - Eric Wang"

"1 - List has duplicates"
(define (has-duplicates? lst)
  (cond ((null? lst) #f)
        ((member (car lst) (cdr lst)) #t)
        (else (has-duplicates? (cdr lst)))))

(member 3 '(1 2 3))
(has-duplicates? (list 1 2 3 3))



"2 - Number of zeros in list"
(define (num-zeroes lst)
  (define (helper lst acc)
    (if (null? lst)
        acc
        (if (list? (car lst))
            (helper (cdr lst) (+ (helper (car lst) 0) acc))
            (if (= (car lst) 0)
                (helper (cdr lst) (+ 1 acc))
                (helper (cdr lst) acc)))))
  (helper lst 0))

(num-zeroes '(1 2 3 4 0 6))
(num-zeroes (list 0 0 (list 0.0 (list 0 0) (list)) 0))



"3A - Insert value into sorted list"
(define (swap-first-two lst)
  (cond ((null? lst) '())
        ((< (length lst) 2) (car lst))
        (else (cons (car (cdr lst)) (cons (car lst) (cdr (cdr lst)))))))

(define (bubble-up lst)
  (if (null? (cdr lst))
      lst
      (if (> (car lst) (car (cdr lst)))
          (cons (car (swap-first-two lst)) (bubble-up (cdr (swap-first-two lst))))
          (cons (car lst) (bubble-up (cdr lst))))))

(define (bubble-sort-aux lst n)
  (if (= n 0)
      lst
      (bubble-up (bubble-sort-aux lst (- n 1)))))

(define (bubble-sort lst)
  (bubble-sort-aux lst (length lst)))

(define (insert item lst precedes)
  (cond ((null? lst) (cons item lst))
        ((eqv? precedes <) (bubble-sort (cons item lst)))
        ((eqv? prededes >) (reverse (bubble-sort (cons (item lst)))))))

(insert 1 '( 2 3 4) < )
(insert 1 '() < )

"3B - Insert All"
(define (insert-all lst precedes)
  (cond ((null? lst) '())
        ((eqv? precedes <) (bubble-sort lst))
        ((eqv? precedes >) (reverse (bubble-sort lst)))))



"4A - Tree Node Count"
(define (make-tree value left right)
  (list value left right))

(define (value tree)
  (car tree))

(define (left tree)
  (cadr tree))

(define (right tree)
  (caddr tree))

(define empty-tree? null?)

(define testtree
  (make-tree
   1
   (make-tree
    3
    (make-tree 7 '() '())
    (make-tree 9 '() '()))
   (make-tree 5 '() '())))

(define (tree-node-count t)
  (if (empty-tree? t)
      0
      (+ 1 (tree-node-count (left t)) (tree-node-count (right t)))))

"tree-node-count testtree"
(tree-node-count testtree)

"4B - Sum of tree nodes"
(define (tree-node-sum t)
  (if (empty-tree? t)
      0
      (+ (value t)
         (tree-node-sum (left t))
         (tree-node-sum (right t)))))

"tree-node-sum testtree"
(tree-node-sum testtree)

"4C - Height of Tree"
(define (tree-height t)
  (if (null? t)
      -1
      (+ 1 (max (tree-height (left t)) (tree-height (right t))))))

"4D - Tree Map"
(define (tree-map f t)
  (if (null? t)
      '()
      (make-tree (f (value t)) (tree-map f (left t)) (tree-map f (right t)))))
 
(tree-map (lambda (x) (* x (+ x 1))) (make-tree 1 '() '()))
