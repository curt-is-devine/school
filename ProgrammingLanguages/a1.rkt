#lang racket

(define countdown
    (lambda (n)
        (cond
            [(> 0 n) empty]
            [else (cons  n (countdown (sub1 n)))])))

(define insertR
  (lambda (sym1 sym2 lst)
    (cond
      [(empty? lst) empty]
      [(equal? sym1 (car lst)) (append (list (car lst) sym2) (insertR sym1 sym2 (cdr lst)))]  
      [else (cons (car lst) (insertR sym1 sym2 (cdr lst)))]))) 

(define remv-1st
  (lambda (sym lst)
    (cond
      [(equal? sym (car lst)) (append empty (cdr lst))]
      [else (cons (car lst) (remv-1st sym (cdr lst)))])))

(define list-index-ofv?
  (lambda (sym lst)
    (cond
      [(equal? sym (car lst)) 0]
      [else (+ 1 (list-index-ofv? sym (cdr lst)))])))

(define filter
  (lambda (pred lst)
    (cond
      [(empty? lst) empty]
      [(pred (car lst)) (append (list (car lst)) (filter pred (cdr lst)))]
      [else (filter pred (cdr lst))])))

(define zip
  {lambda (ls1 ls2)
    (cond
      [(or (empty? ls1) (empty? ls2)) empty]
      [else (cons (cons (car ls1) (car ls2)) (zip (cdr ls1) (cdr ls2)))])})

(define map
  (lambda (p ls)
    (cond
      [(empty? ls) empty]
      [else (append (list(p (car ls))) (map p (cdr ls)))])))

(define append
  (lambda (ls1 ls2)
    (cond
      [(empty? ls1) ls2]
      [else (cons (car ls1) (append (cdr ls1) ls2))])))

(define reverse
  (lambda (lst)
    (cond
      [(empty? lst) empty]
      [else (append (reverse (cdr lst)) (list (car lst)))])))

(define fact
  (lambda (num)
    (cond
      [(zero? num) 1]
      [else (* num (fact (sub1 num)))])))

