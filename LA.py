import re

class PHPLexer:
    def __init__(self, code):
        self.code = code
        self.tokens = []

    def tokenize(self):
        patterns = [
            (r'<\?php', 'START_PHP'),
            (r'\?>', 'END_PHP'),
            (r'\b(?:echo|if|else|while|for|foreach|function)\b', 'KEYWORD'),
            (r'\b(?:true|false|null)\b', 'BOOLEAN'),
            (r'\b(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)\b', 'NUMBER'),
            (r'\$\b(?:[a-zA-Z_][a-zA-Z0-9_]*)\b', 'IDENTIFIER'),  
            (r'\b(?:[a-zA-Z_][a-zA-Z0-9_]*)\b', 'IDENTIFIER'),
            (r'[-+*/%^=<>!&|]', 'OPERATOR'),
            (r'[\(\)\{\}\[\]]', 'PUNCTUATION'),
            (r'"(?:\\.|[^"\\])*"', 'STRING'),
            (r'\'(?:\\.|[^\'\\])\'', 'STRING'),
            (r'\/\/.*', 'COMMENT'),
            (r'\/\*[\s\S]*?\*\/', 'COMMENT'),
            (r'\s+', 'WHITESPACE')
        ]

        combined_patterns = '|'.join(f'({pattern})' for pattern, _ in patterns)

        lines = self.code.split('\n')

        
        indentation_level = 0

        for i, line in enumerate(lines):
            for match in re.finditer(combined_patterns, line):
                for j, (pattern, token_type) in enumerate(patterns):
                    if match.group(j + 1):
                        token_value = match.group(j + 1)

                        if token_value == '{':
                            indentation_level += 1

                        elif token_value == '}':
                            indentation_level -= 1

                        self.tokens.append((token_value, token_type, i + 1, match.start() + 1, indentation_level))
                        break

    def display_tokens(self):
        print("{:<10}  {:<15}  {:<5}  {:<7}  {:<8} ".format("Token", "Type", "Line", "Column", "Block"))
        print("=" * 70)

        for index, token in enumerate(self.tokens, start=1):
            token_value, token_type, line, column, block = token
            formatted_line = f'{line}:{column}'

            if token_value == '\n':
                formatted_value = '\\n'
            elif token_type == 'STRING':
                formatted_value = f'"{token_value}"'
            else:
                formatted_value = token_value

            print("{:<10}  {:<15}  {:<5}  {:<7}  {:<8}  ".format(
                formatted_value, token_type, line, column, block
            ))

    def write_tokens_to_file(self, output_file_path):
        with open(output_file_path, 'w') as output_file:
            output_file.write("{:<10}  {:<15}  {:<5}  {:<7}  {:<8}  \n".format(
                "Token", "Type", "Line", "Column", "Block"))
            output_file.write("=" * 70 + '\n')

            for index, token in enumerate(self.tokens, start=1):
                token_value, token_type, line, column, block = token
                formatted_line = f'{line}:{column}'

                if token_value == '\n':
                    formatted_value = '\\n'
                elif token_type == 'STRING':
                    formatted_value = f'"{token_value}"'
                else:
                    formatted_value = token_value

                output_file.write("{:<10}  {:<15}  {:<5}  {:<7}  {:<8}  \n".format(
                    formatted_value, token_type, line, column, block
                ))

# Read PHP file
file_path = 'test.php'
with open(file_path, 'r') as file:
    php_code = file.read()

lexer = PHPLexer(php_code)
lexer.tokenize()
lexer.display_tokens()

output_file_path = 'token_output.txt'
lexer.write_tokens_to_file(output_file_path)




