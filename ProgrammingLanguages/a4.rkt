#lang racket


(define walk-symbol
  (lambda (x s)
    (cond
      [(and (assv x s) (symbol? (cdr (assv x s)))) (walk-symbol (cdr (assv x s)) s)]
      [(assv x s) (cdr (assv x s))]
      [else x])))

(define lex
  (lambda (e env)
    (match e
      [`,y #:when (number? y) (list 'const y)]
      [`,y #:when (symbol? y) (cons 'var
                                    (walk-symbol y env))]
      [`(zero? ,y)            (cons 'zero? (list (lex y env)))]
      [`(* ,x ,y)             (cons '* (list(lex x env) (lex y env)))]
      [`(sub1 ,x)             (cons 'sub1 (list (lex x env)))]
      [`(lambda (,x) ,body)   (list 'lambda
                                    (lex body (map (lambda (duo) (if (eqv? (car duo) x) duo
                                                                                        (list (car duo) (add1 (car (cdr duo))))))
                                                   (cons (list x 0) env))))]
      [`(if ,cond ,tru ,fal)  (cons 'if (list (lex cond env) (lex tru env) (lex fal env)))]
      [`(let ((,y ,exp)) ,body) (list 'let (lex exp env) (lex body (map (lambda (duo) (if (eqv? (car duo) y) duo
                                                                                        (list (car duo) (add1 (car (cdr duo))))))
                                                   (cons (list y 0) env))))]
      [`(,rator ,rand)        (cons (lex rator env)
                                    (list (lex rand env)))])))

(define empty-env
  (lambda ()
    '()))

(define extend-env
  (lambda (x a env)
    (cons (cons x a) env))) 

(define apply-env
  (lambda (env var)
    (cond
      [(assq var env) (cdr (assq var env))]
      [else (error 'env "unbound variable. ~s" var)])))

(define closure-fn
  (lambda (var body env)
    (lambda (y)
      (value-of-fn body (extend-env var y env)))))

(define apply-closure-fn
  (lambda (clos var)
    (clos var)))

(define value-of-fn
  (lambda (exp env)
    (match exp
      [`,y #:when (integer? y) y]
      [`,y #:when (boolean? y) y]
      [`,y #:when (symbol? y) (apply-env env y)]
      [`(lambda (,x) ,body) (closure-fn x body env)]
      [`(sub1 ,y) (sub1 (value-of-fn y env))]
      [`(zero? ,y) (zero? (value-of-fn y env))]
      [`(* ,y ,z) (* (value-of-fn y env) (value-of-fn z env))]
      [`(let ((,y ,yold)) ,arg) (let ((a (value-of-fn yold env)))
                                  (value-of-fn arg (extend-env y a env)))]
      [`(if ,cond ,affirm ,neg) (if (value-of-fn cond env) (value-of-fn affirm env)
                                                           (value-of-fn neg env))]
      [`(,rator ,rand) (apply-closure-fn (value-of-fn rator env) (value-of-fn rand env))])))

(define closure-ds
  (lambda (id body env)
    `(closure ,id ,body ,env)))

(define apply-closure-ds
  (lambda (closure arg)
    (match closure
      [`(closure ,id ,body ,env) (value-of-ds body (extend-env id arg env))])))

(define value-of-ds
  (lambda (exp env)
    (match exp
      [`,y #:when (integer? y) y]
      [`,y #:when (boolean? y) y]
      [`,y #:when (symbol? y) (apply-env env y)]
      [`(lambda (,x) ,body) (closure-ds x body env)]
      [`(sub1 ,y) (sub1 (value-of-ds y env))]
      [`(zero? ,y) (zero? (value-of-ds y env))]
      [`(* ,y ,z) (* (value-of-ds y env) (value-of-ds z env))]
      [`(let ((,y ,yold)) ,arg) (let ((a (value-of-ds yold env)))
                                  (value-of-ds arg (extend-env y a env)))]
      [`(if ,cond ,affirm ,neg) (if (value-of-ds cond env) (value-of-ds affirm env)
                                                           (value-of-ds neg env))]
      [`(,rator ,rand) (apply-closure-ds (value-of-ds rator env) (value-of-ds rand env))])))


(define value-of-dynamic
  (lambda (exp env)
    (match exp
      [`(null? ,x) (null? (value-of-dynamic x env))]
      [`(cons ,a ,d) (cons (value-of-dynamic a env) (value-of-dynamic d env))]
      [`(car ,ls) (car (value-of-dynamic ls env))]
      [`(cdr ,ls) (cdr (value-of-dynamic ls env))]
      [`(zero? ,x) (zero? (value-of-dynamic x env))]
      [`(sub1 ,x) (sub1 (value-of-dynamic x env))]
      [`(* ,x ,y) (* (value-of-dynamic x env) (value-of-dynamic y env))]
      [`(let ([,y ,yold]) ,body) (value-of-dynamic body (extend-env y (value-of-dynamic yold env) env))]
      [`(quote ,v) v]
      [`,n #:when (number? n) n]
      [`,y #:when (symbol? y) (apply-env env y)]
      [`(lambda (,x) ,body) `(lambda (,x) ,body)]
      [`(,rator ,rand) (match-let ([`(lambda (,x) ,b) (value-of-dynamic rator env)]
                                   [`,a (value-of-dynamic rand env)])
                         (value-of-dynamic b (extend-env x a env)))]
      [`(if ,test ,affirm ,neg) (if (value-of-dynamic test env) (value-of-dynamic affirm env)
                                                                (value-of-dynamic neg env))])))

(define empty-env-fn empty-env)
(define empty-env-ds empty-env)
(define extend-env-fn extend-env)
(define extend-env-ds extend-env)
(define apply-env-fn apply-env)
(define apply-env-ds apply-env)

(define closure-fn-ri
  (lambda (var body env body2)
    (lambda (x y)
      ((body2 (y var x env)) body))))

(define apply-closure-fn-ri
  (lambda (clo x extend-env)
    (clo x extend-env)))

(define closure-ds-ri closure-fn-ri)
(define apply-closure-ds-ri apply-closure-fn-ri)

(define value-of-ri
  (lambda (empty-env extend-env apply-env closure apply-closure)
    (letrec ([again (lambda (env)
                        (lambda (exp)
                          (match exp
                            [`,y #:when (number? y) y]
                            [`,y #:when (boolean? y) y]
                            [`,y #:when (symbol? y) (apply-env env y)]
                            [`(* ,x ,y) (* ((again env) x) ((again env )))]
                            [`(sub1 ,y) ((again env) y)]
                            [`(zero? ,y) (zero? ((again env) y))]
                            [`(if ,cond ,affirm ,neg) (if ((again env) cond) ((again env) affirm)
                                                                             ((again env) neg))]
                            [`(let ([,y ,yold]) ,body) (let ([x ((again env) yold)])
                                                         ((again (extend-env y x)) body))]
                            [`(lambda (,x) ,body) (closure x body env again)]
                            [`(,rator ,rand) (apply-closure ((again env) rator) ((again env) rand) extend-env)])))])
      (again (empty-env)))))

                                                      