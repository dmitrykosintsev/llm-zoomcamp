if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import hashlib

@transformer
def transform(data, *args, **kwargs):
    #print(type(data))
    #print("Printing data:", data)
    documents = []

    for doc in data['documents']:
        doc['course'] = data['course']
        # previously we used just "id" for document ID
        doc['document_id'] = generate_document_id(doc)
        documents.append(doc)

    print("Number of chunks:", len(documents))

    return documents

def generate_document_id(doc):
    combined = f"{doc['course']}-{doc['question']}-{doc['text'][:10]}"
    hash_object = hashlib.md5(combined.encode())
    hash_hex = hash_object.hexdigest()
    document_id = hash_hex[:8]
    return document_id
    
@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'