"Problem 1 Currency Conversion"
 (define (usd-gbp usd)
   (* usd 0.77))
   
 (define (gbp-eur gbp)
   (* gbp 1.11))
      
 (define (eur-sek eur)
   (* eur 10.61))

 (define (usd-sek usd)
   (usd-gbp
    (gbp-eur
     (eur-sek usd))))

"A - USD-GBP Conversion"
 (usd-gbp 175)

"B - GBP-EUR Conversion"
 (gbp-eur 20)
   
"C - EUR-SEK Conversion"
 (eur-sek 240)

"D - USD-SEK Conversion"
 (usd-sek 175)

"Problem 2A"
   (define (det2x2 a b c d)
     (-
      (* a d)
      (* b c)))

"Test Determinant of N"
(det2x2 -3 1 2 7)
   
"Problem 2B"
 (define (invertible? a b c d)
  (not (= (det2x2 a b c d) 0)))

"Test Invertibility of M"
 (invertible? 2 -4 -6 12)
 
"Test Invertibility of N"
 (invertible? -3 1 2 7)

"Problem 2C"
"pro-inv-direct?"
 (define (prod-inv-direct? a1 b1 c1 d1 a2 b2 c2 d2)
  (invertible? (+ (* a1 a2) (* b1 c2))
   (+ (* a1 b2) (* b1 d2))
    (+ (* c1 a2) (* d1 c2))
     (+ (* c1 b2) (* d1 d2))))

"prov-inv-indirect?"
 (define (prod-inv-indirect? a1 b1 c1 d1 a2 b2 c2 d2)
   (not
    (zero?
     (* (det2x2 a1 b1 c1 d1)
        (det2x2 a2 b2 c2 d2)))))
   

"Problem 2D"
(define (det3x3 a b c
                d e f
                g h i)
 (+ (- (* a (det2x2 e f
                    h i)
       (* b (det2x2 d f
                    g i)))
       (* c (det2x2 d e
                    g h)))))

(det3x3 0 5 -6
        8 -11 4
        5 1 1)