#lang racket
(require racket/trace)

(define empty-env
  (lambda ()
    (lambda (y) (error 'value-of "unbound variable ~s" y))))

(define extend-env
  (lambda (x a env)
    (lambda (y)
      (if (eqv? x y) a
                     (apply-env env y)))))
          
(define apply-env
  (lambda (env x)
    (env x)))

(define make-closure
  (lambda (x body env)
    (lambda (a)
       (value-of body (extend-env x a env)))))

(define apply-closure
  (lambda (clos x)
    (clos x)))
        
(define value-of
  (lambda (exp env)
    (match exp
      [`,b #:when (boolean? b) b]
      [`,n #:when (number? n)  n]
      [`(zero? ,n) (zero? (value-of n env))]
      [`(sub1 ,n) (sub1 (value-of n env))]
      [`(* ,n1 ,n2) (* (value-of n1 env) (value-of n2 env))]
      [`(if ,test ,conseq ,alt) (if (value-of test env)
                                  (value-of conseq env)
                                  (value-of alt env))]
      [`(begin2 ,e1 ,e2) (begin (value-of e1 env) (value-of e2 env))]
      [`(random ,n) (random (value-of n env))]
      [`,y #:when (symbol? y) (apply-env env y)]
      [`(set! ,x ,val)  (let ([v (value-of val env)])
                          (set! x v))]
      [`(lambda (,x) ,body) (make-closure x body env)]
      [`(,rator ,rand) (apply-closure (value-of rator env)
                                      (value-of rand env))])))



;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

;for val-of-cbneed and Brainteaser of val-of-cbv
(define getit
  (lambda (exp)
    (let ([unboxed ((unbox exp))])
      (set-box! exp (lambda () unboxed))
      unboxed)))

(define make-closure-cbv
  (lambda (x body env)
    (lambda (y)
       (val-of-cbv body (extend-env x y env)))))

(define val-of-cbv
  (lambda (exp env)
    (match exp
      [`,b #:when (boolean? b) b]
      [`,n #:when (number? n)  n]
      [`(quote ()) '()]
      [`(zero? ,n) (zero? (val-of-cbv n env))]
      [`(null? ,l) (null? (val-of-cbv l env))]
      [`(sub1 ,n) (sub1 (val-of-cbv n env))]
      [`(add1 ,n) (add1 (val-of-cbv n env))]
      [`(* ,n1 ,n2) (* (val-of-cbv n1 env) (val-of-cbv n2 env))]
      [`(if ,test ,conseq ,alt) (if (val-of-cbv test env)
                                  (val-of-cbv conseq env)
                                  (val-of-cbv alt env))]
      [`(let ((,y ,yold)) ,arg) (let ((a (val-of-cbv yold env)))
                                  (val-of-cbv arg (lambda (var) (if (eqv? var y) a
                                                                               (env var)))))]
      [`(begin2 ,e1 ,e2) (begin (val-of-cbv e1 env) (val-of-cbv e2 env))]
      [`(random ,n) (random (val-of-cbv n env))]
      [`,y #:when (symbol? y) (apply-env env y)]
      [`(set! ,x ,val)  (set! x (val-of-cbv val env))]
      [`(cons^ ,a ,d) (cons (box (lambda () (val-of-cbv a env)))
                             (box (lambda () (val-of-cbv d env))))]
      [`(car^ ,ls) (getit (car (val-of-cbv ls env)))]
      [`(cdr^ ,ls) (getit (cdr (val-of-cbv ls env)))]
      [`(cons ,a ,d) (cons (val-of-cbv a env) (val-of-cbv d env))]
      [`(car ,ls) (car (val-of-cbv ls env))]
      [`(cdr ,ls) (car (val-of-cbv ls env))]
      [`(lambda (,x) ,body) (make-closure-cbv x body env)]
      [`(,rator ,rand) (apply-closure (val-of-cbv rator env)
                                      (val-of-cbv rand env))])))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define make-closure-cbr
  (lambda (x body env)
    (lambda (y)
       (val-of-cbr body (extend-env x y env)))))

(define val-of-cbr
  (lambda (exp env)
    (match exp
      [`,b #:when (boolean? b) b]
      [`,n #:when (number? n)  n]
      [`(zero? ,n) (zero? (val-of-cbr n env))]
      [`(sub1 ,n) (sub1 (val-of-cbr n env))]
      [`(* ,n1 ,n2) (* (val-of-cbr n1 env) (val-of-cbr n2 env))]
      [`(if ,test ,conseq ,alt) (if (val-of-cbr test env)
                                  (val-of-cbr conseq env)
                                  (val-of-cbr alt env))]
      [`(begin2 ,e1 ,e2) (begin (val-of-cbr e1 env) (val-of-cbr e2 env))]
      [`(random ,n) (random (val-of-cbr n env))]
      [`,y #:when (symbol? y) (unbox (apply-env env y))]
      [`(set! ,x ,val)  (set-box! (apply-env env x) (val-of-cbr val env))]
      [`(lambda (,x) ,body) (make-closure-cbr x body env)]
      [`(,rator ,rand) #:when (symbol? rand) (apply-closure (val-of-cbr rator env)(apply-env env rand))]
      [`(,rator ,rand) (apply-closure (val-of-cbr rator env)
                                      (box (val-of-cbr rand env)))])))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define random-sieve
    '((lambda (n)
        (if (zero? n)
            (if (zero? n) (if (zero? n) (if (zero? n) (if (zero? n) (if (zero? n) (if (zero? n) #t #f) #f) #f) #f) #f) #f)
            (if (zero? n) #f (if (zero? n) #f (if (zero? n) #f (if (zero? n) #f (if (zero? n) #f (if (zero? n) #f #t))))))))
      (random 2)))

(define make-closure-cbname
  (lambda (x body env)
    (lambda (y)
       (val-of-cbname body (extend-env x y env)))))

(define val-of-cbname
  (lambda (exp env)
    (match exp
      [`,b #:when (boolean? b) b]
      [`,n #:when (number? n)  n]
      [`(zero? ,n) (zero? (val-of-cbname n env))]
      [`(sub1 ,n) (sub1 (val-of-cbname n env))]
      [`(* ,n1 ,n2) (* (val-of-cbname n1 env) (val-of-cbname n2 env))]
      [`(if ,test ,conseq ,alt) (if (val-of-cbname test env)
                                  (val-of-cbname conseq env)
                                  (val-of-cbname alt env))]
      [`(random ,n) (random (val-of-cbname n env))]
      [`,y #:when (symbol? y) ((unbox (apply-env env y)))]
      [`(lambda (,x) ,body) (make-closure-cbname x body env)]
      [`(,rator ,rand) #:when (symbol? rand) (apply-closure (val-of-cbname rator env)(apply-env env rand))]
      [`(,rator ,rand) (apply-closure (val-of-cbname rator env)
                                      (box (lambda () (val-of-cbname rand env))))])))

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define make-closure-cbneed
  (lambda (x body env)
    (lambda (y)
       (val-of-cbneed body (extend-env x y env)))))

(define val-of-cbneed
  (lambda (exp env)
    (match exp
      [`,b #:when (boolean? b) b]
      [`,n #:when (number? n)  n]
      [`(zero? ,n) (zero? (val-of-cbneed n env))]
      [`(sub1 ,n) (sub1 (val-of-cbneed n env))]
      [`(* ,n1 ,n2) (* (val-of-cbneed n1 env) (val-of-cbneed n2 env))]
      [`(if ,test ,conseq ,alt) (if (val-of-cbneed test env)
                                  (val-of-cbneed conseq env)
                                  (val-of-cbneed alt env))]
      [`(random ,n) (random (val-of-cbneed n env))]
      [`,y #:when (symbol? y) (getit (apply-env env y))]
      [`(lambda (,x) ,body) (make-closure-cbneed x body env)]
      [`(,rator ,rand) #:when (symbol? rand) (apply-closure (val-of-cbneed rator env)(apply-env env rand))]
      [`(,rator ,rand) (apply-closure (val-of-cbneed rator env)
                                      (box (lambda () (val-of-cbneed rand env))))])))

(define cons-test
    '(let ((fix (lambda (f)
                 ((lambda (x) (f (lambda (v) ((x x) v))))
                  (lambda (x) (f (lambda (v) ((x x) v))))))))
        (let ((map (fix (lambda (map)
                          (lambda (f)
                            (lambda (l)
                               (if (null? l)
                                   '()
                                   (cons^ (f (car^ l))
                                          ((map f) (cdr^ l))))))))))
          (let ((take (fix (lambda (take)
                             (lambda (l)
                               (lambda (n)
                                 (if (zero? n)
                                     '()
                                      (cons (car^ l) 
                                            ((take (cdr^ l)) (sub1 n))))))))))
            ((take ((fix (lambda (m)
                           (lambda (i)
                             (cons^ 1 ((map (lambda (x) (add1 x))) (m i)))))) 0)) 5)))))

(val-of-cbv cons-test (empty-env))