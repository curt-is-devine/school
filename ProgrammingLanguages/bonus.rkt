#lang racket
(define filter-sps
  (lambda (pred lst store)
    (cond
      [(empty? lst) (values lst store)]
      [(pred (car lst)) (let-values ([(f1 store) (filter-sps pred (cdr lst) store)])
                          (values (cons (car lst) f1) store))]
      [else (let-values ([(f1 store) (filter-sps pred (cdr lst) store)])
              (values f1 (cons (car lst) store)))])))

(define filter*-sps
  (lambda (f ls store)
    (cond
      [(null? ls) (values ls store)]
      [(pair? (car ls)) (let-values ([(f1 store1) (filter*-sps f (car ls) store)])
                          (let-values([(f2 store2) (filter*-sps f (cdr ls) store)])
                            (values `(,f1 . ,f2) (append `(,store1 . ,store2) store))))]
      [(null? (car ls)) (values ls store)]
      [(f (car ls)) (let-values ([(f1 store) (filter*-sps f (cdr ls) store)])
                          (values (cons (car ls) f1) store))]
      [else (let-values ([(f1 store) (filter*-sps f (cdr ls) store)])
              (values f1 (cons (car ls) store)))])))

(define fib-sps
  (λ (n store)
    (cond
      [(zero? n) (values 0 '((0 . 0)))]
      [(zero? (sub1 n)) (let-values ([(fub-sub1 store) (fib-sps (sub1 n) store)])
                          (values 1 (cons '(1 . 1) store)))]
      [else (let-values ([(fib-sub1 store1) (fib-sps (sub1 n) store)])
              (let-values ([(fib-sub2 store2) (fib-sps (sub1 (sub1 n)) store)])
                (values (+ fib-sub1 fib-sub2)
                        (cons `(,n . ,(+ fib-sub1 fib-sub2)) (cons `(,(sub1 n) . ,fib-sub1) store2)))))])))

(define-syntax and*
  (syntax-rules ()
    [(and*) #t]
    [(and* a) (and a)]
    [(and* a b c ...) (and a (and* b c ...))]))

(define-syntax list*
  (syntax-rules ()
    [(list*) (raise-syntax-error "Incorrect argument-count to list*")]
    [(list* a) a]
    [(list* a b c ...) (cons a (list* b c ...))]))

(define-syntax macro-list
  (syntax-rules ()
    [(macro-list) '()]
    [(macro-list a) '(a)]
    [(macro-list a b ...) (cons a (macro-list b ...))]))

(define-syntax mcond
  (syntax-rules ()
    [(mcond (else res)) res]
    [(mcond (cond1 res1) (cond2 res2)) (if cond1 res1 (mcond (cond2 res2)))]  ))

(define-syntax quote-quote
    (syntax-rules ()
      [(_ e) (quote (quote e))]))

(define-syntax copy-code
    (syntax-rules ()
      [(_ x) `(,x x)]))

(define-syntax macro-map
  (syntax-rules ()
    [(macro-map f '()) '()]
    [(macro-map f '((a))) (f a)]
    [(macro-map f '(a b ...)) (cons (f a) (macro-map f '(b ...)))]))



    
    