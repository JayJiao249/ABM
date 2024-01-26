from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import QRegularExpression


#### System Code editor #####


class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)

        # Define the format for each type
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("darkCyan"))

        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("green"))

        string_format = QTextCharFormat()
        string_format.setForeground(QColor("red"))

        function_format = QTextCharFormat()
        function_format.setForeground(QColor("magenta"))

        class_format = QTextCharFormat()
        class_format.setForeground(QColor("darkmagenta"))

        number_format = QTextCharFormat()
        number_format.setForeground(QColor("darkcyan"))

        multiline_comment_format = QTextCharFormat()
        multiline_comment_format.setForeground(QColor("gray"))

        # Create a list of highlighting rules
        self.highlighting_rules = []

        # Keywords rule
        keywords = ["and", "as", "assert", "async", "await", "break", "class", "continue", "def", "del", "elif",
                    "else", "except", "False", "finally", "for", "from", "global", "if", "import", "in", "is",
                    "lambda", "None", "nonlocal", "not", "or", "pass", "raise", "return", "True", "try", "while",
                    "with", "yield"]
        for keyword in keywords:
            pattern = QRegularExpression(r"\b" + keyword + r"\b")
            self.highlighting_rules.append((pattern, keyword_format))

        # Comments rule
        self.highlighting_rules.append((QRegularExpression(r"#[^\n]*"), comment_format))

        # String rules
        self.highlighting_rules.append((QRegularExpression(r'".*"'), string_format))
        self.highlighting_rules.append((QRegularExpression(r"'.*'"), string_format))

        # Function names rule
        self.highlighting_rules.append((QRegularExpression(r'\b[A-Za-z0-9_]+(?=\()'), function_format))

        # Class names rule
        self.highlighting_rules.append((QRegularExpression(r'\bclass\b\s*[A-Za-z0-9_]+'), class_format))

        # Numerical highlighting rule
        self.highlighting_rules.append((QRegularExpression(r'\b\d+\b|\b0[xX][a-fA-F0-9]+\b'), number_format))

        # Multiline comment (docstring) highlighting rule
        self.multiline_comment_format = multiline_comment_format
        self.start_expression = QRegularExpression(r'"""|\'\'\'')
        self.end_expression = QRegularExpression(r'"""|\'\'\'')
    

    def highlightBlock(self, text):
        # Existing single-line highlight rules
        for pattern, format in self.highlighting_rules:
            iterator = pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
        
        # Multi-line comment (docstring) highlighting
        start_expression = self.start_expression
        end_expression = self.end_expression
        
        # Check for a multiline comment start without an end
        startIndex = start_expression.match(text).capturedStart()
        if startIndex >= 0:
            endIndex = end_expression.match(text).capturedStart()
            length = len(text) - startIndex
            if endIndex == -1:
                self.setCurrentBlockState(1)
            else:
                length = endIndex - startIndex + end_expression.match(text, startIndex).capturedLength()
            self.setFormat(startIndex, length, self.multiline_comment_format)
        
        # In a multi-line comment block
        while startIndex >= 0:
            endIndex = end_expression.match(text, startIndex).capturedStart()
            if endIndex == -1:
                self.setCurrentBlockState(1)
                length = len(text) - startIndex
            else:
                length = endIndex - startIndex + end_expression.match(text, startIndex).capturedLength()
            self.setFormat(startIndex, length, self.multiline_comment_format)
            startIndex = start_expression.match(text, startIndex + length).capturedStart()
        
        # Function and class names highlighting
        function_format = QTextCharFormat()
        function_format.setForeground(QColor("magenta"))
        function_pattern = QRegularExpression(r'\b[A-Za-z0-9_]+(?=\()')
        iterator = function_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), function_format)

        class_format = QTextCharFormat()
        class_format.setForeground(QColor("darkmagenta"))
        class_pattern = QRegularExpression(r'\bclass\b\s*[A-Za-z0-9_]+')
        iterator = class_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), class_format)

        # Numerical highlighting
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("darkcyan"))
        number_pattern = QRegularExpression(r'\b\d+\b|\b0[xX][a-fA-F0-9]+\b')
        iterator = number_pattern.globalMatch(text)
        while iterator.hasNext():
            match = iterator.next()
            self.setFormat(match.capturedStart(), match.capturedLength(), number_format)
