import streamlit as st
from PIL import Image
import pandas as pd

st.title("Classifier Demo")
st.header("Step 1: Enter an App Key")

key = st.text_input("96d093bf9fff46b5bdc4e058a754a43a")
if key == '':
   st.warning("An app key has not been entered")
   st.stop()
else:
   st.write("App Key has been uploaded!")

file_data = st.file_uploader("p7.png",type=['png'])
if file_data == None:
   st.warning("File needs to be uploaded")
   st.stop()
else:
   image = Image.open(file_data)
   st.image(image)   

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc

stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())

from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

# This is how you authenticate.
metadata = (('authorization', 'Key {}'.format(key)),)

request = service_pb2.PostModelOutputsRequest(

   # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
   model_id='food-item-recognition',
   inputs=[
     resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(base64=file_data.getvalue())))
   ])
response = stub.PostModelOutputs(request, metadata=metadata)

if response.status.code != status_code_pb2.SUCCESS:
   raise Exception("Request failed, status code: " + str(response.status.code))

names = []
confidences = []
for concept in response.outputs[0].data.concepts:
   names.append(concept.name)
   confidences.append(concept.value)   
df = pd.DataFrame({
   "Concept Name":names,
   "Model Confidence":confidences
})

st.dataframe(df)