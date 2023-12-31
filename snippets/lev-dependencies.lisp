;; Assorted dependencies required to compile the previous code snippet.
;; This file will only be of interest to you if you want to test the lev/lev* macro.
;; Simply evaluate this file first, then lev.lisp second. Only SBCL is supported.
;; ---------------------------------------------------------------------------------
;;
(eval-when (:compile-toplevel :load-toplevel :execute)
  (defun returning-nil (x)
    (declare (ignore x))
    nil)

  (defun find-one (needle haystack &key (test #'eql))
    (dolist (needle-2 haystack)
      (when (funcall test needle needle-2)
        (return-from find-one t)))))

(deftype sb-comma ()
  `(satisfies sb-int:comma-p))

(defun nil-or-xs/cars (x)
  (cond ((null x) nil)
        ((listp x) (mapcar #'(lambda (x) (if (listp x) (car x) x)) x))
        (t (error "'~A' is of type ~A, not (or null list)" x (type-of x)))))

(defun t-p (thing)
  (declare (ignore thing))
  t)

(defun copy-array (array &key (element-type (array-element-type array))
                              (fill-pointer (and (array-has-fill-pointer-p array)
                                                 (fill-pointer array)))
                              (adjustable (adjustable-array-p array)))
  "Returns an undisplaced copy of ARRAY, with same fill-pointer and
adjustability (if any) as the original, unless overridden by the keyword
arguments."
 (let* ((dimensions (array-dimensions array))
        (new-array (make-array dimensions
                               :element-type element-type
                               :adjustable adjustable
                               :fill-pointer fill-pointer)))
   (dotimes (i (array-total-size array))
     (setf (row-major-aref new-array i)
           (row-major-aref array i)))
   new-array))

(eval-when (:compile-toplevel :load-toplevel :execute)
  (defstruct elist
    (:sequence nil :type (vector t))
    ;; A field named 'type' is a probable syntax error and halts comp
    (:typef #'t-p :type function)))

(defun elist (&rest initial-contents)
  (declare (dynamic-extent initial-contents))
  (make-elist :sequence
              (make-array (length initial-contents)
                          :adjustable t
                          :fill-pointer (length initial-contents)
                          :element-type t
                          :initial-contents initial-contents)))

(let ((sb-ext:*muffled-warnings* 'sb-int:duplicate-definition))
  (fmakunbound 'copy-elist)
  (defun copy-elist (elist)
    (declare (type elist elist))
    (make-elist :sequence (copy-array (elist-sequence elist))
                :typef (elist-typef elist))))

(defun extend (elist element)
  (declare (type elist elist))
  (assert (funcall (elist-typef elist) element))
  (vector-push-extend element (elist-sequence elist))
  elist)

(defun efind (item elist &key (test #'eql))
  (declare (type elist elist))
  (find item (elist-sequence elist) :test test))

(defun lastcar (list)
  (car (last list)))

(defun empty? (list)
  (eql (length list) 0))

(defun full? (list)
  (not (empty? list)))

(defun list-of-lists-p (x)
  (and (listp x)
       (full? x)
       (every #'consp x)))

(deftype list-of-lists ()
  `(satisfies list-of-lists-p))

(defun pointer (&optional to)
  (list to))