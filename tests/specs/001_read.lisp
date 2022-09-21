;; Testing read of numbers
1
;=>1
7
;=>7
  7
;=>7
-123
;=>-123


;; Testing read of symbols
+
;=>+
abc
;=>abc
   abc
;=>abc
abc5
;=>abc5
abc-def
;=>abc-def

;; Testing non-numbers starting with a dash.
-
;=>-
-abc
;=>-abc
->>
;=>->>

;; Testing read of lists
(+ 1 2)
;=>(+ 1 2)
()
;=>nil
( )
;=>nil
(nil)
;=>(nil)
((3 4))
;=>((3 4))
(+ 1 (+ 2 3))
;=>(+ 1 (+ 2 3))
  ( +   1   (+   2 3   )   )
;=>(+ 1 (+ 2 3))
(* 1 2)
;=>(* 1 2)
(** 1 2)
;=>(** 1 2)
(* -3 6)
;=>(* -3 6)
(()())
;=>(nil nil)


;>>> deferrable=True

;;
;; -------- Deferrable Functionality --------

;; Testing read of nil/true/false
t
;=>t
nil
;=>nil

;; Testing read of quoting
'1
;=>(quote 1)
'(1 2 3)
;=>(quote (1 2 3))

;; Testing keywords
:kw
;=>:kw
(:kw1 :kw2 :kw3)
;=>(:kw1 :kw2 :kw3)

;; Testing read of comments
 ;; whole line comment (not an exception)
1 ; comment after expression
;=>1
1; comment after expression
;=>1


;>>> soft=True
;>>> optional=True
;;
;; -------- Optional Functionality --------

;; Non alphanumeric characters in comments
1;!
;=>1
1;"
;=>1
1;#
;=>1
1;$
;=>1
1;%
;=>1
1;'
;=>1
1;\
;=>1
1;\\
;=>1
1;\\\
;=>1
1;`
;=>1
;;; Hopefully less problematic characters
1; &()*+,-./:;<=>?@[]^_{|}~
;=>1
