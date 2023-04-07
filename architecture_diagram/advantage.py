from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.azure.identity import Users
from diagrams.custom import Custom



with Diagram("Ad-Vantage Architecture Diagram", direction="RL", show=False):
    with Cluster("App User"):
        ingress = Users("User")
    bucket = S3("S3 Bucket")
    with Cluster("Streamlit Cloud"):
        app = Custom("Streamlit App",r"./streamlit.png")

    chat_api = Custom("Product Name Generator", r"./openai.png")
    dalle_api = Custom("DALL·E API", r"./openai.png")
    ad_api = Custom("Ad from Product Description", r"./openai.png")


    ingress >> Edge(label="Give product description : Get product name", color="orange") << app
    app >> Edge(label="Generate product name ", color="black") << chat_api

    ingress >> Edge(label="Input title : Get Image", color="orange") << app
    app >> Edge(label="Image ", color="black") << dalle_api

    ingress << Edge(label=" Generate website / Download html code", color="black") << app
    app >> Edge(label="save images to S3 ", color="black") >> bucket

    ingress >> Edge(label="Input target audience  : Get Ad", color="orange") << app
    app >> Edge(label="Ad ", color="black") << ad_api



