(define memv
  (lambda (e lst)
    (cond
      [(empty? lst) #f]
      [(equal? (car lst) e) lst]
      [else (memv e (cdr lst))])))

(define fib
  (lambda (n)
    (cond
      [(zero? n) 0]
      [(equal? n 1) 1]
      [else (+ (fib (sub1 n)) (fib (- n 2)))])))

;(equal? '((w x) y (z)) '((w . (x . ())) y (z . ())))

(define binary->natural
  (lambda (lst)
    (cond
      [(empty? lst) 0]
      [(zero? (car lst))
          0
          (* 2 (binary->natural (cdr lst)))]
      [else (+ 1 (* 2(binary->natural (cdr lst))))])))

(define minus
  (lambda (n m)
    (cond
      [(zero? m) n]
      [else (sub1 (minus n (sub1 m)))])))

(define div
  (lambda (n m)
    (cond
      [(zero? n) 0]
      [else (+ 1 (div (minus n m) m))])))

(define append-map
  (lambda (p ls)
    (cond
      [(empty? (cdr ls)) (p (car ls))]
      [else (append (p (car ls)) (append-map p (cdr ls)))])))
             
(define set-difference
 (lambda (s1 s2)
   (cond
     [(empty? s1) empty]
     [(member (car s1) s2) (set-difference (cdr s1) s2)]
     [else (append (list (car s1)) (set-difference (cdr s1) s2))])))
;------------------------------------------------------------------------------------------------------------------------------------------
(define buildlst
  (lambda (rec ele)
    (cond
      [(empty? rec) empty]
      [else (cons (cons ele (car rec))
                  (cons (car rec) (buildlst (cdr rec) ele)))])))

(define powerset
  (lambda (lst)
    (cond
      [(empty? lst) (list empty)]
      [else (buildlst (powerset (cdr lst)) (car lst))])))

;----------------------------------------------------------------------------------------------
(define addtolist
  (lambda (ele lst)
    (cond
      [(empty? lst) empty]
      [else (cons (list ele (car lst)) (addtolist ele (cdr lst)))]))) 

(define cartesian-product
  (lambda (lol) ;lol = list of lists
    (cond
      [(empty? (car lol)) empty]
      [else (append (addtolist (car (car lol))
                               (car (cdr lol)))
                    (cartesian-product (list (cdr (car lol)) (car (cdr lol)))))])))

;----------------------------------------------------------------------------------------------
(define insertR-fr
  (lambda (sym1 sym2 lst)
    (foldr (lambda (first rec)       
             (cond
               [(equal? sym1 first) (append (list first sym2) rec)]  
               [else (cons first rec)]))
           '()
           lst)))
    
(define filter-fr
  (lambda (pred lst)
    (foldr (lambda (first rec)
             (cond
               [(pred first) (append (list first) rec)]
               [else rec]))
           empty
           lst)))


(define map-fr
  (lambda (p ls)
    (foldr (lambda (first rec)
             (cons (p first) rec))
           empty
           ls)))

(define append-fr
  (lambda (ls1 ls2)
    (foldr (lambda (first rec)
             (cons first rec))
           ls2  
           ls1)))

(define reverse-fr
  (lambda (lst)
    (foldr (lambda (first rec)
             (append rec (list first)))
           empty
           lst)))

(define binary->natural-fr
  (lambda (lst)
    (foldr (lambda (first rec)
             (cond
               [(zero? first) (* 2 rec)]
               [else (+ 1 (* 2 rec))]))
           0
           lst)))

(define append-map-fr
  (lambda (p ls)
    (foldr (lambda (first rec)
             (append (p first) rec))
           '()
           (p (car ls)))))


(define set-difference-fr
 (lambda (s1 s2)
   (foldr (lambda (first rec)
            (cond
              [(member first s2) rec]
              [else (append (list first) rec)]))
          '()
          s1)))

(define buildlst-fr
  (lambda (rec ele)
    (foldr (lambda (first rec)
      (cons (cons ele first)
            (cons first rec)))
    empty
    rec)))

(define powerset-fr
  (lambda (lst)
    (foldr (lambda (first rec)
             (buildlst-fr rec first))
    (list empty)
    lst)))
 
(define addtolist-fr
  (lambda (ele lst)
    (foldr (lambda (first rec)
             (cons (list ele first) rec))
           empty
           lst)))

;does not work
(define cartesian-product-fr
  (lambda (lol)
   (foldr (lambda (first rec)
            (append (addtolist (car first) (car (cdr lol)))
                    rec))
          empty
          (car lol))))

;(cartesian-product-fr '((5 4) (3 2 1)))

(define getfirstele
  (lambda (lol)
    (car (car lol))))



;(define cartesian-product
;  (lambda (lol)
;    (foldr (lambda (rec)
;      [else (append (addtolist (getfirstele lol) lol)
;                               (car (cdr lol)))
;                    (cartesian-product (list (cdr (car lol)) (car (cdr lol)))))])))
;            empty
;            (car lol)


;----------------------------------------------------------------------------------------------
;does not work
(define collatz
  (letrec
    ((odd-case
       (lambda (recur)
         (lambda (x)
           (cond 
            ((and (positive? x) (odd? x)) (collatz (add1 (* x 3)))) 
            (else (recur x))))))
     (even-case
       (lambda (recur)
         (lambda (x)
           (cond 
            ((and (positive? x) (even? x)) (collatz (/ x 2))) 
            (else (recur x))))))
     (one-case
       (lambda (recur)
         (lambda (x)
           (cond
            ((zero? (sub1 x)) 1)
            (else (recur x))))))
     (base
       (lambda (x)
         (error 'error "Invalid value ~s~n" x))))  
    ;(or (odd-case) (even-case) (one-case) base);; this should be a single line, without lambda
    base
    ))

;(collatz 1)