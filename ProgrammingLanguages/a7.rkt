#lang racket
(require racket/trace)
(define last-non-zero
  (lambda (ls)
    (let/cc k
      (letrec
	((last-non-zero
	   (lambda (ls)
	     (cond
	       [(null? ls) '()]
               [(zero? (car ls)) (k (last-non-zero (cdr ls)))]
               [else (cons (car ls) (last-non-zero (cdr ls)))]
  	       ))))
	(last-non-zero ls)))))

(define walk-symbol
  (lambda (x s)
    (cond
      [(and (assv x s) (symbol? (cdr (assv x s)))) (walk-symbol (cdr (assv x s)) s)]
      [(assv x s) (cdr (assv x s))]
      [else x])))

(define lex
  (lambda (e acc)
    (match e
      [`,y #:when (number? y) (list 'const y)]
      [`,y #:when (symbol? y) (cons 'var
                                    (walk-symbol y acc))]
      [`(zero? ,nexp)         `(zero ,(lex nexp acc))]
      [`(* ,nexp1 ,nexp2)     `(mult ,(lex nexp1 acc) ,(lex nexp2 acc))]
      [`(sub1 ,x)             (cons 'sub1 (list (lex x acc)))]
      ;still lost on what throw and let/cc do in general
      [`(throw ,k-exp ,v-exp) (list 'throw (lex k-exp acc) (lex v-exp acc))]
      [`(letcc ,body)         (list 'letcc body)] 
      [`(lambda (,x) ,body)   (list 'lambda
                                    (lex body (map (lambda (duo) (if (eqv? (car duo) x) duo
                                                                                        (list (car duo) (add1 (car (cdr duo))))))
                                                   (cons (list x 0) acc))))]
      [`(if ,cond ,tru ,fal)  (cons 'if (list (lex cond acc) (lex tru acc) (lex fal acc)))]
      [`(let ((,y ,exp)) ,body) (list 'let (lex exp acc) (lex body (map (lambda (duo) (if (eqv? (car duo) y) duo
                                                                                        (list (car duo) (add1 (car (cdr duo))))))
                                                   (cons (list y 0) acc))))]
      [`(,rator ,rand)        `(app ,(lex rator acc) ,(lex rand acc))])))

(define value-of
  (lambda (expr env)
    (match expr
      [`(const ,expr) expr]
      [`(mult ,x1 ,x2) (* (value-of x1 env) (value-of x2 env))]
      [`(sub1 ,x) (sub1 (value-of x env))]
      [`(zero ,x) (zero? (value-of x env))]
      [`(if ,test ,conseq ,alt) (if (value-of test env)
                                    (value-of conseq env)
                                    (value-of alt env))]
      [`(letcc ,body) (let/cc k
                         (value-of body (lambda (y) (if (zero? y) k (env (sub1 y))))))]
      [`(throw ,k-exp ,v-exp) ((value-of k-exp env) (value-of v-exp env))]
      [`(let ,e ,body) (let ((a (value-of e env)))
                         (value-of body (lambda (y) (if (zero? y) a (env (sub1 y))))))]
      [`(var ,expr) (env expr)]
      [`(lambda ,body) (lambda (a) (value-of body (lambda (y) (if (zero? y) a (env (sub1 y))))))]
      [`(app ,rator ,rand) ((value-of rator env) (value-of rand env))])))
 
(define empty-env
  (lambda ()
    (lambda (y)
      (error 'value-of "unbound identifier"))))
 
(define empty-k
  (lambda ()
    (lambda (v)
      v)))

(define value-of-cps
  (lambda (expr env k)
    (match expr
      [`(const ,expr) (k expr)]
      [`(mult ,x1 ,x2) (value-of-cps x1 env (lambda (x1) (k (value-of-cps x2 env (lambda (x2) (k (* x1 x2)))))))]
      [`(sub1 ,x) (value-of-cps x env (lambda (x) (k (sub1 x))))]
      [`(zero ,x) (value-of-cps x env (lambda (x) (k (zero? x))))]
      [`(if ,test ,conseq ,alt) (value-of-cps test env (lambda (test) (if test (value-of-cps conseq env k)
                                                                          (value-of-cps alt env k))))]
      ;[`(letcc ,body) (let/cc k
      ;                   (value-of body (lambda (y) (if (zero? y) k (env (sub1 y))))))]
      ;[`(throw ,k-exp ,v-exp) ((value-of k-exp env) (value-of v-exp env))]
      ;[`(let ,e ,body) (let ((a (value-of e env)))
      ;                   (value-of body (lambda (y) (if (zero? y) a (env (sub1 y))))))]
      [`(var ,expr) (env expr k)]
      ;I dont understand why these two lines are not working. I thought I was doing this right?
      [`(lambda ,body) (k (lambda (a k) (value-of-cps body (k (lambda (y k) (if (zero? y) (k a) (env (sub1 y) k)))) k)))]
      [`(app ,rator ,rand) (value-of-cps rator env (lambda (t) value-of-cps rand env (lambda (n) (t n k))))])))

(define empty-env-fn
  (lambda ()
    (lambda (y) (error 'value-of "unbound variable ~s" y))))

(value-of (lex '(lambda (x) (zero? 5)) '()) empty-env-fn (empty-k))
(value-of-cps (lex '((lambda (x) x) 5) '()) empty-env-fn (empty-k)) 
;why is this lower one returning procedure? From what I can tell, the lex version is fine, so is value-of wrong?
(value-of (lex '(lambda (!)
  	  (lambda (n)
  	    (if (zero? n) 1 (* n (! (sub1 n))))))
	'()) empty-env-fn)

(value-of (lex '(let ((! (lambda (!)
  		   (lambda (n)
  		     (if (zero? n) 1 (* n ((! !) (sub1 n))))))))
          ((! !) 5))
       '()) empty-env-fn)