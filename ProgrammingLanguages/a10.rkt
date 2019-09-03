#lang racket
(require "mk.rkt")
(require "numbers.rkt")

;; Part I Write the answers to the following problems using your
;; knowledge of miniKanren.  For each problem, explain how miniKanren
;; arrived at the answer.  You will be graded on the quality of your
;; explanation; a full explanation will require several sentences.

;; 1 What is the value of 
;(run 2 (q)
;  (== 5 q)
;  (conde
;   [(conde 
;     [(== 5 q)
;      (== 6 q)])
;    (== 5 q)]
;   [(== q 5)]))

;(5).
;When miniKanren reads the program, the second line assigns "5" to the value 
;of "q." No matter what manipulation is attempted past that line, q will always be associated 
;with value "5" or the empty list in order to make the statement true. When the program gets 
;to the following conde statement, q is still associated with value 5, so the binding holds.
;In the other part fo that conde, these is another conde that associated 5 with q and 6 with 6.
;miniKanren ignores the 6 binding since it would make all of the above statements false.
;Thus, throughout the program q retains the value of "5"

;; 2 What is the value of
;(run 1 (q) 
;  (fresh (a b) 
;    (== `(,a ,b) q)
;    (absento 'tag q)
;    (symbolo a)))

;(((_.0 _.1) (=/= ((_.0 tag))) (sym _.0) (absento (tag _.1))))
;When miniKanren reads the program, q is immediately associated with the list (,a ,b). In
;the folowing line, a constraint is given to q's value that says that the word "tag" cannot
;by a part of the value binded to q. Finally, the program says that the variable is is a 
;symbol, and since "tag" is not part fo the list, a cannot be set to the value "tag", so =/= 
;is added as a constraint: "(=/= ((_.0 tag)))" to the final result. The final result reads as:
;q is (_.0 _.1) with _.0 not being "tag". _.0 is a symbol, and _.1 cannot have "tag" in it.

;; 3 What do the following miniKanren constraints mean?
;a: == means that the two elements that follow are the same
;b: =/= means that the two elements are not the same
;c: absento means that the following element is not a part of the element that follows. i.e:
;	(absento 'tag q) means that tag is not a part of the value stored in q
;d: numbero means that the following element is a number
;e: symbolo means that the following element is a symbol


(define assoco
  (lambda (x ls out)
    (fresh (a d aa da)
           (== `(,a . ,d) ls)
           (== `(,aa . ,da) a)
           (conde
            ((== aa x) (== a out))
            ((=/= aa x) (assoco x d out))))))

(define reverseo
  (lambda (ls out)
    (conde
     ((== '() ls) (== '() out))
     ((fresh (a d res)
            (== `(,a . ,d) ls)
            (reverseo d res)
            (appendo res `(,a) out))))))

(define stuttero
  (lambda (ls out)
    (conde
      ((== '() ls) (== '() out))
      ((fresh (a d res)
             (== `(,a . ,d) ls)
             (== `(,a ,a . ,res) out)
             (stuttero d res))))))

(define lengtho
  (lambda (ls out)
    (conde
     [(== '() ls) (== '() out)]
     [(fresh (a d res)
             (== `(,a ,d) ls)
             (lengtho d res))])))
             ;(pluso '(0) res out))]))) ;this is where my problems are happening 



(run 1 (q) (lengtho '() q))
;(())

(run 1 (q) (lengtho '(a b) q))
;((0 1))

(run 1 (q) (lengtho '(a b c) q))
;((1 1))

(run 1 (q) (lengtho '(a b c d e f g) q))
;((1 1 1))

(run 1 (q) (lengtho q (build-num 0)))
;(())
(run 1 (q) (lengtho q (build-num 5)))
;((_.0 _.1 _.2 _.3 _.4))
      