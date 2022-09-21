(define x 10)
;=>10

(define fn1 (lambda (x) x))
;=>(lambda (x) x)

;; Church numerals

(define c0 (lambda (f x) x))
;=>(lambda (f x) x)
(define c1 (lambda (f x) (f x)))
;=>(lambda (f x) (f x))
(define c2 (lambda (f x) (f (f x))))
;=>(lambda (f x) (f (f x)))
(define c3 (lambda (f x) (f (f (f x)))))
;=>(lambda (f x) (f (f (f x))))
(define c4 (lambda (f x) (f (f (f (f x))))))
;=>(lambda (f x) (f (f (f (f x)))))
(define c5 (lambda (f x) (f (f (f (f (f x)))))))
;=>(lambda (f x) (f (f (f (f (f x))))))

;; Church numerals to integer (to debugging)

(c0 '1+ 0)
;=>0
(c1 '1+ 0)
;=>1
(c2 '1+ 0)
;=>2
(c3 '1+ 0)
;=>3
(c4 '1+ 0)
;=>4
(c5 '1+ 0)
;=>5


;; Testing evaluation of arithmetic operations
(+ 1 2)
;=>3

(+ 5 (* 2 3))
;=>11

(- (+ 5 (* 2 3)) 3)
;=>8

(/ (- (+ 5 (* 2 3)) 3) 4)
;=>2

(/ (- (+ 515 (* 87 311)) 302) 27)
;=>1010

(* -3 6)
;=>-18

(/ (- (+ 515 (* -87 311)) 296) 27)
;=>-994

;;; This should throw an error with no return value
(abc 1 2 3)
;/.+

;; Testing empty list
()
;=>()

;>>> deferrable=True
;;
;; -------- Deferrable Functionality --------

;; Testing evaluation within collection literals
[1 2 (+ 1 2)]
;=>[1 2 3]

{"a" (+ 7 8)}
;=>{"a" 15}

{:a (+ 7 8)}
;=>{:a 15}

;; Check that evaluation hasn't broken empty collections
[]
;=>[]
{}
;=>{}
