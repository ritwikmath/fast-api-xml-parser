# POC for handling XML request and response

Run application

```bash
fastapi.exe dev ./main.py
```

```bash
curl --location 'http://127.0.0.1:8000' \
--header 'Content-Type: application/xml' \
--data '<?xml version="1.3"?>
<person>
    <name>
        Your Name
    </name>
</person>'
```