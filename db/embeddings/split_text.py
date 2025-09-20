
from langchain_text_splitters import RecursiveCharacterTextSplitter


with open("test.txt", "r") as f:
    text = f.read()

text_splitter = RecursiveCharacterTextSplitter(
    # Set a really small chunk size, just to show.
    chunk_size=1000,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=True,
)
chunks = text_splitter.create_documents([text])

# chunks = chunk_text(text)
for chunk in chunks:
    print(chunk)
    print(f"Length of chunk in chars: {len(chunk.page_content)}")
    print("------")