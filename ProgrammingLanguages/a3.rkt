#lang racket

(define value-of
  (lambda (exp env)
    (match exp
      [`,y #:when (number? y) y]
      [`,y #:when (boolean? y) y]
      [`,y #:when (symbol? y) (env y)]
      [`(lambda (,x) ,body) (lambda (a) (value-of body (lambda (y) (if (eqv? y x) a
                                                                                 (env y)))))]
      [`(zero? ,y) (zero? (value-of y env))]
      [`(sub1 ,y) (sub1 (value-of y env))]
      [`(* ,y ,z) (* (value-of y env) (value-of z env))] 
      [`(set! ,id ,expr) (let ((vexpr (value-of expr env))
                               (vid (env id)))
                           (set! vid vexpr))]
      [`(begin2 ,expr ,val) (begin (value-of expr env) (value-of val env))] ;order of begin matters?      
      [`(let ((,y ,yold)) ,arg) (let ((a (value-of yold env)))
                                  (value-of arg (lambda (var) (if (eqv? var y) a
                                                                               (env var)))))]
      [`(if ,cond ,affirm ,neg) (if (value-of cond env) (value-of affirm env)
                                    (value-of neg env))]
      [`(,rator ,rand) ((value-of rator env) (value-of rand env))])))

;---------------------------------------------------------------------------------------------
(define empty-env-fn
  (lambda ()
    (lambda (y) (error 'value-of "unbound variable ~s" y))))

(define extend-env-fn
  (lambda (x a env)
    (lambda (y)
      (if (eqv? x y) a
                     (apply-env-fn env y))))) 
(define apply-env-fn
  (lambda (env x)
    (env x)))

(define value-of-fn
  (lambda (exp env)
    (match exp
      [`,y #:when (integer? y) y]
      [`,y #:when (boolean? y) y]
      [`,y #:when (symbol? y) (env y)]
      [`(lambda (,x) ,body) (lambda (a) (value-of-fn body (extend-env-fn x a env)))]
      [`(sub1 ,y) (sub1 (value-of-fn y env))]
      [`(zero? ,y) (zero? (value-of-fn y env))]
      [`(* ,y ,z) (* (value-of-fn y env) (value-of-fn z env))]
      [`(let ((,y ,yold)) ,arg) (let ((a (value-of-fn yold env)))
                                  (value-of-fn arg (extend-env-fn y a env)))]
      [`(if ,cond ,affirm ,neg) (if (value-of-fn cond env) (value-of-fn affirm env)
                                                           (value-of-fn neg env))]
      [`(,rator ,rand) ((value-of-fn rator env) (value-of-fn rand env))])))

;------------------------------------------------------------------------------------------
(define empty-env-ds
  (lambda ()
    `(empty-env-ds)))

(define extend-env-ds
  (lambda (x a env)
    `(extend-env-ds ,x ,a ,env)))

(define apply-env-ds
  (lambda (env var)
    (match env
      [`(empty-env-ds) (lambda (y) (error 'value-of "unbound variable ~s" y))]
      [`(extend-env-ds ,x ,a ,env) (if (eqv? x var) a
                                                    (apply-env-ds env var))])))

(define value-of-ds
  (lambda (exp env)
    (match exp
      [`,y #:when (integer? y) y]
      [`,y #:when (boolean? y) y]
      [`,y #:when (symbol? y) (apply-env-ds env y)]
      [`(lambda (,x) ,body) (lambda (a) (value-of-ds body (extend-env-ds x a env)))]
      [`(zero? ,y) (zero? (value-of-ds y env))]
      [`(sub1 ,y) (sub1 (value-of-ds y env))]
      [`(* ,y ,z) (* (value-of-ds y env) (value-of-ds z env))]
      [`(let ((,y ,yold)) ,arg) (let ((a (value-of-ds yold env)))
                                  (value-of-ds arg (extend-env-ds y a env)))]
      [`(if ,cond ,affirm ,neg) (if (value-of-ds cond env) (value-of-ds affirm env)
                                    (value-of-ds neg env))]
      [`(,rator ,rand) ((value-of-ds rator env) (value-of-ds rand env))])))
;------------------------------------------------------------------------------------------
(define fo-eulav
  (lambda (exp env)
    (match exp
      [`,y #:when (integer? y) y]
      [`,y #:when (symbol? y) (env y)]
      [`(,body (,x) adbmal) (lambda (a) (fo-eulav body (lambda (y) (if (eqv? y x) a
                                                                                  (env y)))))]
      [`(,y ?orez) (zero? (fo-eulav y env))]
      [`(,y 1bus) (sub1 (fo-eulav y env))]
      [`(,z ,y *) (* (fo-eulav y env) (fo-eulav z env))]
      [`(,arg ((,yold ,y)) tel) (let ((a (fo-eulav yold env)))
                                  (fo-eulav arg (lambda (var) (if (eqv? var y) a
                                                                               (env var)))))]
      [`(,neg ,affirm ,cond fi) (if (fo-eulav cond env) (fo-eulav affirm env)
                                                        (fo-eulav neg env))]
      [`(,rand ,rator) ((fo-eulav rator env) (fo-eulav rand env))])))
      
;------------------------------------------------------------------------------------------
(define (apply-env-lex env n)
  (cond
    [(zero? n) (car env)]
    [else (apply-env-lex (cdr env) (- n 1))]))
  
(define (extend-env-lex n env)
  (cons n env))

(define value-of-lex
  (lambda (exp env)
    (match exp
      [`(const ,expr) expr]
      [`(mult ,x1 ,x2) (* (value-of-lex x1 env) (value-of-lex x2 env))]
      [`(zero ,x) (zero? (value-of-lex x env))]
      (`(sub1 ,body) (sub1 (value-of-lex body env)))
      (`(if ,t ,c ,a) (if (value-of-lex t env) (value-of-lex c env) (value-of-lex a env)))
      (`(var ,num) (apply-env-lex env num))
      (`(lambda ,body) (lambda (a) (value-of-lex body (extend-env-lex a env))))
      (`(,rator ,rand) ((value-of-lex rator env) (value-of-lex rand env))))))
 
(define empty-env-lex 
  (lambda () '()))



