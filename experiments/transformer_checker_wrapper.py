import torch
import json
from base.vpl import VPL
from base.alphabet import VPAlphabet
from transformer_checker.transformer import (
    TransformerClassifier,
    TransformerClassifierConfig
)
from transformer_checker.dataset.dyck_language_dataset import DyckLanguageTokenizer

class TransformerWrapper(VPL):
    def __init__(self, metadata_path: str, alphabet: VPAlphabet, tokenizer = None):
        self.alphabet = alphabet
        self.alphabet_symbols = list(self.alphabet.get_all_symbols())


        self.tokenizer = tokenizer if tokenizer else DyckLanguageTokenizer("".join(self.alphabet_symbols))

        self.metadata = self._load_metadata(metadata_path)
        self.model = self._load_model(self.metadata)

    
    def _load_metadata(self, metadata_path: str) -> dict:
        # Load metadata from the specified path
        with open(metadata_path, 'r') as file:
            metadata = json.loads(file.read())

        return metadata

    
    def _load_model(self, metadata: dict) -> TransformerClassifier:
        config = metadata.get('model_config', None)

        if config is None:
            raise ValueError("Metadata does not contain 'config' key.")

        config['vocab_size'] = len(self.alphabet_symbols)

        model_config = TransformerClassifierConfig(
            **config
        )

        model = TransformerClassifier(
            config=model_config
        )

        model_weights_path = metadata.get('wheigts_path', None)
        if model_weights_path is None:
            raise ValueError("Metadata does not contain 'weights_path' key.")

        model_weights = torch.load(model_weights_path)
        model.load_state_dict(model_weights)
        return model
    
    
    def is_accepted(self, sequence: str) -> bool:
        with torch.no_grad():
            sequence = self.tokenizer.tokenize(sequence)
            transformer_response = self.model(sequence)
            return torch.argmax(transformer_response, 1).item() == 1

    