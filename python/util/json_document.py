#add embedding to a document
doc = {
        "id":1, 
        "text":"this is my text", 
        "metadata":{
            "val1":1,
            "val2":{
                "message":"this text is for embedding"
            }
        }
    }
print(doc)
doc["embedding"] = [0.1, 0.3, 0.5]
print(doc)
print('val1 =', doc["metadata"]["val1"])
print('message =', doc["metadata"]["val2"]["message"])

val1 = doc.get("metadata",{}).get('val1',{})
