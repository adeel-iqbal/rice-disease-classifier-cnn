import tensorflow as tf
import numpy as np
from PIL import Image
import gradio as gr

# Load your saved model
model = tf.keras.models.load_model("rice_disease_model.keras")

# Class names in the same order as training
class_names = ['Bacterialblight', 'Blast', 'Brownspot', 'Tungro']

def predict_rice_disease(img):
    if img is None:
        return None, "Please upload an image first!"
    
    # Convert to RGB
    img = img.convert("RGB")
    
    # Resize to model input size
    img = img.resize((224, 224))
    
    # Convert to array - DON'T divide by 255! Model has Rescaling layer
    img_array = np.array(img, dtype=np.float32)  # Keep 0-255 range
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # Get predictions
    preds = model.predict(img_array, verbose=0)
    
    # Create results dictionary for all classes
    results = {}
    for i, class_name in enumerate(class_names):
        results[class_name] = float(preds[0][i])
    
    # Get top prediction for detailed info
    top_pred = max(results, key=results.get)
    confidence = results[top_pred] * 100
    
    # Disease info
    disease_info = {
        'Bacterialblight': '🦠 Bacterial disease - Use copper-based fungicides',
        'Blast': '💥 Fungal disease - Apply appropriate fungicides immediately', 
        'Brownspot': '🟤 Fungal infection - Improve air circulation',
        'Tungro': '🦠 Viral disease - Control leafhopper vectors'
    }
    
    info_text = f"## 🎯 Top Prediction: {top_pred} ({confidence:.1f}%)\n\n"
    info_text += f"**Treatment:** {disease_info[top_pred]}\n\n"
    info_text += "### All Predictions:\n"
    
    for disease, conf in sorted(results.items(), key=lambda x: x[1], reverse=True):
        info_text += f"- **{disease}**: {conf*100:.1f}%\n"
    
    return results, info_text

# Create interface with theme
iface = gr.Interface(
    fn=predict_rice_disease,
    inputs=[
        gr.Image(
            type="pil", 
            label="📷 Upload Rice Leaf Image",
            height=300
        )
    ],
    outputs=[
        gr.Label(
            label="🎯 Disease Predictions", 
            num_top_classes=4
        ),
        gr.Markdown(
            label="📋 Detailed Analysis"
        )
    ],
    title="🌾 Rice Disease Classifier (CNN - Deep Learning) 🔬",
    description="""
    🚀 **AI-Powered Rice Disease Detection System**
    
    📸 Upload a clear image of a rice leaf to get instant disease diagnosis
    
    🎯 Detects: Bacterial Blight • Blast • Brown Spot • Tungro
    
    ⚡ Powered by Deep Learning with 98.9% accuracy
    """,
    theme=gr.themes.Soft(
        primary_hue="green",
        secondary_hue="blue",
        neutral_hue="slate"
    ),
    examples=None,  
    cache_examples=False,
    flagging_mode="never"
)

# Launch
iface.launch(share=True, show_error=True)