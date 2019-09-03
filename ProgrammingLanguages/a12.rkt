#lang racket

(require "mk.rkt")
(require "numbers.rkt")


(define-relation (nullo x)
    (== '() x))

(define-relation (cdro p d)
    (fresh (a)
           (== (cons a d) p)))

(define-relation (listo ls)
    (conde
     ((nullo ls))
     ((fresh (d)
             (cdro ls d)
             (listo d)))))

(define-relation (facto n f)
    (conde
     ((== '() n) (== f '(1)))
     ((fresh (k fs)
             (minuso n '(1) k)
             (facto k fs) 
             (*o n fs f)))))

(define-relation (fibso n outn outn1)
    (conde
     ((== '() n) (== '(1) outn) (== '(1) outn1))
     ((fresh (n- o1 o2 sum)
            (minuso n '(1) n-)
            (fibso n- o1 o2)
            (pluso o1 o2 sum)
            (== o2 outn)
            (== sum outn1)))))

(define empty-env
  (lambda ()
    (lambda (y) (error 'value-of "unbound variable ~s" y))))

(define fo-lav
  (lambda (exp env)
    (match exp
      [`,y #:when (integer? y) y]
      [`,y #:when (symbol? y) (env y)]
      [`(,y etouq) y]
      [`(,y tsil) (list (fo-lav y env))]
      [`(,body (,x) adbmal) (lambda (a) (fo-lav body (lambda (y) (if (eqv? y x) a
                                                                                  (env y)))))]
      [`(,arg ((,yold ,y)) tel) (let ((a (fo-lav yold env)))
                                  (fo-lav arg (lambda (var) (if (eqv? var y) a
                                                                               (env var)))))]
      [`(,rand ,rator) ((fo-lav rator env) (fo-lav rand env))])))


(define-relation (lookup x vars vals o)
  (fresh (y vars^ v vals^)
    (== `(,y . ,vars^) vars)
    (== `(,v . ,vals^) vals)
    (conde
      [(== x y) (== v o)]
      [(=/= x y) (lookup x vars^ vals^ o)])))

(define-relation (valsof es vars vals o)
  (conde 
    [(== `() es) (== '() o)]
    [(fresh (e es^)
       (== `(,e . ,es^) es)
       (fresh (v vs)
         (== `(,v . ,vs) o)
         (fo-lavo e vars vals v)
         (valsof es^ vars vals vs)))]))

;    [(fresh (x b)
;       (== `(λ (,x) ,b) exp)
;       (absento 'λ vars)
;       (symbolo x)
;       (== `(clos ,x ,b ,vars ,vals) o))]
;    [(== `(quote ,o) exp)
;     (absento 'quote vars)
;     (absento 'clos o)]
;    [(fresh (es)
;       (== `(list . ,es) exp)
;       (absento 'list vars)
;       (valsof es vars vals o))]
;    [(fresh (rator rand)
;         (== `(,rator ,rand) exp)
;         (=/= rator 'quote) (=/= rator 'list)
;         (fresh (x b vars^ vals^ a) 
;           (valof rator vars vals `(clos ,x ,b ,vars^ ,vals^))
;           (valof rand vars vals a)
;           (valof b `(,x . ,vars^) `(,a . ,vals^) o)))]))

;this does not work, but after 5 hours of trying, I just cant figure this out...
(define-relation (fo-lavo exp vars vals o)
  (conde
   [(symbolo exp) (lookup exp vars vals o)]
   [(fresh (x b)
           (== `(,b (,x) adbmal) exp)
           (absento 'adbmal vars)
           (symbolo x)
           (fresh (a y)
                  (conde
                   [(== x y) (fo-lavo b a vals o)]
                   [(fo-lavo b vars vals o)])))]
   [(fresh (rator rand)
           (== '(,rand ,rator) exp)
           (=/= rator 'etouq) (=/= rator 'tsil)
           (fresh (x b vars^ vals^ a)
                  (fo-lavo rator vars vals o)))]))

   ;[(fresh (etouq)
    ;       (== `(,y etouq) exp)
     ;      (absento 'etouq vars)
      ;     (== 
      ;[`,y #:when (integer? y) y]
      ;[`,y #:when (symbol? y) (env y)]))
      ;[`(,y etouq) y]
      ;[`(,y tsil) (list (fo-lavo y env))]
      ;(lambda (a) (fo-lavo body (lambda (y) (if (eqv? y x) a (env y)))))]
      ;[`(,arg ((,yold ,y)) tel) (let ((a (fo-lavo yold env)))
      ;                            (fo-lavo arg (lambda (var) (if (eqv? var y) a
      ;                                                                         (env var)))))]
      ;[`(,rand ,rator) ((fo-lavo rator env) (fo-lavo rand env))]))
;(run 1 (q) (fo-lavo (lambda (x) 5 '() '() q))