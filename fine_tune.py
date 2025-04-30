import openai
import os

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Upload the dataset file (uncomment if not already uploaded)
# Hindi: Pehle dataset file upload karein (agar pehle nahi kiya hai)
# file = openai.File.create(file=open("dataset.jsonl", "rb"), 
#                          purpose='fine-tune')
# print("Uploaded file ID:", file.id)

# Step 2: Start fine-tuning (replace 'file-ID-you-upload' with actual file ID)
# Hindi: Fine-tuning start karein (file ID yahan daalein)
resp = openai.FineTune.create(
    training_file="file-ID-you-upload",  # yahan apna file ID daalein
    model="gpt-3.5-turbo",
    n_epochs=2
)
print(resp) 