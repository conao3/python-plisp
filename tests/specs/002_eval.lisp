(define x 10)
;=>10

(define fn1 (lambda (x) x))
;=>(lambda (x) x)

(fn1 10)
;=>10

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

;; Church numerals to concrete value

(c0 (lambda (x) (cons 'a x)) nil)
;=>nil
(c1 (lambda (x) (cons 'a x)) nil)
;=>(a)
(c2 (lambda (x) (cons 'a x)) nil)
;=>(a a)
(c3 (lambda (x) (cons 'a x)) nil)
;=>(a a a)
(c4 (lambda (x) (cons 'a x)) nil)
;=>(a a a a)
(c5 (lambda (x) (cons 'a x)) nil)
;=>(a a a a a)

;; Church numerals to concrete value (using function)

(define cval (lambda (c) (c (lambda (x) (cons 'a x)) nil)))
;=>(lambda (c) (c (lambda (x) (cons 'a x)) nil))

(cval c0)
;=>nil
(cval c1)
;=>(a)
(cval c2)
;=>(a a)
(cval c3)
;=>(a a a)
(cval c4)
;=>(a a a a)
(cval c5)
;=>(a a a a a)

;; Testing evaluation of arithmetic operations

(define cadd (lambda (c_a c_b) (lambda (f x) (c_a f (c_b f x)))))
;=>(lambda (c_a c_b) (lambda (f x) (c_a f (c_b f x))))

(cadd c2 c3)
;=>(lambda (f x) (c_a f (c_b f x)))

(cval (cadd c2 c3))
;=>(a a a a a)

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
