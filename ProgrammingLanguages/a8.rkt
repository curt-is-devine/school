#lang racket

(define n* '())
(define k* '())
(define m* '())
(define v* '())
(define ls* '())
(define a* '())
(define pc* '())
(define done* #f)

(define empty-k
 (lambda ()
    `(empty-k)))

(define apply-k-ack
  (lambda ()
    (match k*
      [`(inner-k-ack ,m ,k) (begin 
                          (set! m* (sub1 m))
                          (set! n* v*)
                          (set! k* k)
                          (ack))]
      [`(empty-k) v*])))         

(define inner-k-ack 
  (lambda (m k)
    `(inner-k-ack ,m ,k)))

(define ack
  (lambda ()
    (cond
      [(zero? m*) (begin
                    (set! v* (add1 n*))
                    (apply-k-ack))]
      [(zero? n*) (begin 
                    (set! m* (sub1 m*))
                    (set! n* 1)
                   (ack))]
      [else (begin 
              (set! k* (inner-k-ack m* k*))
              (set! n* (sub1 n*))
              (ack))])))

(define ack-reg-driver
  (lambda (m n)
    (begin
      (set! m* m)
      (set! n* n)
      (set! k* (empty-k))
      (ack))))
;----------------------------------------------------------------------------------------
(define apply-k-depth
  (lambda ()
    (match k*
      [`(outer-k-depth ,ls ,k) (begin 
                                 (set! ls* (cdr ls))
                                 (set! k* (inner-k-depth v* k))
                                 (depth))]
      [`(inner-k-depth ,v^ ,k) (let ((v^ (add1 v^)))
                                  (if (< v^ v*)
                                      (begin 
                                        (set! k* k)
                                        (apply-k-depth))
                                      (begin 
                                        (set! k* k)
                                        (set! v* v^)
                                        (apply-k-depth))))]
      [`(empty-k) v*])))

(define outer-k-depth 
  (lambda (ls^ k^)
    `(outer-k-depth ,ls^ ,k^)))

(define inner-k-depth 
  (lambda (v^ k^)
    `(inner-k-depth ,v^ ,k^)))

(define depth
  (lambda ()
    (cond
      [(null? ls*) (begin 
                     (set! v* 1)
                     (apply-k-depth))]
      [(pair? (car ls*)) (begin 
                           (set! k* (outer-k-depth ls* k*))
                           (set! ls* (car ls*))
                           (depth))]
      [else (begin 
              (set! ls* (cdr ls*))
              (depth))])))

(define depth-reg-driver
  (lambda (ls)
    (begin
      (set! ls* ls)
      (set! k* (empty-k))
      (depth))))
;---------------------------------------------------------------------------------------
(define apply-k-fact
  (lambda ()
    (match k*
      [`(inner-k-fact ,n^ ,k^) (begin 
                                 (set! v* (* n^ v*))
                                 (set! k* k^)
                                 (apply-k-fact))]
      [`(empty-k) v*])))

(define inner-k-fact
  (lambda (n^ k^)
     `(inner-k-fact ,n^ ,k^)))

(define fact
  (lambda ()
    ((lambda (fact)
       (fact fact))
     (lambda (fact)
       (cond
         [(zero? n*) (begin 
                       (set! v* 1)
                       (apply-k-fact))]
         [else (begin 
                 (set! k* (inner-k-fact n* k*))
                 (set! n* (sub1 n*))
                 (fact fact))])))))

(define fact-reg-driver
  (lambda (n)
    (begin
      (set! n* n)
      (set! k* (empty-k))
      (fact))))
;---------------------------------------------------------------------------------------
(define apply-k-pascal
  (lambda ()
    (match k*
      [`(empty-k) v*]
      [`(outer-k-pascal ,k) (begin
                              (set! k* k)
                              (v* 1 0))]
      [`(in-let-k-pascal ,a ,k) (begin 
                                  (set! k* k)
                                  (set! v* (cons a v*))
                                  (apply-k-pascal))]
      [`(out-let-k-pascal ,m ,a ,k) (begin
                                      (set! k* (in-let-k-pascal a k))
                                      (v* (add1 m) a))])))
  
(define outer-k-pascal
  (lambda (k)
    `(outer-k-pascal ,k)))

(define in-let-k-pascal
  (lambda (a k)
    `(in-let-k-pascal ,a ,k)))

(define out-let-k-pascal
  (lambda (m a k)
    `(out-let-k-pascal ,m ,a ,k)))
    
(define pascal
  (lambda ()
    (let ((pascal (lambda (pascal)
                    (begin
                      (set! v* (lambda (m a)
                                        (cond
                                          [(> m n*) (begin
                                                      (set! v* '())
                                                      (apply-k-pascal))]
                                          [else (let ((a (+ a m)))
                                                  (begin
                                                    (set! k* (out-let-k-pascal m a k*))
                                                    (pascal pascal)))])))
                      (apply-k-pascal)))))
      (begin
        (set! k* (outer-k-pascal k*))
        (pascal pascal)))))

(define pascal-reg-driver
  (lambda (n)
    (begin
      (set! n* n)
      (set! k* (empty-k))
      (pascal))))
;---------------------------------------------------------------------------------------
(define apply-k-fib
  (lambda ()
    (match k*
      [`(inner-k-fib ,o ,k) (begin 
                              (set! k* k)
                              (set! v* (+ o v*))
                              (set! pc* apply-k-fib))]
      [`(outer-k-fib ,n ,k) (begin 
                              (set! n* (sub1 (sub1 n)))
                              (set! k* (inner-k-fib v* k))
                              (set! pc* fib-cps))]
      [`(empty-k) (set! done* #t)])))

(define inner-k-fib
  (lambda (o k)
    `(inner-k-fib ,o ,k)))

(define outer-k-fib
  (lambda (n k)
    `(outer-k-fib ,n ,k)))

(define trampoline
  (lambda ()
    (if done*
        v*
        (begin
          (pc*) (trampoline)))))

(define rampoline
  (lambda (th1 th2 th3)
    (or (th1) (th2) (th3))))

(define fib
  (lambda (n k)
    (begin
      (set! n* n)
      (set! k* k)
      (set! done* #f)
      (set! pc* fib-cps)
      (trampoline))))

(define fib-cps
  (lambda ()
    (cond
      [(and (not (negative? n*)) (< n* 2)) (begin
                                             (set! v* n*)
                                             (set! pc* apply-k-fib))] 
      [else (begin 
              (set! k* (outer-k-fib n* k*))
              (set! n* (sub1 n*))
              (set! pc* fib-cps))])))

;(define fib-ramp-driver
;  (lambda (n1 n2 n3)
;    (let/cc jumpout
;      (rampoline
;        (lambda ()
;          (fib n1 (ramp-empty-k jumpout)))
;        (lambda ()
;          (fib n2 (ramp-empty-k jumpout)))
;        (lambda ()
;          (fib n3 (ramp-empty-k jumpout)))))))

