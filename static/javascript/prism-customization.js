// default
Prism.languages.lisp.defvar.pattern = /(\()def(?:const|custom|group|var)\s+(?!\d)[-+*/~!@$%^=<>{}\w]+/

// custom (highlight the word; FIXME fails to highlight the dot)
Prism.languages.lisp.defvar.pattern = /(\()def(?:const|custom|group|var|type)\s+(?!\d)([.]?)[-+*/~!@$%^=<>{}\w]+/

// default
Prism.languages.lisp.keyword[0].pattern = /(\()(?:and|(?:cl-)?letf|cl-loop|cond|cons|error|if|(?:lexical-)?let\*?|message|not|null|or|provide|require|setq|unless|use-package|when|while)(?=\s)/

// custom (highlights progn, labels, returning-nil, dolist, eval-when, dotimes, flet (the last two for futureproofing))
Prism.languages.lisp.keyword[0].pattern = /(\()(?:and|(?:cl-)?letf|cl-loop|cond|cons|error|if|(?:lexical-)?let\*?|message|not|null|or|provide|require|setq|unless|use-package|when|while|progn|labels|returning-nil|dolist|eval-when|dotimes|flet)(?=\s)/

// Note the existence of Prism.languages.lisp.keyword[1].pattern