#lang racket

(require "monads.rkt")


(define return-maybe
  (lambda (a)
    `(Just ,a)))

(define fail
  (lambda ()
    '(Nothing)))


(define findf-maybe
  (lambda (p l)
    (cond
      [(null? l) (fail)]
      [else (if (p (car l)) (return-maybe (car l))
                            (findf-maybe p (cdr l)))])))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define return-writer
  (lambda (a)
    `(,a . ())))


(define bind-writer
  (lambda (ma f)
    (let ((mb (f (car ma))))
      `(,(car mb) . ,(append (cdr ma) (cdr mb))))))


(define tell-writer
  (lambda (to-writer)
    `(_ . (,to-writer))))

(define partition-writer
  (lambda (p l)
    (cond
      [(null? l) (return-writer `())]
      [(not (p (car l))) (bind-writer
                    (partition-writer p (cdr l))
                    (lambda (d)
                      (return-writer (cons (car l) d))))]
      [else
       (bind-writer
        (tell-writer (car l))
        (lambda (_)
          (partition-writer p (cdr l))))])))

(define powerXpartials
  (lambda (b e)
    (cond
      [(zero? e) (return-writer 1)]
      [(equal? e 1) (return-writer b)]
      [(odd? e) (bind-writer (powerXpartials b (sub1 e))
                             (lambda (o)
                               (bind-writer (tell-writer o)
                                            (lambda (_)
                                              (return-writer (* b o))))))]
      [(even? e) (bind-writer (powerXpartials b (/ e 2))
                             (lambda (o)
                               (bind-writer (tell-writer o)
                                            (lambda (_)
                                              (return-writer (* o o))))))])))



(powerXpartials 2 4)
;I cannot get the order of this right

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define return-state
  (lambda (a)
    (lambda (s)
      `(,a . ,s))))

(define bind-state
  (lambda (ma f)
    (lambda (s)
      (let ([vs^ (ma s)])
        (let ([v (car vs^)]
              [s^ (cdr vs^)])
          ((f v) s^))))))

(define get-state
  (lambda (s) `(,s . ,s)))

(define put-state
  (lambda (new-s)
    (lambda (s)
      `(__ . ,new-s))))


;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define traverse
    (lambda (inj bind f)
      (letrec
        ((trav
           (lambda (tree)
             (cond
               [(pair? tree)
                (go-on
                  (a <- (trav (car tree)))
                  (d <- (trav (cdr tree)))
                  (inj (cons a d)))]
               [else (f tree)]))))
        trav)))

(define reciprocal
  (lambda (n)
    (cond
      [(zero? n) (fail)]
      [else (return-maybe (/ 1 n))])))

(define traverse-reciprocal
  (traverse return-maybe bind-maybe reciprocal))

;(traverse-reciprocal '((1 . 2) . (3 . (4 . 5))))
;I keep getting the error "a is not a monad" but this code is provided by the web page?