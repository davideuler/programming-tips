# Elegant DSPy

## 1.Implement a Translator feature in 9 lines code (by Declarative Module)

``` python
import dspy
import argparse
import os

api_key, api_base = os.getenv("OPENAI_API_KEY"), os.getenv("OPENAI_API_BASE") or "https://api.openai.com/v1"

if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set.")

# Configure the LLM using dspy.LM
llm = dspy.LM(model="openai/gpt-4o-mini", api_key=api_key, api_base=api_base)
dspy.settings.configure(lm=llm)

def translate(source_text:str, source_language:str = "Unspecified", target_language:str = "English"):
    translator = dspy.Predict('source_text, source_language, target_language -> translated_text')

    result = translator(source_text=source_text, source_language=source_language, target_language=target_language)
    return result.translated_text
```

The calling function

``` python
def main():
    parser = argparse.ArgumentParser(
        description="Translate text using DSPy and an OpenAI-compatible LLM API. Requires OPENAI_API_KEY and OPENAI_API_BASE environment variables."
    )
    parser.add_argument("source_text", help="The text to translate.")
    parser.add_argument("--source_lang", default="Unspecified", help="Source language (default: Unspecified).")
    parser.add_argument("--target_lang", default="English", help="Target language (default: English).")

    args = parser.parse_args()

    try:

        # Call the translate function
        translated_output = translate(
            source_text=args.source_text,
            source_language=args.source_lang,
            target_language=args.target_lang
        )

        print(f"Source ({args.source_lang}): {args.source_text}")
        print(f"Translation ({args.target_lang}): {translated_output}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure OPENAI_API_KEY and OPENAI_API_BASE environment variables are set correctly.")
    except Exception as e: # Catch potential dspy/API errors
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
```

## 2.Implement a Translator feature by dspy Structural Signatures

```
import dspy
import argparse
import os

class TranslationSignature(dspy.Signature):
    """Translate text from source language to target language."""
    source_language = dspy.InputField(desc="The language of the input text.")
    target_language = dspy.InputField(desc="The desired language for the translation.")
    source_text = dspy.InputField(desc="The text to be translated.")
    translated_text = dspy.OutputField(desc="The translated text.")

class Translator:
    def __init__(self, model="openai/gpt-4o-mini"):
        """Initializes the Translator with a specified OpenAI-compatible model.
           Requires OPENAI_API_KEY and OPENAI_API_BASE environment variables to be set.
        """
        api_key = os.getenv("OPENAI_API_KEY")
        api_base = os.getenv("OPENAI_API_BASE")

        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set.")
        if not api_base:
            raise ValueError("OPENAI_API_BASE environment variable not set.")

        # Configure the LLM using dspy.LM
        llm = dspy.LM(model=model, api_key=api_key, api_base=api_base)
        dspy.settings.configure(lm=llm)
        # Define the translation module using the renamed signature
        self.translator = dspy.Predict(TranslationSignature)

    def translate(self, source_text, source_language, target_language):
        """Translates the source text from the source language to the target language."""
        result = self.translator(
            source_language=source_language,
            target_language=target_language,
            source_text=source_text
        )
        return result.translated_text

def main():
    parser = argparse.ArgumentParser(
        description="Translate text using DSPy and an OpenAI-compatible LLM API. Requires OPENAI_API_KEY and OPENAI_API_BASE environment variables."
    )
    parser.add_argument("source_text", help="The text to translate.")
    parser.add_argument("--source_lang", default="Unspecified", help="Source language (default: Unspecified).")
    parser.add_argument("--target_lang", default="English", help="Target language (default: English).")
    parser.add_argument("--model", default="gpt-4o-mini", help="OpenAI-compatible model name (default: gpt-4o-mini).")

    args = parser.parse_args()

    try:
        # Instantiate the Translator
        translator_instance = Translator(model=args.model)

        # Perform the translation using the translate method
        translated_output = translator_instance.translate(
            source_text=args.source_text,
            source_language=args.source_lang,
            target_language=args.target_lang
        )

        print(f"Source ({args.source_lang}): {args.source_text}")
        print(f"Translation ({args.target_lang}): {translated_output}")

    except ValueError as e:
        print(f"Error: {e}")
        print("Please ensure OPENAI_API_KEY and OPENAI_API_BASE environment variables are set correctly.")

if __name__ == "__main__":
    main()

```

## 3.Integrate DSPy and mlflow

``` python
import dspy
from typing import Literal
import os

# uv add mlflow
# mlflow server --host 127.0.0.1 --port 8080

import mlflow
mlflow.set_experiment("DSPy Quickstart")
mlflow.dspy.autolog()


lm = dspy.LM('openai/gpt-4o', api_key=os.getenv('OPENAI_API_KEY'), api_base=os.getenv('OPENAI_API_BASE'))
dspy.configure(lm=lm)


class Classify(dspy.Signature):
    """Classify sentiment of a given sentence."""

    sentence: str = dspy.InputField()
    sentiment: Literal['positive', 'negative', 'neutral'] = dspy.OutputField()
    confidence: float = dspy.OutputField()

classify = dspy.Predict(Classify)
response = classify(sentence="I spend 2 hours to read this book.")
print(response.sentiment)
print(response.confidence)
```
