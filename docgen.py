import os
import ast
import hashlib
import astunparse
from openai import OpenAI

example_md = """
## load_callbacks_and_logger
```python
def load_callbacks_and_logger(args):
    checkpoint_callback = ModelCheckpoint(
        dirpath=args.output_dir,
        filename="model-{epoch:02d}-{step}",
        every_n_train_steps=args.save_steps,
        save_top_k=-1,
        save_weights_only=True,
        save_on_train_epoch_end=False,
    )
    lr_monitor = LearningRateMonitor(logging_interval="step")
    logger = WandbLogger(name=args.exp_name, log_model=False)
    return [checkpoint_callback, lr_monitor], logger
```

**Improvements:**
- Change `save_top_k=-1` to `save_weights_only=True` in the `ModelCheckpoint` to only save the model weights.
- None Found

**Errors:**
- None Found

**Vulnerabilities:**
- None Found

"""


class FileParser(ast.NodeVisitor):
    def __init__(self):
        self.parsed_content = []

    def visit_ClassDef(self, node):
        class_str = ""
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                class_str += astunparse.unparse(item)
            elif isinstance(item, ast.AnnAssign):
                class_str += astunparse.unparse(item)
        self.parsed_content.append((node.name, class_str))

    def visit_FunctionDef(self, node):
        if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(node)):
            self.parsed_content.append(astunparse.unparse(node))

    def generic_visit(self, node):
        super().generic_visit(node)

class Loader:

    def __init__(self, api_key, content) -> None:
        self.content = content
        # openai.api_key = api_key
        self.client = OpenAI(api_key=api_key)
    
    def get_response_doc(self):
        class_methods_extractor = FileParser()

        tree = ast.parse(self.content)

        class_methods_extractor.visit(tree)
        docu = ''
        for block in class_methods_extractor.parsed_content:
            res = explain_function(self.client, block)
            docu += block + '\n'
            docu += res + '\n'
        
        full_docu = generate_doc(self.client, docu)

        return full_docu
    
    def get_response_update(self):
        class_methods_extractor = FileParser()

        tree = ast.parse(self.content)

        class_methods_extractor.visit(tree)
        docu = ''
        for block in class_methods_extractor.parsed_content:
            res = upgrade_function(self.client, block)
            docu += res + '\n'

        return docu

def write_response(dir:str, content:str, response:str):
    hash_value = hashlib.md5(content.encode()).hexdigest()

    file_name = hash_value + ".md"

    with open(os.path.join(dir, file_name), "w") as file:
        file.write(response)


def explain_function(client, func:str):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "text" },
    messages=[
        {"role": "system", "content": "You are a developer that has to write documentation for his code in Markdown. Explain the given function or class and give one usage example."},
        {"role": "user", "content": f"Explain this function: {func}"}
    ]
    )
    return response.choices[0].message.content

def generate_doc(client, doc:str):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "text" },
    messages=[
        {"role": "system", "content": """You are a developer that has to write documentation for his code in Markdown.
         Given the documented functions, generate a complete documentation page for the project.
         Start with a introduction of the project and a summarization of the code."""},
        {"role": "user", "content": f"The documented functions are: {doc}"}
    ]
    )
    return response.choices[0].message.content

def upgrade_function(client, func:str):
    response = client.chat.completions.create(
    model="gpt-3.5-turbo-0125",
    response_format={ "type": "text" },
    temperature=0.0,
    messages=[
        {"role": "system", "content": "You are a developer that has to improve a given function or class and find possible errors or exploits. Rewrite the given code and return a markdown with the code and 3 lists: improvements, errors, vulnerabilities. The title is the function or class name If there any of the lists is empty, display the text None Found. Do not add or consider imports an error or improvement."},
        {"role": "system", "content": "Use the following structure" + example_md},
        {"role": "user", "content": f"Fix this function: {func}"}
    ]
    )
    return response.choices[0].message.content