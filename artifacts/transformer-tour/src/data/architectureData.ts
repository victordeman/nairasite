import { ArchitectureData } from '../types';

export const OLD_TRANSFORMER: ArchitectureData = {
  name: "Original Transformer (2017)",
  nameIgbo: "Transformer mbụ (2017)",
  blocks: [
    {
      id: 'enc-input-embedding',
      name: 'Input Embedding',
      nameIgbo: 'Mtinyere Ihe Ntinye',
      description: 'Converts input tokens into dense vectors of d_model dimensions.',
      descriptionIgbo: 'Ọ na-atụgharị mkpụrụokwu ntinye ka ọ bụrụ vectors dị arọ nke akụkụ d_model.',
      position: [0, -5, 0],
      color: 0x6366f1
    },
    {
      id: 'enc-pos-encoding',
      name: 'Positional Encoding',
      nameIgbo: 'Ntinye Ọnọdụ',
      description: 'Adds information about the relative or absolute position of the tokens.',
      descriptionIgbo: 'Na-agbakwunye ozi gbasara ọnọdụ ikwu ma ọ bụ zuru oke nke akara ndị ahụ.',
      position: [0, -3, 0],
      color: 0xa855f7
    },
    {
      id: 'enc-mha',
      name: 'Multi-Head Attention',
      nameIgbo: 'Nleba anya nwere ọtụtụ isi',
      description: 'Allows the model to jointly attend to information from different representation subspaces.',
      descriptionIgbo: 'Na-enye ohere ka ihe nlereanya ahụ lekọta ozi sitere na subspaces nnọchite anya dịiche iche.',
      position: [0, -1, 0],
      color: 0x3b82f6
    },
    {
      id: 'enc-add-norm',
      name: 'Add & Norm',
      nameIgbo: 'Tinye & Hazie',
      description: 'Residual connection followed by layer normalization.',
      descriptionIgbo: 'Njikọ residual na-esochi ya site na nhazi oyi akwa.',
      position: [0, 1, 0],
      color: 0x10b981
    },
    {
      id: 'enc-ffn',
      name: 'Feed Forward',
      nameIgbo: 'Nye n\'ihu',
      description: 'Point-wise fully connected layers applied to each position identically.',
      descriptionIgbo: 'Ihe mkpuchi ejikọtara nke ọma na-emetụta ọnọdụ ọ bụla n\'otu aka ahụ.',
      position: [0, 3, 0],
      color: 0xf97316
    },
    {
      id: 'out-linear-softmax',
      name: 'Linear + Softmax Output',
      nameIgbo: 'Mmepụta Linear + Softmax',
      description: 'The final linear layer projects the decoder output to the vocabulary size. Softmax converts these logits to probabilities over the vocabulary.',
      descriptionIgbo: 'Ọwa linear ikpeazụ na-atụgharị mmepụta decoder n\'ogo okwu. Softmax na-atụgharị logits ndị a n\'ike n\'elu okwu.',
      position: [5, 1, 0],
      color: 0xec4899
    }
  ]
};

export const MODERN_TRANSFORMER: ArchitectureData = {
  name: "Modern Transformer (GPT-style)",
  nameIgbo: "Transformer nke oge a (ụdị GPT)",
  blocks: [
    {
      id: 'mod-mha',
      name: 'Masked Multi-Head Attention',
      nameIgbo: 'Nlebara anya nwere ọtụtụ isi ekpuchiri ekpuchi',
      description: 'Ensures the model only attends to previous positions to maintain causality.',
      descriptionIgbo: 'Na-eme ka ihe nlereanya ahụ lekwasị anya na ọnọdụ ndị gara aga iji nọgide na causality.',
      position: [0, 0, 0],
      color: 0x06b6d4
    }
  ]
};
