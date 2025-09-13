from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer
print("Imported transfromers")

# model = SentenceTransformer(
#     "sdadas/stella-pl" #"sdadas/mmlw-retrieval-roberta-large-v2",
#     trust_remote_code=True,
#     #device="cuda",
#     model_kwargs={"attn_implementation": "flash_attention_2", "trust_remote_code": True}
# )
# #Flash-Attention works only in 16-bit mode, so we need to cast the model to float16 or bfloat16
# model.bfloat16()
model_name = 'Snowflake/snowflake-arctic-embed-l-v2.0'
model = SentenceTransformer(model_name)

tokenizer = AutoTokenizer.from_pretrained("sdadas/stella-pl", trust_remote_code=True)
print("Imported models")
#text = "Paracetamol 500 mg — lek przeciwbólowy i przeciwgorączkowy."
text = """1
CHARAKTERYSTYKA PRODUKTU LECZNICZEGO
1. NAZWA PRODUKTU LECZNICZEGO
Edelan, 1 mg/g, krem
2. SKŁAD JAKOŚCIOWY I ILOŚCIOWY
Każdy g kremu zawiera 1 mg mometazonu furoinianu (Mometasoni furoas).
Pełny wykaz substancji pomocniczych, patrz punkt 6.1. 3. POSTAĆ FARMACEUTYCZNA
Krem
Biały lub prawie biały, gładki, jednolity krem."""

tokens = tokenizer.tokenize(text)
token_ids = tokenizer.encode(text)

print("Tokens:", tokens)
print("Number of tokens:", len(token_ids))

embeddings = model.encode(text, convert_to_numpy=True)
print("Embedding shape:", embeddings.shape)
print(embeddings)