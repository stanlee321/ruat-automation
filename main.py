# main.py

from typing import Optional
from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import time
import os
# Import configs
from configs import configs
from libs.tools import get_documents, reset_done
from libs.upload import upload_to_aws

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

class Item(BaseModel):
    nit: str
    username: str
    password: str
    tipo_usuario: str
    periodo_desde: int
    periodo_hasta: int
    description: Optional[str] = None

    
app = FastAPI()

@app.post("/download_documents/",  status_code=status.HTTP_201_CREATED)
def create_item(item: Item):

    reset_done()
    # Start the main function
    download_status, documents_list = get_documents(
        url_base = configs["URL_BASE"],
    )
    
    print("I got this...")
    print(download_status, documents_list)
    
    if download_status is None:
        raise HTTPException(
            status_code=500,
            detail="Some error ocurred",
            headers={"X-Error": "There goes my error"},
        )
    
    # Get actual iso datetime
    actual_iso_date = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    
    documents_in_s3 = []
    # If PDF file is obtained
    if len(documents_list) > 0:
        # Save the pdf file
        # Upload the file to S3
        # Write to S3
        
        
        for doc in documents_list:
   
            # Create filename
            full_file_name = f"impuestos/{item.nit}_{actual_iso_date}/{doc.split('/')[-1]}"
            
            upload_to_aws(configs["BUCKET_NAME"],
                          doc,
                          full_file_name
            )
            bucket_name = configs["BUCKET_NAME"]
            # Create full file url
            full_doc_url = f"https://{bucket_name}.s3.amazonaws.com/{full_file_name}"
            
            # Add the document to the list
            documents_in_s3.append(full_doc_url)
    
    json_compatible_item_data = jsonable_encoder({
        "documents": documents_in_s3
    })
    
    return JSONResponse(content=json_compatible_item_data)


@app.post("/items/")
async def create_item(item: Item):
    return item