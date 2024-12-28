import json
from fastapi import FastAPI, Request, HTTPException, Response
from pydantic_xml import BaseXmlModel, element
from pydantic import BaseModel, ConfigDict
from xml.dom.minidom import parse
from xml_parser import parse

app = FastAPI()
import exceptions.exception_handler


class PersonXML(BaseXmlModel, tag="person"):
    name: str = element(tag="name")


# Define the inner model for the "person" object
class Person(BaseModel):
    model_config = ConfigDict(extra='forbid')
    name: str


# Define the outer model that contains the "person" field
class PersonWrapper(BaseModel):
    model_config = ConfigDict(extra='forbid')
    person: Person


@app.middleware("http")
async def convert_xml_to_json(request: Request, call_next):
    if request.headers.get("content-type") == "application/xml":
        body = await request.body()
        try:
            # Convert XML to a Python dictionary
            xml_dict = parse(body)
            # Ensure the dictionary matches the Pydantic model structure
            modified_body = json.dumps(xml_dict).encode("utf-8")
            # Replace the request body with the JSON data
            request._body = modified_body
            # Update the content-type header to application/json
            request.scope["headers"] = [
                (b"content-type", b"application/json")
            ] + [
                (b"content-length", str(len(modified_body)).encode("utf-8"))
            ] + [
                (k.encode("utf-8"), v.encode("utf-8")) for k, v in request.headers.items() if k.lower() not in ["content-type", "content-length"]
            ]
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid XML format")
    response = await call_next(request)
    return response


@app.get("/")
async def index():
    PersonWrapper(**{"r": "i"})
    raise HTTPException(404, "Items not found")


@app.post("/")
async def index(person: PersonWrapper):
    data = f"""<?xml version="1.3"?>
    <person>
    <name>
        {person.person.name}
    </name>  
    </person>
    """
    return Response(content=data, media_type="application/xml")
