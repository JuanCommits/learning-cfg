import torch
from base.vpl import VPL
from transformer_checker.transformer import (
    TransformerClassifier,
    TransformerClassifierConfig
)

class TransformerWrapper(VPL):
    def __init__(self, metadata_path: str, tokenizer, alphabet):
        self.tokenizer = tokenizer
        self.alphabet = alphabet

        self.metadata = self._load_metadata(metadata_path)
        self.model = self._load_model()

    
    def _load_metadata(self) -> None:
        # Load metadata from the specified path
        with open(self.metadata_path, 'r') as file:
            metadata = file.read()

        return metadata

    
    def _load_model(self, metadata: dict) -> None:
        config = metadata.get('config', None)

        if config is None:
            raise ValueError("Metadata does not contain 'config' key.")

        model_config = TransformerClassifierConfig(
            vocab_size=config.get('vocab_size', 1000),
            d_model=config.get('d_model', 256),
            n_heads=config.get('n_heads', 1),
            dim_ff=config.get('dim_ff', 512),
            n_layers=config.get('n_layers', 2),
            n_classes=config.get('n_classes', 2),
            max_seq_len=config.get('max_seq_len', 100),
        )

        model = TransformerClassifier(
            config=model_config
        )

        model_weights_path = metadata.get('model_weights_path', None)
        if model_weights_path is None:
            raise ValueError("Metadata does not contain 'model_weights_path' key.")

        model_weights = torch.load(model_weights_path)
        model.load_state_dict(model_weights)
        return model
    
    
    def is_accepted(self, sequence: str) -> bool:
        raise NotImplementedError
    