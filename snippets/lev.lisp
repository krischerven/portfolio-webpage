;; NOTE: The following snippet is derived from a Common Lisp codebase. The dependencies needed to
;; compile this snippet are contained in the second section. You also need SBCL (https://www.sbcl.org/)
;; ----------------------------------------------------------------------------------------------------
;;
;; lev (let-value) is a macro for introducing immutable bindings.
;; It is syntactically identical to (let).
;;
;; Compare:
;;
;; (let ((x 1))
;;   (setq x 0) ;; fine
;;   (print x))
;;
;; (lev ((x 1))
;;   (setq x 0) ;; compile error
;;   x)
;;
;; (lev ((x 1))
;;   (lev ((x 0))
;;     ;; Fine - x is 0 here
;;     (print x))
;;   ;; x is 1 again
;;   (print x))
;;
(defmacro lev (bindings &body forms)
  `(progn
     (lev-compiler "lev" ,bindings ,@forms)
     (let ,bindings ,@forms)))

;; (lev*) is to (lev) as (let*) is to (let).
(defmacro lev* (bindings &body forms)
  `(progn
     (lev-compiler "lev*" ,bindings ,@forms)
     (let* ,bindings ,@forms)))

;; NOTE: The following lists are dynamically created throughout a real codebase using a special macro.
;; They are incomplete in this snippet.

;; Forbid (setf CONST VALUE) etc
(defvar .lev-forbidden-car-parameters
  (list 'setf 'setq 'incf 'decf 'nreverse 'close 'sb-thread:signal-semaphore 'extend))

;; Forbid (push VALUE CONST) etc
(defvar .lev-forbidden-cadr-parameters (list 'push 'delete 'delete-if 'edelete))

;; Forbid (lev ((CONST (POINTER))) ...) etc
(defvar .lev-inherently-mutable-cars (list 'pointer))

;; Forbid (setf (nth* N CONST) ...),
;;        (push VALUE (nth* N CONST))
;;
;; where nth* is any number of nested nth forms
;; NOTE: only forbidden when used with .lev-forbidden-ca(d)r-parameters
(defvar .lev-forbidden-recursive-cadr-forms (list 'car 'cdr 'nth 'symbol-value 'gethash))

(defmacro lev-compiler (name bindings &body forms)
  `(progn

     ;; Returns the relevant symbol of a form (ie x from (nth 0 x))
     ,@(labels ((basic-form (form)
                  (declare (type (or symbol cons sb-comma) form))
                  ;; Define a global parameter *basic-forms*, and the possible types can be tested like such:
                  ;; [NOTE that *basic-forms* may not be pushed to unless (wipe-REDACTED-cache) is run first.]
                  ;; (push (type-of form) *basic-forms*)
                  ;; (remove-if (lambda (x) (or (symbolp x) (consp x) (sb-int:comma-p x))) *basic-forms*)
                  (if (and
                       (listp form)
                       (find (car form) .lev-forbidden-recursive-cadr-forms))
                      (basic-form (lastcar form))
                      form))

                (prohibit-rebindings (branch forbidden-rebindings allowed-rebindings)
                  (declare (type list branch)) ;; Note that the initial branch for an empty (lev ((...))) is nil.
                  (declare (type cons forbidden-rebindings))
                  (declare (type elist allowed-rebindings))
                  (let ((last-twig nil))
                    (mapcar (lambda (twig)
                              (cond ((listp twig)
                                     (cond
                                       ;; (let ((...)) a b c ...)
                                       ;;  ^last ^current ^next twigs
                                       ((eql last-twig 'let)
                                        (when (list-of-lists-p twig)
                                          ;; 1) New elist for this (let ...) - otherwise, these new bindings
                                          ;; are allowed for everything that is evaluated after this point,
                                          ;; regardless of scope.
                                          (setq allowed-rebindings (copy-elist allowed-rebindings))
                                          (dolist (binding twig)
                                            (let ((symbol (car binding)))
                                              (extend allowed-rebindings symbol))))
                                        ;; Must be (), (x), ((x)), ((x) (y))
                                        ;; This prevents (let ((y (setq x 4))) ...) etc
                                        (prohibit-rebindings twig forbidden-rebindings allowed-rebindings))
                                       ;; (incf <binding>), (setf <binding> <val>), etc
                                       ((find (car twig) .lev-forbidden-car-parameters)
                                        (let ((basic-form (basic-form (second twig))))
                                          (when (and
                                                 (not (efind basic-form allowed-rebindings))
                                                 (find-one basic-form forbidden-rebindings))
                                            (error "Modification of binding in (~A) via (~A): form is ~A"
                                                   name (car twig) twig))))
                                       ;; (push <val> <binding>), etc
                                       ((find (car twig) .lev-forbidden-cadr-parameters)
                                        (let ((basic-form (basic-form (third twig))))
                                          (when (and
                                                 (not (efind basic-form allowed-rebindings))
                                                 (find-one basic-form forbidden-rebindings))
                                            (error "Modification of binding in (~A) via (~A): form is ~A"
                                                   name (car twig) twig))))
                                       (t (prohibit-rebindings twig forbidden-rebindings allowed-rebindings))))
                                    ;; For ,symbol ,(1 2 3) etc
                                    ((sb-int:comma-p twig)
                                     (let ((expr (sb-int:comma-expr twig)))
                                       (if (listp expr)
                                           (prohibit-rebindings expr forbidden-rebindings allowed-rebindings)
                                           twig)))
                                    (t twig))
                              (setq last-twig twig))
                            branch)))

                ;; We prohibit (lev ((x (pointer))) ...) because pointers are meant to be assigned at runtime
                ;; in a way that is not cost-effective to prevent. You can still write (lev ((x (list))) ...)
                ;; and do the same thing, which is an inherent limitation of this macro.
                (prohibit-inherently-mutables (binding-values)
                  ;; (let nil) is valid (and returns nil), so (lev nil) is also valid
                  (declare (type list binding-values))
                  ;; eg '(pointer X)
                  (dolist (value binding-values)
                    (when (listp value)
                      ;; eg 'pointer
                      (when (find (car value) .lev-inherently-mutable-cars)
                        (error "Attempting to run inherently-mutable form ~A in (~A) form." value name))))))

         (returning-nil
          ;; Since (let (x y z) ...) is valid, we need to remove plain symbols first
          (prohibit-inherently-mutables (mapcar (lambda (x) (cadr x)) (remove-if-not #'listp `,bindings))))

         (returning-nil
          ;; Avoid a lot of work for forms like (lev nil 1 2 3 ...) [which is identical to (lev () 1 2 3 ...)]
          (when `,bindings
            (prohibit-rebindings (copy-tree `,forms) (nil-or-xs/cars `,bindings) (elist)))))))