(define x 10)
;=>10

(define fn1 (lambda (x) x))
;=>(lambda (x) x)

;; Church numerals

(define zero (lambda (_f) (lambda (x) x)))
;=>(lambda (_f) (lambda (x) x))
(define one (lambda (f) (lambda (x) (f x))))
;=>(lambda (f) (lambda (x) (f x)))
(define two (lambda (f) (lambda (x) (f (f x)))))
;=>(lambda (f) (lambda (x) (f (f x))))
(define three (lambda (f) (lambda (x) (f (f (f x))))))
;=>(lambda (f) (lambda (x) (f (f (f x)))))
(define four (lambda (f) (lambda (x) (f (f (f (f x)))))))
;=>(lambda (f) (lambda (x) (f (f (f (f x))))))
(define five (lambda (f) (lambda (x) (f (f (f (f (f x))))))))
;=>(lambda (f) (lambda (x) (f (f (f (f (f x)))))))


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
