import streamlit as st
import boto3
import json
import math

def endpoint_invoke(data=[]):

    # Create a low-level client representing Amazon SageMaker Runtime
    sagemaker_runtime = boto3.client("sagemaker-runtime",
             aws_access_key_id ='****************',
             aws_secret_access_key = '***************',
             region_name = 'eu-west-1')

    # The name of the endpoint. The name must be unique within an AWS Region in your AWS account.
    endpoint_name = 'ShipmentPrediction'
    user_dict = {"features" : data }
    user_encode_data = json.dumps(user_dict).encode('utf-8')
    print(user_encode_data)

    response = sagemaker_runtime.invoke_endpoint(
                                EndpointName=endpoint_name,
                                ContentType='application/json',
                                Body=user_encode_data
                                )


    # Optional - Print the response body and decode it so it is human read-able.
    response = response['Body'].read().decode('utf-8')
    return  response


res = 0
prob = 0

st.title('Shipment Prediction For Arabian Cement')  ### Start web app by name our app

st.markdown(

    """
    <style> 
    [data-testid="stSidebar"] [aria-expanded ='true'] >div:first-child{
        width :350px 
    }

    [data-testid="stSidebar"] [aria-expanded ='false'] >div:first-child{
        width :350px 
        margin-left :-350px
    }
    </style>
    """,
    unsafe_allow_html=True,

)

st.sidebar.title('Arabian Cement')

app_mode = st.sidebar.selectbox('Choose App Mode',
                                [ 'Make_Prediction','About_app'])
if app_mode == 'About_app':
    st.markdown('In this Application we are using Aws Endpoint to create prediction')

    st.markdown(

        """
    <style> 
    [data-testid="stSidebar"] [aria-expanded ='true'] >div:first-child{
        width :350px 
    }

    [data-testid="stSidebar"] [aria-expanded ='false'] >div:first-child{
        width :350px 
        margin-left :-350px
    }
    </style>
    """,
        unsafe_allow_html=True,

    )



elif app_mode == "Make_Prediction":
    st.markdown(

        """
        <style> 
        [data-testid="stSidebar"] [aria-expanded ='true'] >div:first-child{
            width :350px 
        }

        [data-testid="stSidebar"] [aria-expanded ='false'] >div:first-child{
            width :350px 
            margin-left :-350px
        }
        </style>
        """,
        unsafe_allow_html=True,

    )
    col = st.columns(2)
    col[0].markdown("Please Choose your shipment type")
    shipment = col[0].selectbox("choose shipment",['Bags','Bulk',])

    col[1].markdown("Enter distance in Km")
    distance = col[1].number_input('Kilometers', min_value=0)

    invoke = st.button('submit')
    if invoke and distance > 0:
        res = 0
        prob = 0
        res = endpoint_invoke([shipment, distance])
        res, prob = res.split(",")

    prob = math.ceil(float(prob) * 100)

    c = st.columns(2)
    c[0].markdown('Result :')
    c[0].text(res)

    c[1].markdown('Prediction Confidence')
    c[1].text(prob)



