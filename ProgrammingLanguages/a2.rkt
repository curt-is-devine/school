#lang racket

(define list-ref
  (lambda (ls n)
    (letrec
        ([nth-cdr
          (lambda (n)
            (cond
              [(zero? n) ls]
              [else (cdr (nth-cdr (sub1 n)))]))])
      (car (nth-cdr n)))))

(define union
  (lambda (ls1 ls2)
    (cond
      [(empty? ls2) ls1]
      [(memv (car ls2) ls1) (union ls1 (cdr ls2))]
      [else (union (cons (car ls2) ls1) (cdr ls2))])))

(define extend
  (lambda (x pred)
    (define both
      (lambda (test)
        (or (eqv? x test) (pred test))))
    both))

(define walk-symbol
  (lambda (x s)
    (cond
      [(and (assv x s) (symbol? (cdr (assv x s)))) (walk-symbol (cdr (assv x s)) s)]
      [(assv x s) (cdr (assv x s))]
      [else x])))
      
(define lambda->lumbda
  (lambda (e)
    (match e
      [`,y #:when (symbol? y) y]
      [`(lambda (,x) ,body) `(lumbda (,x) ,(lambda->lumbda body))]
      [`(,rator ,rand) (or `(,(lambda->lumbda rator) ,(lambda->lumbda rand)))])))

(define var-occurs?
  (lambda (v e)
    (match e
      [`,y #:when (symbol? y) (eqv? v y)]
      [`(lambda (,x) ,body) (var-occurs? v body)]
      [`(,rator ,rand) (or (var-occurs? v rator) (var-occurs? v rand))])))

(define vars
  (lambda (e)
    (match e
      [`,y #:when (symbol? y) (list y)]
      [`(lambda (,x) ,body) (vars body)]
      [`(,rator ,rand) (append (vars rator) (vars rand))])))

(define unique-vars
  (lambda (e)
    (match e
      [`,y #:when (symbol? y) (list y)]
      [`(lambda (,x) ,body) (unique-vars body)]
      [`(,rator ,rand) (union (unique-vars rator) (unique-vars rand))])))

(define var-occurs-free?
  (lambda (var e)
    (match e
      [`,y #:when (symbol? y) (eqv? y var)]
      [`(lambda (,x) ,body) (if (eqv? var x) #f (var-occurs-free? var body))]
      [`(,rator ,rand) (or (var-occurs-free? var rator) (var-occurs-free? var rand))])))

(define var-occurs-bound?
  (lambda (var e)
    (match e
      [`,y #:when (symbol? y) #f]
      [`(lambda (,x) ,body) (or (var-occurs-bound? var body)
                                (and (eqv? x var)
                                     (var-occurs? var body)))]
      [`(,rator ,rand) (or (var-occurs-bound? var rator) (var-occurs-bound? var rand))])))
 
(define unique-free-vars
  (lambda (e)
    (define vars (unique-vars e))
    (match e
      [`,y #:when (symbol? y) vars]
      [`(lambda (,x) ,body) (remv x vars)]
      [`(,rator ,rand) (union (unique-free-vars rator) (unique-free-vars rand))])))

(define unique-bound-vars
  (lambda (e)
    (define vars (unique-vars e))
    (match e
      [`,y #:when (symbol? y) (remv y vars)]
      [`(lambda (,x) ,body) (if (var-occurs? x body) (union (list x) (unique-bound-vars body))
                                (and (remv x vars) (unique-bound-vars body)))]
      [`(,rator ,rand) (union (unique-bound-vars rator) (unique-bound-vars rand))])))

(define lex
  (lambda (e ls)
    (match e
      [`,y #:when (symbol? y) (cons 'var
                                    (walk-symbol y ls))]
      [`(lambda (,x) ,body)   (list 'lambda
                                    (lex body (map (lambda (duo) (if (eqv? (car duo) x) duo
                                                                                        (list (car duo) (add1 (car (cdr duo))))))
                                                   (cons (list x 0) ls))))]
      [`(,rator ,rand)        (cons (lex rator ls)
                                    (list (lex rand ls)))])))


(define walk-symbol-update
  (lambda (x s)
    (match (walk-symbol x s)
      [`,t #:when (number? (unbox t)) (unbox t)]
      [`,y #:when (box? y) (and (walk-symbol-update (unbox y) s)
                                (set-box! y (unbox (walk-symbol (unbox y) s)))
                                (walk-symbol-update x s))]
      [`,a #:when (symbol? a) (walk-symbol-update a s)])))
  



