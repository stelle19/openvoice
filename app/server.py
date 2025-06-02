from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import os
import uuid
import subprocess
import uvicorn

app = FastAPI()

@app.post("/synthesize/")
async def synthesize(reference: UploadFile = File(...)):
    # Save the reference file
    ref_id = str(uuid.uuid4())
    input_path = f"resources/{ref_id}.mp3"
    output_path = f"outputs_v2/output_v2-en.wav"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(reference.file, buffer)

    # Call main script with the new reference file
    os.system(f"python openvoice_app.py {input_path} {output_path}")

    return FileResponse(output_path, media_type="audio/wav", filename="result.wav")

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
    
    
# curl -X POST "http://localhost:8000/synthesize/" \
#   -F "reference=@/home/stelle94/conda_folder/OpenVoice_cp/resources/Trumpvoice.mp3" \
#   --output result.wav