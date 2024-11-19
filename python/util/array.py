# sample into chunking strings.
# this is used to break up string that mught be used to pass to vector methods
# and save them into vector store.  there is a overlap to show how to 
# take some context from the previous chunk.
# this is so when using vectors you retain some information
# from the previous chunk
sentence = "hello this is my sentence to break into chunks"

chunk = 5
start = 0
overlap = 1
chunk_array = []
while start < len(sentence):
    end = start + chunk
    chunk_array.append(sentence[start:end])
    start = end - overlap

print(chunk_array)
