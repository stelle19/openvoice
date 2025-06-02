## How to run it 
Build the dockerfile locally: 
```
docker build -t openvoice .  
```
And run it with
```
docker run  -p 8000:8000 openvoice
```

To clone a voice run: 
```
curl -X POST "http://localhost:8000/synthesize/" -F "reference=@/path_to_input.mp3"   --output result.wav
```
